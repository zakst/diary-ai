# diary-ai

diary-ai provides a pipeline for processing, embedding, and storing diary entries using OpenAI's embedding API and Qdrant vector database

## Prerequisites

#### Dependencies
* [Python 3.11+](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)

#### External Services
* Create a [Qdrant Account](https://qdrant.tech/) a free one will do
* Create an [Open API Secret Key](https://platform.openai.com/api-keys)

## Installation

```shell
  poetry install
```

Create a `.env` file and add the following to it

```dotenv
QDRANT_URL=qdrant_endpoint # you can find it in the cluster
QDRANT_API_KEY=api_key
QDRANT_COLLECTION=collection_name # defaults to diaries
OPEN_AI_API_KEY=api_key
```

Lastly run the following script

```shell
  python setup.py
```

> Note: the method [store_diary_entry](qdrant_utils/qdrant_repository.py) will not allow duplication of samples

## Reset Qdrant Data
You can use the following script to delete all qdrant data in your `QDRANT_COLLECTION`

```shell
  python qdrant_utils/delete_collection_data.py
```