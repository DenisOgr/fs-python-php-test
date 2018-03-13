<?php

namespace frontend\modules\documents\models;

use Faker\Factory;
use frontend\models\AbstractSearch;
use GuzzleHttp\Client;
use yii\helpers\ArrayHelper;
use Exception;

class DocumentsSearchModel extends AbstractSearch
{
    protected $faker;
    /** @var  ProviderFake */
    protected $provider;

    public function init()
    {
        $this->provider = new ProviderFake();

        $this->faker = Factory::create();
    }


    public function search(array $params): array
    {
        $search       = (empty($params['search']))? $this->provider->seed_fake_words() . ' ' . $this->faker->word : $params['search'];
        $userId       = (empty($params['user_id']))? rand(0, \Yii::$app->params['random']['user_id']) : $params['user_id'];
        $organisation = (empty($params['organisation_id'])) ? rand(0, \Yii::$app->params['random']['organisation_id']) : $params['organisation_id'];
        // FORMS 1
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $userId
                            ],
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
                                'user_id' => $userId
                            ],
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['file_name'],
                                'like'   => [$search],
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
                                'like'   => [$search],
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
                                'user_id' => $userId
                            ],
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
                                'user_id' => $userId
                            ],
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['comment'],
                                'like'   => [$search],
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
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'user_id' => $userId
                            ],
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['comment'],
                                'like'   => [$search],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $chats = $this->request('chats/_search', $config);
        if (empty($comments)) {
            throw new Exception('Response not eq array');
        }
        // Projects 3
        $config = [
            'query' => [
                'bool' => [
                    'must' => [
                        [
                            'match' => [
                                'organisation_id' => $organisation
                            ],
                        ],
                        [
                            'match' => [
                                'is_public' => true
                            ],
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['file_name'],
                                'like'   => [$search],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ]
                    ],
                    'must_not' => [
                        [
                            'term' => [
                                'user_id' => $userId
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
        $projects3 = $this->get($elResult, 'project_id');

        $done = array_unique(array_merge($projects1, $projects2));
        $done = array_unique(array_merge($done, $projects3));

        return [
            'projects' => $done,
            'comments' => $comments['hits'],
            'chats'    => $chats['hits'],
            'query'    => [
                'user_id'           => $userId,
                'organisation_id'   => $organisation,
                'search'            => $search
            ]
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
