from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, validator


class MethodPaymentValidator(BaseModel):
    methodPayment: Optional[str]

    @validator("methodPayment")
    def validate_method_payment(cls, method: str) -> str:
        if method is None:
            raise ValueError("Method payment is required")
        if method not in MethodPayment.__members__:
            raise ValueError("Invalid method payment")
        if isinstance(method, str):
            method = method.upper()
            method_payment = MethodPayment(method)
            return method_payment.value
        raise ValueError("Invalid method payment")


class ExtractFinancialOutput(BaseModel):
    id: int
    idFinancial: int
    idEmployee: int
    value: int
    createdAt: datetime


class FinancialOutput(BaseModel):
    id: int
    user: int
    methodPayment: Optional[str]
    dtMaturity: Optional[datetime]
    dtFirstPayment: Optional[datetime]
    extractFinancial: List[ExtractFinancialOutput] = []
    createdAt: datetime
    updatedAt: Optional[datetime]


class MethodPayment(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    CASH = "CASH"
    PIX = "PIX"
    BANK_PAYMENT_SLIP = "BANK_PAYMENT_SLIP"


class FinancialRegister(MethodPaymentValidator):
    user: int
    dtMaturity: Optional[datetime]
    dtFirstPayment: Optional[datetime]


class FinancialUpdate(MethodPaymentValidator):
    id: int
    dtMaturity: Optional[datetime]


class ExtractFinancialRegister(MethodPaymentValidator):
    idFinancial: int
    idEmployee: int
    value: int
    dtMaturity: Optional[datetime]


class ExtractFinancialInputInternal(BaseModel):
    idFinancial: int
    idEmployee: int
    value: int
