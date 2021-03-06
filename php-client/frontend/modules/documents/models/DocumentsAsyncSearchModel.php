<?php

namespace frontend\modules\documents\models;

use Faker\Factory;
use frontend\models\AbstractSearch;
use GuzzleHttp\Client;
use GuzzleHttp\Promise\PromiseInterface;
use function GuzzleHttp\Promise\unwrap;
use yii\helpers\ArrayHelper;
use Exception;

class DocumentsAsyncSearchModel extends AbstractSearch
{
    /** @var Client $cli */
    protected $cli;

    /** @var Factory $faker */
    protected $faker;

    /** @var ProviderFake $provider */
    protected $provider;

    protected $promise = [];

    public function init()
    {
        $this->cli = new Client([
            // Base URI is used with relative requests
            'base_uri' => 'elasticsearch:9200',
            // You can set any number of default request options.
            'headers'  => ['content-type' => 'application/json', 'Accept' => 'application/json'],
        ]);

        $this->provider = new ProviderFake();

        $this->faker = Factory::create();

    }

    public function search(array $params): array
    {
        $count        = 0;
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
        $this->promise['forms_1'] = $this->cli->postAsync('documents/_search', ['body' => json_encode($config)]);
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
        $this->promise['projects_1'] = $this->cli->postAsync('documents/_search', ['body' => json_encode($config)]);

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
        $this->promise['comments'] = $this->cli->postAsync('comments/_search', ['body' => json_encode($config)]);

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
        $this->promise['chats'] = $this->cli->postAsync('chats/_search', ['body' => json_encode($config)]);

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
        $this->promise['projects_3'] = $this->cli->postAsync('documents/_search', ['body' => json_encode($config)]);

        $results = unwrap($this->promise);
        $count++;
        $results['forms_1']     = \GuzzleHttp\json_decode($results['forms_1']->getBody()->getContents(), true);
        $results['projects_1']  = \GuzzleHttp\json_decode($results['projects_1']->getBody()->getContents(), true);
        $results['projects_3']  = \GuzzleHttp\json_decode($results['projects_3']->getBody()->getContents(), true);
        $results['comments']    = \GuzzleHttp\json_decode($results['comments']->getBody()->getContents(), true);
        $results['chats']       = \GuzzleHttp\json_decode($results['chats']->getBody()->getContents(), true);

        $forms1    = $this->get($results['forms_1'], 'form_id');
        $projects1 = $this->get($results['projects_1'], 'project_id');
        $projects3 = $this->get($results['projects_3'], 'project_id');
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
        $count++;
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
        $count++;
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $projects2 = $this->get($elResult, 'form_id');

        $done = array_unique(array_merge($projects1, $projects2));
        $done = array_unique(array_merge($done, $projects3));
        return [
            'projects' => $done,
            'comments' => $results['comments'],
            'chats'    => $results['chats'],
            'query'    => [
                'user_id'           => $userId,
                'organisation_id'   => $organisation,
                'search'            => $search,
                'count_query'       => $count,
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
        $r = $this->cli->post($url, ['body' => json_encode($config)]);
        return \GuzzleHttp\json_decode($r->getBody()->getContents(), true);
    }
}
