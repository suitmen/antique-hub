import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <h1>Добро пожаловать в AntiqueHub</h1>
        <p>Платформа для покупки и продажи антиквариата</p>
        <div className="cta-buttons">
          <button className="btn btn-primary">Найти антиквариат</button>
          <button className="btn btn-secondary">Продать антиквариат</button>
        </div>
      </div>
      
      <div className="features">
        <div className="feature">
          <h3>Широкий выбор</h3>
          <p>Тысячи уникальных предметов искусства и антиквариата</p>
        </div>
        <div className="feature">
          <h3>Безопасная оплата</h3>
          <p>Интеграция с ЮKassa и Stripe для безопасных платежей</p>
        </div>
        <div className="feature">
          <h3>Экспертная оценка</h3>
          <p>Профессиональная оценка и аутентификация предметов</p>
        </div>
      </div>
    </div>
  );
};

export default Home;