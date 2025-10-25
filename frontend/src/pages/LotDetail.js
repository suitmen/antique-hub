import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './LotDetail.css';

const LotDetail = () => {
  const { id } = useParams();
  const [lot, setLot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [orderLoading, setOrderLoading] = useState(false);

  useEffect(() => {
    fetchLot();
  }, [id]);

  const fetchLot = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/lots/${id}`);
      setLot(response.data);
    } catch (err) {
      setError('Ошибка загрузки лота');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOrder = async () => {
    try {
      setOrderLoading(true);
      
      // Создание заказа
      const response = await axios.post('/api/orders/', {
        item_id: parseInt(id)
      });
      
      // Инициализация платежа
      const paymentResponse = await axios.post('/api/payments/init', {
        item_id: parseInt(id),
        currency: lot.currency
      });
      
      // Перенаправление на страницу оплаты
      if (paymentResponse.data.redirect_url) {
        window.location.href = paymentResponse.data.redirect_url;
      } else {
        alert('Заказ создан. Для завершения оплаты следуйте инструкциям.');
      }
    } catch (err) {
      alert('Ошибка создания заказа: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    } finally {
      setOrderLoading(false);
    }
  };

  // Функция для форматирования цены
  const formatPrice = (price, currency) => {
    const currencySymbols = {
      'RUB': '₽',
      'USD': '$',
      'EUR': '€'
    };
    
    return `${price.toLocaleString()} ${currencySymbols[currency] || currency}`;
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!lot) return <div className="error">Лот не найден</div>;

  return (
    <div className="lot-detail">
      <div className="lot-images">
        {lot.image_urls && lot.image_urls.length > 0 ? (
          lot.image_urls.map((url, index) => (
            <img key={index} src={url} alt={`${lot.title} ${index + 1}`} />
          ))
        ) : (
          <img src="/placeholder-image.jpg" alt={lot.title} />
        )}
      </div>
      
      <div className="lot-info">
        <h1>{lot.title}</h1>
        <div className="lot-meta">
          <span className="category">{lot.category}</span>
          <span className="era">{lot.era}</span>
          <span className="material">{lot.material}</span>
        </div>
        
        <div className="lot-price">
          {formatPrice(lot.price, lot.currency)}
        </div>
        
        <div className="lot-description">
          <h2>Описание</h2>
          <p>{lot.description}</p>
        </div>
        
        <div className="lot-seller">
          <h3>Продавец</h3>
          <p>ID продавца: {lot.seller_id}</p>
        </div>
        
        <button 
          className="btn btn-primary"
          onClick={handleCreateOrder}
          disabled={orderLoading}
        >
          {orderLoading ? 'Создание заказа...' : 'Купить'}
        </button>
      </div>
    </div>
  );
};

export default LotDetail;