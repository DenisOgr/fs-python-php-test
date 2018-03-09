<?php

namespace frontend\components\response\models;

use common\components\exceptions\ValidateException;
use common\components\validators\ArrayValidator;
use Yii;
use yii\base\Model;

/**
 * Class AbstractResponse
 *
 * @property integer $status
 * @property string $message
 * @property array $data
 */
abstract class AbstractResponse extends Model
{
    const STATUS_ERROR = 0;
    const STATUS_SUCCESS = 1;

    /** @var int $status */
    public $status;

    /** @var string $message */
    public $message = '';

    /** @var array $data */
    public $data = [];

    /**
     * @inheritdoc
     */
    public function init()
    {
        parent::init();

        Yii::$app->response->format = $this->responseFormat();
    }

    /**
     * @inheritdoc
     */
    public function rules()
    {
        return [
            [['status'], 'required'],
            [['status'], 'in', 'range' => self::getStatuses()],
            [['message'], 'string'],
            [['data'], ArrayValidator::className()],
        ];
    }

    /**
     * @return string
     */
    abstract protected function responseFormat(): string;

    /**
     * @return array
     */
    protected function getStatuses(): array
    {
        return [
            self::STATUS_ERROR,
            self::STATUS_SUCCESS,
        ];
    }

    /**
     * @return array
     * @throws ValidateException
     */
    public function getResponse(): array
    {
        if (!$this->validate()) {
            throw new ValidateException($this);
        }

        return $this->getAttributes();
    }
}
