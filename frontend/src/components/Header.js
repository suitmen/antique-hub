import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">
          AntiqueHub
        </Link>
        <nav className="nav">
          <Link to="/lots">Каталог</Link>
          <Link to="/create-lot">Создать лот</Link>
          <Link to="/support">Поддержка</Link>
          <Link to="/profile">Профиль</Link>
          <Link to="/admin">Админка</Link>
          <Link to="/login">Вход</Link>
          <Link to="/register">Регистрация</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;