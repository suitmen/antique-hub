import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <h1>Добро пожаловать в AntiqueHub</h1>
        <p>Платформа для покупки и продажи антиквариата</p>
        <div className="cta-buttons">
          <Link to="/lots" className="btn btn-primary">Найти антиквариат</Link>
          <Link to="/create-lot" className="btn btn-secondary">Продать антиквариат</Link>
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