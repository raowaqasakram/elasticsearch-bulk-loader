# Loading JSON Files to Elasticsearch

This repository contains the python script for loading JSON data into Elasticsearch using Docker.

## Prerequisites

Before running the application, please ensure you have the following:

- Docker installed on your system

## Setup

1. Clone this repository to your local machine:

```
      git clone https://github.com/raowaqasakram/elasticsearch-bulk-loader
```

2. Update the configuration files:
   
   - Navigate to the `configs` folder.
   - Open the `index_mappings.json` file and update it with your own index mappings.
   - Open the `index_settings.json` file and update it with your own index settings.

3. Place JSON files:
   
   - Navigate to the `jsonData` folder.
   - Put all the JSON files you want to load into Elasticsearch in the `jsonData` folder.

4. Docker Compose configuration:
   
   - Open the `docker-compose.yml` file.
   - In the `environment` section, update the following line by adding the elasticsearch index name where you want to load the data:
     ```
     - ES_INDEX_NAME=elon_data_index
     ```
   - Make sure to link this application with the network where Elasticsearch is already running.
     ```
     networks:
      bulk_data_network: 
        # Replace 'elasticsearch_existing_network' with your actual network name of Elasticsearch
        name: elasticsearch_existing_network
        external: true
     ```
     
5. Dockerfile:
   
   - If you make any changes to the original file `es_bulk_load_script.py`, build the Docker image using the provided Dockerfile by running the following commmand
   ```
   sudo docker build -t <image-tag-name> .
   ```
6. Run Application
  - Run application using the following command
   ````
   sudo docker-compose up
   ````

That's it! You can now run the application to load your JSON data into Elasticsearch.
