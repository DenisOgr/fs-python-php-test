from elasticsearch import Elasticsearch
import env
import numpy as np
import json
from multiprocessing import Process,Queue
import time
from faker import Faker
import random

def get_elastic():
    return Elasticsearch([{'host': env.ELASTIC_HOST, 'port': env.ELASTIC_PORT}])


def get_user_documents(elastic, user_id, index, doc_type, q):
    query = {
        'query': {
            'match': {
                'user_id': user_id
            }
        }
    }

    documents = _get_documents(elastic, index, doc_type, query, 'form_id')

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

    documents = _get_documents(elastic, index, doc_type, query, 'project_id')

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

    return _get_documents(elastic, index, doc_type, query, 'form_id')


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

    return _get_documents(elastic, index, doc_type, query, 'project_id')


def get_public_documents(elastic, index, doc_type, queue, user_id, query, organization_id):
    query = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'organization_id': organization_id
                        }
                    },
                    {
                        'more_like_this': {
                            'fields': ['title'],
                            'like': [query],
                            'min_term_freq': 1,
                            'min_doc_freq': 1
                        },
                    }
                ],
                'must_not': [
                    {
                        'term': {
                            'user_id': user_id
                        }
                    }
                ]
            }
        },
    }

    documents = _get_documents(elastic, index, doc_type, query, 'project_id')

    queue.put(documents)


def get_user_comments(elastic, index, doc_type, queue, user_id, query):
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
                            'fields': ['comment'],
                            'like': [query],
                            'min_term_freq': 1,
                            'min_doc_freq': 1
                        },
                    }
                ]
            }
        },
    }

    results= _get_documents(elastic, index, doc_type, query, False, True)

    queue.put(results)


def get_user_chats(elastic, index, doc_type, queue, user_id, query):
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
                            'fields': ['comment'],
                            'like': [query],
                            'min_term_freq': 1,
                            'min_doc_freq': 1
                        },
                    }
                ]
            }
        },
    }

    results= _get_documents(elastic, index, doc_type, query, False, True)

    queue.put(results)


def _get_documents(elastic, index, doc_type, query, filter_field, get_hits=False):
    result = elastic.search(index=index, doc_type=doc_type, body=query, size=env.DEFAULT_SIZE)

    documents = np.array([])

    if result['hits']['total'] == 0:
        return documents

    if get_hits:
        return result['hits']['hits']

    documents = np.array([hit['_source'][filter_field] for hit in result['hits']['hits']])

    return documents


def process():
    fake = Faker()

    title = fake.sentence(nb_words=2)
    user_id = random.randint(0, 10000)
    organization_id = random.randint(0, 1000)

    esastic = get_elastic()

    documents_by_title_queue = Queue()
    documents_by_title_process = Process(target=get_user_documents_by_title,
                                         args=(esastic, user_id, title, 'documents', 'doc', documents_by_title_queue,))
    documents_by_title_process.start()
    documents_by_title_process.join()
    documents_by_title = documents_by_title_queue.get()

    documents_queue = Queue()
    documents_process = Process(target=get_user_documents,
                                args=(esastic, user_id, 'documents', 'doc', documents_queue,))
    documents_process.start()
    documents_process.join()
    documents = documents_queue.get()

    user_form_content = get_user_form_content(esastic, documents, title, 'form_contents', 'doc')
    user_projects_by_content = get_user_projects_by_forms(esastic, user_form_content, user_id, 'documents', 'doc')

    projects = np.unique(np.concatenate([user_projects_by_content, documents_by_title]))

    return {
        'projects': projects
    }


result = process()
print(result)