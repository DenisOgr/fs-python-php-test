import yaml
from faker import Faker
from elasticsearch.helpers import parallel_bulk
from elasticsearch import Elasticsearch
import random
from collections import deque
import time
thread_count = 4
cores = [
    'elasticsearch_document_core',
    'elasticsearch_form_contents_core',
     'elasticsearch_comments_core',
     'elasticsearch_chats_core'
]
with open("conf.yaml", 'r') as stream:
    conf = yaml.load(stream)

es = Elasticsearch("%s:%s"%(conf['elasticsearch_host'], str(conf['elasticsearch_port'])))

count_users = conf['count_users']
count_organisations = conf['count_organisations']
count_forms = conf['count_forms']
count_documents = conf['count_documents']
count_chats = conf['count_chats']
count_comments = conf['count_comments']

fake = Faker()

#elasticsearch_form_contents_core
core = conf['elasticsearch_form_contents_core']
print("Seeding index %s...." % core)


def seed_forms_generator(fake: Faker, index, count):
    for form_id in range(count):
        yield {
            "_index": index,
            "_type":"_doc",
            "_source": {
                "form_id": form_id,
                "title": fake.sentence(nb_words=7),
                "description": fake.paragraph(nb_sentences=6),
                "content": fake.text(max_nb_chars=2000),
                "date_create": fake.date(pattern="%Y-%m-%d"),
                "is_fillable": True
                }
        }
seedr = seed_forms_generator(fake, core, count_forms)
deque(parallel_bulk(es, seedr, thread_count=thread_count), maxlen=0)
time.sleep(1)
print("Count documents in core '%s' = %s"%(core, es.count(index=core)['count']))



#elasticsearch_document_core
core = conf['elasticsearch_document_core']
print("Seeding index %s...." %core)

def seed_document_generator(fake: Faker, index, count, ):
    for project_id in range(count):
        yield {
            "_index": index,
            "_type":"_doc",
            "_source": {
                "project_id": project_id,
                "form_id": random.randint(0, count_forms),
                "user_id": random.randint(0, count_users),
                "organisation_id": random.randint(0, count_organisations),
                "file_name": fake.sentence(nb_words=7),
                "file_type": random.choice(['pdf', 'world', 'excel', 'ppt']),
                "date_create": fake.date(pattern="%Y-%m-%d"),

                "message": fake.paragraph(nb_sentences=6),
                "signer_email": fake.company_email(),
                "inviter2sign_email": fake.company_email(),
                "is_template": True,
                "is_public": random.choice([True, False]),

            }
    }


seedr = seed_document_generator(fake, core, count_documents)
deque(parallel_bulk(es, seedr, thread_count=thread_count))
time.sleep(1)
print("Count documents in core '%s' = %s"%(core, es.count(index=core)['count']))


#elasticsearch_comments_core
core = conf['elasticsearch_comments_core']
print("Seeding index %s...." %core)

def seed_comments_generator(fake: Faker, index, count):
    for chat_id in range(count):
        yield {
            "_index": index,
            "_type":"_doc",
            "_source": {
                "chat_id": chat_id,
                "user_id": random.randint(0, count_users),
                "organisation_id": random.randint(0, count_organisations),
                "comment": fake.paragraph(nb_sentences=6),
                "description": fake.paragraph(nb_sentences=6),
                "date_create": fake.date(pattern="%Y-%m-%d"),
                "date_create_chat": fake.date(pattern="%Y-%m-%d"),
            }
    }


seedr = seed_comments_generator(fake, core, count_comments)
deque(parallel_bulk(es, seedr, thread_count=thread_count))
time.sleep(1)
print("Count documents in core '%s' = %s"%(core, es.count(index=core)['count']))


#elasticsearch_chats_core
core = conf['elasticsearch_chats_core']
print("Seeding index %s...." %core)

def seed_comments_generator(fake: Faker, index, count):
    for chat_id in range(count):
        yield {
            "_index": index,
            "_type":"_doc",
            "_source": {
                "chat_id": chat_id,
                "user_id": random.randint(0, count_users),
                "organisation_id": random.randint(0, count_organisations),
                "comment": fake.paragraph(nb_sentences=6),
                "description": fake.paragraph(nb_sentences=6),
                "date_create": fake.date(pattern="%Y-%m-%d"),
                "date_create_chat": fake.date(pattern="%Y-%m-%d"),
            }
    }


seedr = seed_comments_generator(fake, core, count_chats)
deque(parallel_bulk(es, seedr, thread_count=thread_count), maxlen=0)
time.sleep(1)
print("Count documents in core '%s' = %s"%(core, es.count(index=core)['count']))

