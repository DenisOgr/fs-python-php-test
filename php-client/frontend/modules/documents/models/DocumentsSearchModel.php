<?php

namespace frontend\modules\documents\models;

use frontend\models\AbstractSearch;
use yii\helpers\ArrayHelper;
use Exception;

class DocumentsSearchModel extends AbstractSearch
{
    public function search(array $params): array
    {
        // FORMS 1
        /** @var \yii\elasticsearch\Connection $el */
        $el     = \Yii::$app->get('elasticsearch');
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
                                'organization_id' => $params['organization_id']
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $el->post('documents/_search', [], json_encode($config));
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
                                'organization_id' => $params['organization_id']
                            ]
                        ],
                        [
                            'more_like_this' => [
                                'fields' => ['title'],
                                'like'   => [$params['search']],
                                'min_term_freq' => 1,
                                'min_doc_freq' => 1
                            ]
                        ]
                    ]
                ]
            ]
        ];
        $elResult = $el->post('documents/_search', [], json_encode($config));
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
                                'fields' => ['title'],
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
        $elResult = $el->post('form_content/_search', [], json_encode($config));
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
                                'organization_id' => $params['organization_id']
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
        $elResult = $el->post('documents/_search', [], json_encode($config));
        if (empty($elResult)) {
            throw new Exception('Response not eq array');
        }
        $projects2 = $this->get($elResult, 'form_id');
        return array_unique(array_merge($projects1, $projects2));
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
}
