import requests
import uuid
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

class YooKassaPaymentService:
    def __init__(self):
        self.shop_id = os.getenv("YOOKASSA_SHOP_ID")
        self.secret_key = os.getenv("YOOKASSA_SECRET_KEY")
        self.base_url = "https://api.yookassa.ru/v3"
        
    def create_payment(self, amount: float, currency: str = "RUB", description: str = "", 
                      metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Создание платежа через ЮKassa
        
        Args:
            amount: Сумма платежа
            currency: Валюта (по умолчанию RUB)
            description: Описание платежа
            metadata: Дополнительные данные
            
        Returns:
            Dict: Данные платежа
        """
        try:
            payment_data = {
                "amount": {
                    "value": str(amount),
                    "currency": currency
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": os.getenv("RETURN_URL", "http://localhost:3000/payment-success")
                },
                "description": description,
                "metadata": metadata or {},
                "capture": True
            }
            
            response = requests.post(
                f"{self.base_url}/payments",
                json=payment_data,
                auth=(self.shop_id, self.secret_key),
                headers={"Idempotence-Key": str(uuid.uuid4())}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"YooKassa payment error: {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"YooKassa payment error: {str(e)}")

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Получение статуса платежа
        
        Args:
            payment_id: ID платежа
            
        Returns:
            Dict: Данные платежа
        """
        try:
            response = requests.get(
                f"{self.base_url}/payments/{payment_id}",
                auth=(self.shop_id, self.secret_key)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"YooKassa payment status error: {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"YooKassa payment status error: {str(e)}")