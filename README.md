# Loading JSON Files to Elasticsearch

This repository contains the python script for loading JSON data into Elasticsearch using Docker.

## Prerequisites

Before running the application, please ensure you have the following:

- Docker installed on your system

## Setup

1. Clone this repository to your local machine:

```
git clone https://github.com/raowaqasakram/elasticsearch-bulk-loader.git
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
      - In the `environment` section, update the following line with the elasticsearch index name where you want to load the data:

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
     
## Load Data
After completing all the configurations as mentioned above. You can run the container using the following command.

```
sudo docker-compose up
```

## Build custom Docker Image
To modify the primary script file, es_bulk_load_script.py, and generate a Docker image using the given Dockerfile, execute the following command:

```
sudo docker build -t <image-tag-name> .
```

## About Me

This is developed with ❤️ by **Rao Waqas Akram**. 
Visit my blog on [Hashnode](https://raowaqasakram.hashnode.dev/) and 
Connect with me on [LinkedIn](https://www.linkedin.com/in/raowaqasakram/).
