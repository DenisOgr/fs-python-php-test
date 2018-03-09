<?php

namespace common\components\exceptions;

use Exception;
use yii\base\Model;
use yii\helpers\VarDumper;

/**
 * Class ValidateException
 */
class ValidateException extends Exception
{
    /**
     * @inheritdoc
     */
    public function __construct(Model $model, $code = 500, Exception $previous = null)
    {
        $modelName = $model::className();
        $errors = VarDumper::export($model->errors);
        $message = "Validation errors: modelName: $modelName, errors: $errors. Data: " . VarDumper::export($model->attributes);

        parent::__construct($message, $code, $previous);
    }
}
