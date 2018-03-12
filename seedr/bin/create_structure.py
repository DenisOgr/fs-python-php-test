from elasticsearch import Elasticsearch
import yaml

cores = [
    'elasticsearch_document_core',
    'elasticsearch_form_contents_core',
     'elasticsearch_comments_core',
     'elasticsearch_chats_core'
]
with open("conf.yaml", 'r') as stream:
    conf = yaml.load(stream)

es = Elasticsearch([conf['elasticsearch_host']+':'+str(conf['elasticsearch_port'])])

for core in cores:
    print("Creating index %s...."%core)
    with open("core_configs/%s"%core, 'r') as stream:
        body = stream.read()

    es.indices.create(index=conf[core], body=body, request_timeout=60)





