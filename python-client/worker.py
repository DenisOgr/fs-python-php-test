from elasticsearch import Elasticsearch
import env
import numpy as np
import json
from multiprocessing import Process,Queue
import time
from faker import Faker
import random
from threading import Thread


class Worker:
    def get_elastic(self):
        return Elasticsearch([{'host': env.ELASTIC_HOST, 'port': env.ELASTIC_PORT}])

    def get_user_documents(self, elastic, user_id, index, doc_type, q):
        query = {
            'query': {
                'match': {
                    'user_id': user_id
                }
            }
        }

        documents = self._get_documents(elastic, index, doc_type, query, 'form_id')

        q.put(documents)

    def get_user_documents_by_title(self, elastic, user_id, query, index, doc_type, q):
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
                                'fields': ['file_name'],
                                'like': [query],
                                'min_term_freq': 1,
                                'min_doc_freq': 1
                            },
                        }
                    ]
                }
            },
        }
        documents = self._get_documents(elastic, index, doc_type, query, 'project_id')
        q.put(documents)

    def get_user_form_content(self, elastic, form_ids, query, index, doc_type):
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
                                'fields': ['file_name'],
                                'like': [query],
                                'min_term_freq': 1,
                                'min_doc_freq': 1
                            },
                        }
                    ]
                }
            },
        }

        return self._get_documents(elastic, index, doc_type, query, 'form_id')

    def get_user_projects_by_forms(self, elastic, form_ids, user_id, index, doc_type):
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

        return self._get_documents(elastic, index, doc_type, query, 'project_id')

    def get_public_documents(self, elastic, index, doc_type, queue, user_id, query, organisation_id):
        query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'match': {
                                'organisation_id': organisation_id
                            }
                        },
                        {
                            'more_like_this': {
                                'fields': ['file_name'],
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

        documents = self._get_documents(elastic, index, doc_type, query, 'project_id')

        queue.put(documents)

    def get_user_comments(self, elastic, index, doc_type, queue, user_id, query):
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

        results = self._get_documents(elastic, index, doc_type, query, False, True)

        queue.put(results)

    def get_user_chats(self, elastic, index, doc_type, queue, user_id, query):
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

        results = self._get_documents(elastic, index, doc_type, query, False, True)

        queue.put(results)

    def _get_documents(self, elastic, index, doc_type, query, filter_field, get_hits=False):
        result = elastic.search(index=index, doc_type=doc_type, body=query, size=env.DEFAULT_SIZE)

        documents = np.array([])

        if result['hits']['total'] == 0:
            return documents

        if get_hits:
            return result['hits']['hits']

        documents = np.array([hit['_source'][filter_field] for hit in result['hits']['hits']])

        return documents

    def _get_result(self, projects, comments, chats):
        projects = projects.tolist()

        if isinstance(comments, np.ndarray):
            comments = comments.tolist()

        if isinstance(chats, np.ndarray):
            chats = chats.tolist()

        return json.dumps({
            'projects': projects,
            'comments': comments,
            'chats': chats
        })

    def process(self):
        fake = Faker()

        title = fake.sentence(nb_words=2)
        user_id = random.randint(0, 10000)
        organisation_id = random.randint(0, 1000)

        elastic = self.get_elastic()
        # user documents by user_id

        documents_queue = Queue()
        documents_process = Thread(target=self.get_user_documents,
                                    args=(
                                    elastic, user_id, env.ELASTIC_DOCUMENTS_INDEX, env.ELASTIC_CORE, documents_queue,))
        documents_process.start()

        # user documents by query and user_id

        documents_by_title_queue = Queue()
        documents_by_title_process = Thread(target=self.get_user_documents_by_title,
                                             args=(
                                             elastic, user_id, title, env.ELASTIC_DOCUMENTS_INDEX, env.ELASTIC_CORE,
                                             documents_by_title_queue,))
        documents_by_title_process.start()
        # public documents by org_id , query and user_id

        public_documents_queue = Queue()
        public_documents_process = Thread(target=self.get_public_documents,
                                           args=(elastic, env.ELASTIC_DOCUMENTS_INDEX, env.ELASTIC_CORE,
                                                 public_documents_queue,
                                                 user_id, title, organisation_id))
        public_documents_process.start()

        # user comments by user_id and query
        comments_queue = Queue()
        comments_process = Thread(target=self.get_user_comments,
                                   args=(elastic, env.ELASTIC_COMMENTS_INDEX, env.ELASTIC_CORE, comments_queue, user_id,
                                         title))
        comments_process.start()

        # user chats by user_id and query
        chats_queue = Queue()
        chats_process = Thread(target=self.get_user_chats,
                                args=(
                                elastic, env.ELASTIC_CHATS_INDEX, env.ELASTIC_CORE, chats_queue, user_id, title))

        chats_process.start()

        #get results
        documents_by_title = documents_by_title_queue.get()
        public_documents = public_documents_queue.get()
        comments = comments_queue.get()
        chats = chats_queue.get()
        documents = documents_queue.get()

        user_form_content = self.get_user_form_content(elastic, documents, title, env.ELASTIC_FORMS_INDEX, env.ELASTIC_CORE)
        user_projects_by_content = self.get_user_projects_by_forms(elastic, user_form_content, user_id,
                                                              env.ELASTIC_DOCUMENTS_INDEX, env.ELASTIC_CORE)

        projects = np.unique(np.concatenate([user_projects_by_content, documents_by_title, public_documents]))

        return self._get_result(projects, comments, chats)