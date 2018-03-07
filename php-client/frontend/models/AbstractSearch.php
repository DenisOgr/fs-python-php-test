<?php

namespace frontend\models;

use yii\base\Model;

abstract class AbstractSearch extends Model
{
    abstract public function search(array $params) : array;
}
