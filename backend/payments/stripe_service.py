import stripe
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Инициализация Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class StripePaymentService:
    @staticmethod
    def create_payment_intent(amount: int, currency: str = "rub", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создание платежного намерения в Stripe
        
        Args:
            amount: Сумма в центах/копейках
            currency: Валюта (по умолчанию RUB)
            metadata: Дополнительные данные
            
        Returns:
            Dict: Данные платежного намерения
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {}
            )
            return {
                "id": intent.id,
                "client_secret": intent.client_secret,
                "status": intent.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe payment error: {str(e)}")

    @staticmethod
    def confirm_payment_intent(payment_intent_id: str) -> Dict[str, Any]:
        """
        Подтверждение платежного намерения
        
        Args:
            payment_intent_id: ID платежного намерения
            
        Returns:
            Dict: Данные подтвержденного платежа
        """
        try:
            intent = stripe.PaymentIntent.confirm(payment_intent_id)
            return {
                "id": intent.id,
                "status": intent.status,
                "amount": intent.amount
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe payment confirmation error: {str(e)}")