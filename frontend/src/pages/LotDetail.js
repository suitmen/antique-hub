import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/config';
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
      const response = await api.get(`/lots/${id}`);
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
      const response = await api.post('/orders/', {
        item_id: parseInt(id)
      });
      
      // Инициализация платежа
      const paymentResponse = await api.post('/payments/init', {
        item_id: parseInt(id),
        currency: lot.currency || 'RUB'
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
    
    return `${price?.toLocaleString() || '0'} ${currencySymbols[currency] || currency || 'RUB'}`;
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!lot) return <div className="error">Лот не найден</div>;

  return (
    <div className="lot-detail">
      <div className="lot-images">
        {lot.image_urls && lot.image_urls.length > 0 ? (
          lot.image_urls.map((url, index) => (
            <img key={index} src={url} alt={`${lot.title || 'Лот'} ${index + 1}`} />
          ))
        ) : (
          <img src="/placeholder-image.jpg" alt={lot.title || 'Лот'} />
        )}
      </div>
      
      <div className="lot-info">
        <h1>{lot.title || 'Без названия'}</h1>
        <div className="lot-meta">
          <span className="category">{lot.category || 'Не указано'}</span>
          <span className="era">{lot.era || 'Не указано'}</span>
          <span className="material">{lot.material || 'Не указано'}</span>
        </div>
        
        <div className="lot-price">
          {formatPrice(lot.price, lot.currency)}
        </div>
        
        <div className="lot-description">
          <h2>Описание</h2>
          <p>{lot.description || 'Описание не указано'}</p>
        </div>
        
        <div className="lot-seller">
          <h3>Продавец</h3>
          <p>ID продавца: {lot.seller_id || 'Не указано'}</p>
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