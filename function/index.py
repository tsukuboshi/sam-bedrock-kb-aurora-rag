import boto3
import cfnresponse
import logging
from typing import Any, Dict

logger = logging.getLogger()

rds_data = boto3.client('rds-data')

def execute_statement(resource_arn: str, database_name: str, secret_arn: str, sql: str) -> Any:
    response = rds_data.execute_statement(
        resourceArn=resource_arn,
        database=database_name,
        secretArn=secret_arn,
        sql=sql
    )
    return response


def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    request_type = event['RequestType']
    logger.info(f"RequestType: {request_type}")

    try:
        if request_type == 'Create':
            # Get the parameters from the event
            # embedding_model_id = event['ResourceProperties']['BedrockEmbeddingModelId']
            dimension = event['ResourceProperties']['Dimension']
            resource_arn = event['ResourceProperties']['ResourceArn']
            secret_arn = event['ResourceProperties']['SecretArn']
            database_name = event['ResourceProperties']['DatabaseName']
            database_password = event['ResourceProperties']['DatabasePassword']
            table_name = event['ResourceProperties']['TableName']
            schema_name = event['ResourceProperties']['SchemaName']
            user_name = event['ResourceProperties']['UserName']
            metadata_field = event['ResourceProperties']['MetadataField']
            primary_key_field = event['ResourceProperties']['PrimaryKeyField']
            text_field = event['ResourceProperties']['TextField']
            vector_field = event['ResourceProperties']['VectorField']

            # # Set the dimension based on the embedding model id
            # if embedding_model_id == 'amazon.titan-embed-text-v1':
            #     dimension = 1536
            # if embedding_model_id == 'cohere.embed-english-v3':
            #     dimension = 1024
            # if embedding_model_id == 'cohere.embed-multilingual-v3':
            #     dimension = 1024

            # logger.info(f"Dimension: {dimension}")

            # Set up vector store on aurora
            create_extension = f"""
            CREATE EXTENSION IF NOT EXISTS vector;
            """
            create_extension_res = execute_statement(resource_arn, database_name, secret_arn, create_extension)
            logger.info(f"Create Extension Response: {create_extension_res}")

            create_role = f"""
            CREATE ROLE {user_name} WITH PASSWORD '{database_password}' LOGIN;
            """
            create_role_res = execute_statement(resource_arn, database_name, secret_arn, create_role)
            logger.info(f"Create Role Response: {create_role_res}")

            create_shema = f"""
            CREATE SCHEMA {schema_name};
            """
            create_shema_res = execute_statement(resource_arn, database_name, secret_arn, create_shema)
            logger.info(f"Create Schema Response: {create_shema_res}")

            grant_schema = f"""
            GRANT ALL ON SCHEMA {schema_name} to {user_name};
            """
            grant_schema_res = execute_statement(resource_arn, database_name, secret_arn, grant_schema)
            logger.info(f"Grant Schema Response: {grant_schema_res}")

            create_table = f"""
            CREATE TABLE {table_name} ({primary_key_field} uuid PRIMARY KEY, {vector_field} vector({dimension}), {text_field} text, {metadata_field} json)
            """
            create_table_res = execute_statement(resource_arn, database_name, secret_arn, create_table)
            logger.info(f"Create Table Response: {create_table_res}")

            grant_table = f"""
            GRANT ALL ON TABLE {table_name} TO {user_name};
            """
            grant_table_res = execute_statement(resource_arn, database_name, secret_arn, grant_table)
            logger.info(f"Grant Table Response: {grant_table_res}")

            create_index = f"""
            CREATE INDEX on {table_name} USING hnsw ({vector_field} vector_cosine_ops);
            """
            create_index_res = execute_statement(resource_arn, database_name, secret_arn, create_index)
            logger.info(f"Create Index Response: {create_index_res}")

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        if request_type == 'Update':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        if request_type == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': str(e)})
