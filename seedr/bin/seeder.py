from faker import Faker
from elasticsearch import Elasticsearch
import yaml

fake = Faker()

with open("conf.yaml", 'r') as stream:
    conf = yaml.load(stream)

es = Elasticsearch([conf['elasticsearch_host']+':'+str(conf['elasticsearch_port'])])


