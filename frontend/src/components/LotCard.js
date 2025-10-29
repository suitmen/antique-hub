import React from 'react';
import { Link } from 'react-router-dom';
import './LotCard.css';

const LotCard = ({ lot }) => {
  // Функция для форматирования цены
  const formatPrice = (price, currency) => {
    const currencySymbols = {
      'RUB': '₽',
      'USD': '$',
      'EUR': '€'
    };
    
    return `${price?.toLocaleString() || '0'} ${currencySymbols[currency] || currency || 'RUB'}`;
  };

  // Функция для получения первого изображения
  const getFirstImage = (imageUrls) => {
    if (imageUrls && imageUrls.length > 0) {
      return imageUrls[0];
    }
    return '/placeholder-image.jpg'; // Путь к изображению-заглушке
  };

  return (
    <div className="lot-card">
      <div className="lot-image">
        <img 
          src={getFirstImage(lot.image_urls)} 
          alt={lot.title || 'Лот'} 
          onError={(e) => {
            e.target.src = '/placeholder-image.jpg';
          }}
        />
      </div>
      <div className="lot-content">
        <h3 className="lot-title">
          <Link to={`/lots/${lot.id}`}>{lot.title || 'Без названия'}</Link>
        </h3>
        <p className="lot-category">{lot.category || 'Не указано'}</p>
        <p className="lot-era">{lot.era || 'Не указано'}</p>
        <div className="lot-price">
          {formatPrice(lot.price, lot.currency)}
        </div>
        <div className="lot-seller">
          Продавец: ID {lot.seller_id || 'Не указано'}
        </div>
      </div>
    </div>
  );
};

export default LotCard;