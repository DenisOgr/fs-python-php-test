<?php
namespace frontend\controllers;

use Yii;
use frontend\components\response\models\JsonResponse;
use yii\web\Controller;

/**
 * Site controller
 */
class SiteController extends Controller
{
    public function actionError()
    {
        /** @var JsonResponse $response */
        $response          = Yii::createObject(JsonResponse::class);
        $response->status  = JsonResponse::STATUS_ERROR;
        $response->message = Yii::$app->getErrorHandler()->exception->getMessage();
        return $response->getResponse();
    }

    public function actionIndex()
    {
        /** @var JsonResponse $response */
        $response          = Yii::createObject(JsonResponse::class);
        $response->status  = JsonResponse::STATUS_SUCCESS;
        $response->message = 'Hi';
        return $response->getResponse();
    }
}
