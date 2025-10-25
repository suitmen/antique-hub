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
    
    return `${price.toLocaleString()} ${currencySymbols[currency] || currency}`;
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
          alt={lot.title} 
          onError={(e) => {
            e.target.src = '/placeholder-image.jpg';
          }}
        />
      </div>
      <div className="lot-content">
        <h3 className="lot-title">
          <Link to={`/lots/${lot.id}`}>{lot.title}</Link>
        </h3>
        <p className="lot-category">{lot.category}</p>
        <p className="lot-era">{lot.era}</p>
        <div className="lot-price">
          {formatPrice(lot.price, lot.currency)}
        </div>
        <div className="lot-seller">
          Продавец: {lot.seller_id}
        </div>
      </div>
    </div>
  );
};

export default LotCard;