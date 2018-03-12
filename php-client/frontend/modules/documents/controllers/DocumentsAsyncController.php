<?php

namespace frontend\modules\documents\controllers;

use frontend\controllers\AbstractApiController;
use frontend\modules\documents\models\DocumentsAsyncSearchModel;

class DocumentsAsyncController extends AbstractApiController
{
    protected function searchClassName(): string
    {
        return DocumentsAsyncSearchModel::class;
    }
}
