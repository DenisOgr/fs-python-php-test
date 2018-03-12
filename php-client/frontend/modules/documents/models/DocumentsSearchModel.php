<?php

namespace frontend\modules\documents\models;

use frontend\models\AbstractSearch;
use GuzzleHttp\Client;
use yii\helpers\ArrayHelper;
use Exception;

class DocumentsSearchModel extends AbstractSearch
{
    public function search(array $params): array
    {
        // FORMS 1
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $params['user_id']
                            ],
                        ],
                        [
                            'match' => [
                                'organisation_id' => $params['organization_id']
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $this->request('documents/_search', $config);
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $forms1 = $this->get($elResult, 'form_id');
        // PROJECTS 1
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $params['user_id']
                            ],
                        ],
                        [
                            'match' => [
                                'organisation_id' => $params['organization_id']
                            ]
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['file_name'],
                                'like'   => [$params['search']],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $this->request('documents/_search', $config);
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $projects1 = $this->get($elResult, 'project_id');

        // FORMS 2

        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'more_like_this' => [
                                'fields' => ['description'],
                                'like'   => [$params['search']],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ],
                        [
                            'terms' =>  [
                                'form_id' => $forms1
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $this->request('form_contents/_search', $config);
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $forms2 = $this->get($elResult, 'form_id');
        // Projects 2
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $params['user_id']
                            ],
                        ],
                        [
                            'match' => [
                                'organisation_id' => $params['organization_id']
                            ]
                        ],
                        [
                            'terms' =>  [
                                'form_id' => $forms2
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $this->request('documents/_search', $config);
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $projects2 = $this->get($elResult, 'form_id');
        // Comments
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $params['user_id']
                            ],
                        ],
                        [
                            'match' => [
                                'organisation_id' => $params['organization_id']
                            ]
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['comment'],
                                'like'   => [$params['search']],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $comments = $this->request('comments/_search', $config);
        if (empty($comments)) {
            throw new Exception('Response not eq array');
        }
        return [
            'projects' => array_unique(array_merge($projects1, $projects2)),
            'comments' => $comments['hits']
        ];
    }

    protected function get(array $data, string $field) : array
    {
        $data = ArrayHelper::getValue($data, 'hits.hits');
        if (empty($data)) {
            return [];
        }
        return array_filter(ArrayHelper::getColumn($data, function ($element) use ($field) {
             return ArrayHelper::getValue($element, '_source.' . $field);
        }));
    }

    public function request(string $url, array $config): array
    {
        $cli = new Client([
            // Base URI is used with relative requests
            'base_uri' => 'elasticsearch:9200',
            // You can set any number of default request options.
            'headers'  => ['content-type' => 'application/json', 'Accept' => 'application/json'],
        ]);
        $r = $cli->post($url, ['body' => json_encode($config)]);
        return \GuzzleHttp\json_decode($r->getBody()->getContents(), true);
    }
}
