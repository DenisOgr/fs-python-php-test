<?php
namespace frontend\components\response\models;
use yii\web\Response;
/**
 * Class JsonResponse
 */
class JsonResponse extends AbstractResponse
{
    /**
     * @inheritdoc
     */
    protected function responseFormat(): string
    {
        return Response::FORMAT_JSON;
    }
}