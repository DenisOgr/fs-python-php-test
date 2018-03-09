<?php

namespace common\components\validators;

use yii\validators\Validator;

/**
 * Class ArrayValidator
 */
class ArrayValidator extends Validator
{
    /**
     * @inheritdoc
     */
    public function validateAttribute($model, $attribute)
    {
        if (!is_array($model->$attribute)) {
            $model->addError($attribute, 'Should be array.');
        }
    }
}
