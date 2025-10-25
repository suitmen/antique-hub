from typing import Union
from .stripe_service import StripePaymentService
from .yookassa_service import YooKassaPaymentService
from ..models import Order

class PaymentProviderFactory:
    @staticmethod
    def get_payment_provider(currency: str) -> Union[StripePaymentService, YooKassaPaymentService]:
        """
        Выбор платежной системы в зависимости от валюты
        
        Args:
            currency: Валюта платежа
            
        Returns:
            Объект платежной системы
        """
        if currency.upper() == "RUB":
            return YooKassaPaymentService()
        else:
            return StripePaymentService()
    
    @staticmethod
    def process_payment(order: Order, amount: float) -> dict:
        """
        Обработка платежа через выбранную платежную систему
        
        Args:
            order: Объект заказа
            amount: Сумма платежа
            
        Returns:
            dict: Результат обработки платежа
        """
        provider = PaymentProviderFactory.get_payment_provider(order.lot.currency)
        
        if isinstance(provider, YooKassaPaymentService):
            # Обработка через ЮKassa
            metadata = {
                "order_id": order.id,
                "item_id": order.lot.id,
                "buyer_id": order.buyer_id
            }
            
            payment = provider.create_payment(
                amount=amount,
                currency=order.lot.currency,
                description=f"Оплата лота {order.lot.title}",
                metadata=metadata
            )
            
            return {
                "provider": "yookassa",
                "payment_id": payment["id"],
                "redirect_url": payment["confirmation"]["confirmation_url"]
            }
        else:
            # Обработка через Stripe
            # Для Stripe сумма указывается в центах/копейках
            amount_in_cents = int(amount * 100)
            metadata = {
                "order_id": order.id,
                "item_id": order.lot.id,
                "buyer_id": order.buyer_id
            }
            
            payment_intent = provider.create_payment_intent(
                amount=amount_in_cents,
                currency=order.lot.currency.lower(),
                metadata=metadata
            )
            
            return {
                "provider": "stripe",
                "payment_id": payment_intent["id"],
                "client_secret": payment_intent["client_secret"]
            }