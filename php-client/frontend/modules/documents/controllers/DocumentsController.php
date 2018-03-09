<?php

namespace frontend\modules\documents\controllers;

use frontend\controllers\AbstractApiController;
use frontend\modules\documents\models\DocumentsSearchModel;

class DocumentsController extends AbstractApiController
{
    protected function searchClassName(): string
    {
        return DocumentsSearchModel::class;
    }
}
