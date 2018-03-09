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
        try {
            /** @var AbstractSearch $searchModel */
            $searchModel = Yii::createObject($this->searchClassName());
            $response->status = JsonResponse::STATUS_SUCCESS;
            $this->validate();
            $response->data = $searchModel->search(Yii::$app->request->queryParams);
            return $response->getResponse();
        } catch (Exception $exception) {
            $response->status  = JsonResponse::STATUS_ERROR;
            $response->message = $exception->getMessage();
            return $response->getResponse();
        }
    }

    public function validate()
    {
        $requiredKey = ['user_id', 'organization_id', 'search'];
        foreach ($requiredKey as $item) {
            if (!isset(Yii::$app->request->queryParams[$item])) {
                throw new Exception('Not validate key:' . $item);
            }
        }
        return true;
    }
}