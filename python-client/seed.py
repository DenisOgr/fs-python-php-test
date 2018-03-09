from elasticsearch import Elasticsearch
from faker import Faker
import env


def set_documents():
    elastic = Elasticsearch([{'host': env.ELASTIC_HOST, 'port': env.ELASTIC_PORT}])
    fake = Faker()
    for i in range(1, 100000):
        form_id = fake.random.randint(100000,1000000000)
        print(form_id)
        doc = {
            'form_id': form_id,
            'organization_id': fake.random.randint(1,1000000),
            'user_id': fake.random.randint(1,100),
            'project_id': i,
            'title': fake.sentence(),
            'content': fake.text(),
        }

        res = elastic.index(index="documents", doc_type='doc', body=doc)
        print(res['created'])
        create_form_content(form_id)


def create_form_content(form_id):
    elastic = Elasticsearch([{'host': env.ELASTIC_HOST, 'port': env.ELASTIC_PORT}])
    fake = Faker()

    doc = {
        'form_id': form_id,
        'title': fake.sentence(),
        'content': fake.text(),
    }

    elastic.index(index="form_content", doc_type='doc', body=doc)


set_documents()


