#!/usr/bin/env python

"""Script that loads JSON files from a directory to an Elasticsearch cluster"""

import json
import os
from os.path import abspath, join, dirname, isfile
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

# Path to the index settings file
INDEX_SETTINGS_FILE_ABSOLUTE_PATH = os.environ.get("INDEX_SETTINGS_FILE_ABSOLUTE_PATH")

# Path to the index mappings file
INDEX_MAPPINGS_FILE_ABSOLUTE_PATH = os.environ.get("INDEX_MAPPINGS_FILE_ABSOLUTE_PATH")

# Path to the directory containing the JSON bulk data
JSON_BULK_DATA_ABSOLUTE_PATH = os.environ.get("JSON_BULK_DATA_ABSOLUTE_PATH")

# Elasticsearch index name to upload the data
ES_INDEX_NAME = os.environ.get("ES_INDEX_NAME")

# Elasticsearch host URL
ES_HOST = os.environ.get("ES_HOST")


# Construct the path to the JSON bulk data directory
JSON_DIRECTORY = join(
    dirname(abspath(__file__)),
    JSON_BULK_DATA_ABSOLUTE_PATH,
)

# Get the list of JSON file paths in the JSON bulk data directory
DATASET_PATHS = [
    join(JSON_DIRECTORY, f)
    for f in os.listdir(JSON_DIRECTORY)
    if isfile(join(JSON_DIRECTORY, f))
]

def generate_actions():
    """
    Reads each JSON file in the directory and yields a single document for each file.
    This function is passed into the streaming_bulk() helper to create many documents in sequence.

    Yields:
        dict: A single document loaded from a JSON file.

    Raises:
        json.JSONDecodeError: If there is an error decoding JSON in a file.

    """
    print("generate_actions method called")
    for path in DATASET_PATHS:
        if path.endswith(".json"):
            with open(path, mode="r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {path}: {e}")
                    continue
                yield data

def create_index(client):
    """
    Creates an Elasticsearch index with the specified settings and mappings.

    Args:
        client (Elasticsearch): The Elasticsearch client instance.

    Raises:
        FileNotFoundError: If the index settings or mappings file is not found.

    """
    with open(INDEX_SETTINGS_FILE_ABSOLUTE_PATH) as f:
        index_settings = json.load(f)
    with open(INDEX_MAPPINGS_FILE_ABSOLUTE_PATH) as f:
        index_mappings = json.load(f)
    client.indices.create(
        index=ES_INDEX_NAME, settings=index_settings, mappings=index_mappings
    )
    print(f"Created a new index: {ES_INDEX_NAME}")


def main():
    """
    Main function that performs the Elasticsearch indexing process.

    Raises:
        ConnectionError: If there is an error connecting to the Elasticsearch cluster.

    """
    print("Creating an Elasticsearch client...")
    client = Elasticsearch(ES_HOST)


    if client.indices.exists(index=ES_INDEX_NAME):
        print(f"Index already existing: {ES_INDEX_NAME}")
    else:
        print("Creating an index...")
        create_index(client)


    print("Indexing documents...")
    number_of_docs = len(DATASET_PATHS)

    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client,
        index=ES_INDEX_NAME,
        actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))
if __name__ == "__main__":
    """
    Entry point of the script. Executes the main indexing process.

    """
    main()