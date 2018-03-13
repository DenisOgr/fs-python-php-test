<?php

namespace frontend\controllers;

use frontend\components\response\models\JsonResponse;
use frontend\models\AbstractSearch;
use yii\web\Controller;
use Exception;
use Yii;

abstract class AbstractApiController extends Controller
{
    /**
     * @return string
     */
    abstract protected function searchClassName(): string;
    /**
     * @return array
     */
    public function actionView()
    {
        /** @var JsonResponse $response */
        $response = Yii::createObject(JsonResponse::class);

            /** @var AbstractSearch $searchModel */
            $searchModel = Yii::createObject($this->searchClassName());
            $response->status = JsonResponse::STATUS_SUCCESS;
            $response->data = $searchModel->search(Yii::$app->request->queryParams);
            return $response->getResponse();

    }
}