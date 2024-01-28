from elasticsearch import Elasticsearch

elastic_url = "http://elasticsearch:9200"
es_client = Elasticsearch([elastic_url])

index_name = "logs"
doc_type = "_doc"


def check_connection():
    print("Checking connection to Elasticsearch...")
    is_connected = False

    while not is_connected:
        try:
            es_client.cluster.health()
            print("Successfully connected to Elasticsearch")
            is_connected = True
        except Exception as e:
            print("Connection failed, retrying in 2 seconds...")
            print(e)


def create_index(index):
    try:
        es_client.indices.create(index=index)
        print(f"Created index {index}")
    except Exception as e:
        print(f"An error occurred while creating the index {index}:")
        print(e)


def set_logs_mapping():
    try:
        schema = {
            "properties": {
                "level": {"type": "text"},
                "message": {"type": "text"},
                "resourceId": {"type": "text"},
                "timestamp": {"type": "date"},
                "traceId": {"type": "text"},
                "spanId": {"type": "text"},
                "commit": {"type": "text"},
                "metadata": {"type": "text"},
            }
        }

        es_client.indices.put_mapping(index=index_name, doc_type=doc_type, body=schema)

        print("Subtitle mapping created successfully")
    except Exception as e:
        print("An error occurred while setting the subtitle mapping:")
        print(e)
