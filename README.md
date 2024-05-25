# sam-bedrock-kb-aurora-rag

## 概要

RAGのサンプルシステムをKnowledge Bases for Amazon Bedrock、Amazon Aurora PostgreSQL、Amazon S3を用いて、SAMで実装しています。  

## デプロイ手順

1. 以下コマンドでリポジトリをクローンし、ディレクトリを移動

```bash
git clone https://github.com/tsukuboshi/sam-bedrock-kb-aurora-rag
cd sam-bedrock-kb-aurora-rag
```

2. 以下コマンドで、SAMアプリをビルド

```bash
sam build
```

3. 以下コマンドで、SAMアプリをデプロイ

```bash
sam deploy 
  [--parameter-overrides]
  [AuroraSchedulerState=<Auroraのスケジューラの状態>]
  [DatabasePassword=<データベースパスワード>]
  [EmbeddingModelId=<Bedrockの埋め込みモデルARN>]

  
```

## パラメータ詳細

|パラメータ名|デフォルト値|指定可能な値|説明|
|---|---|---|---|
|AuroraSchedulerState|ENABLED|ENABLED/DISABLED|Auroraクラスター起動停止スケジューラの状態|
|DatabasePassword|-|文字列|データベースパスワード|
|EmbeddingModelId|cohere.embed-multilingual-v3|amazon.titan-embed-text-v1/cohere.embed-english-v3/cohere.embed-multilingual-v3/|Bedrockの埋め込みモデルのID|
