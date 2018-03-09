from elasticsearch import Elasticsearch
import env
import numpy as np
import json
from multiprocessing import Process,Queue
import time


def get_elastic():
    return Elasticsearch([{'host': env.ELASTIC_HOST, 'port': env.ELASTIC_PORT}])


def get_user_documents(elastic, user_id, index, doc_type, q):
    result = elastic.search(index=index, doc_type=doc_type, body={"query": {"match": {'user_id':user_id}}}, size=env.DEFAULT_SIZE)
    documents = np.array([])

    if result['hits']['total'] == 0:
        q.put(documents)
        return True

    documents = np.array([hit['_source']['form_id'] for hit in result['hits']['hits']])

    q.put(documents)


def get_user_documents_by_title(elastic, user_id, title, index, doc_type,q):
    query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'user_id': user_id
                        }
                    },
                    {
                        'more_like_this': {
                            'fields': ['title'],
                            'like': [title],
                            'min_term_freq': 1,
                            'min_doc_freq': 1
                        },
                    }
                ]
            }
        },
    }
    result = elastic.search(index=index, doc_type=doc_type, body=query, size=env.DEFAULT_SIZE)

    documents = np.array([])

    if result['hits']['total'] == 0:
        q.put(documents)
        return True

    documents = np.array([hit['_source']['project_id'] for hit in result['hits']['hits']])

    q.put(documents)


def get_user_form_content(elastic, form_ids, title, index, doc_type):
    query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'terms': {
                            'form_id': [''.join(str(form)) for form in form_ids]
                        }
                    },
                    {
                        'more_like_this': {
                            'fields': ['title'],
                            'like': [title],
                            'min_term_freq': 1,
                            'min_doc_freq': 1
                        },
                    }
                ]
            }
        },
    }

    result = elastic.search(index=index, doc_type=doc_type, body=query, size=env.DEFAULT_SIZE)

    documents = np.array([])

    if result['hits']['total'] == 0:
        return documents

    documents = np.array([hit['_source']['form_id'] for hit in result['hits']['hits']])

    return documents


def get_user_projects_by_forms(elastic, form_ids, user_id, index, doc_type):
    query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'terms': {
                            'form_id': [''.join(str(form)) for form in form_ids]
                        }
                    },
                    {
                        'match': {
                            'user_id': user_id
                        }
                    }
                ]
            }
        },
    }

    result = elastic.search(index=index, doc_type=doc_type, body=query, size=env.DEFAULT_SIZE)

    documents = np.array([])

    if result['hits']['total'] == 0:
        return documents

    documents = np.array([hit['_source']['project_id'] for hit in result['hits']['hits']])

    return documents


esastic = get_elastic()
title = 'meet'
user_id = 30

documents_by_title_queue = Queue()
documents_by_title_process = Process(target=get_user_documents_by_title, args=(esastic,user_id,title, 'documents','doc',documents_by_title_queue,))
documents_by_title_process.start()
documents_by_title_process.join()
documents_by_title = documents_by_title_queue.get()

documents_queue = Queue()
documents_process = Process(target=get_user_documents, args=(esastic, user_id, 'documents','doc',documents_queue,))
documents_process.start()
documents_process.join()
documents = documents_queue.get()

user_form_content = get_user_form_content(esastic, documents, title, 'form_content', 'doc')
user_projects_by_content = get_user_projects_by_forms(esastic, user_form_content, user_id, 'documents','doc')

result = np.unique(np.concatenate([user_projects_by_content, documents_by_title]))

print(json.dumps(result.tolist()))