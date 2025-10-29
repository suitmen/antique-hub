import React, { useState, useEffect } from 'react';
import api from '../api/config';
import './Profile.css';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [lots, setLots] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      console.log('Fetching user data...');
      console.log('Token in localStorage:', localStorage.getItem('token'));
      
      // Сначала тестируем простой endpoint
      try {
        const testResponse = await api.get('/test-token');
        console.log('Test token response:', testResponse.data);
      } catch (testErr) {
        console.error('Test token error:', testErr);
      }
      
      // Получение данных пользователя
      const userResponse = await api.get('/users/me');
      console.log('User response:', userResponse.data);
      setUser(userResponse.data);
      
      // Получение лотов пользователя
      const lotsResponse = await api.get(`/lots/?seller_id=${userResponse.data.id}`);
      setLots(lotsResponse.data);
      
      // Получение заказов пользователя
      const ordersResponse = await api.get(`/orders/?user_id=${userResponse.data.id}`);
      setOrders(ordersResponse.data);
    } catch (err) {
      console.error('Error fetching user data:', err);
      setError('Ошибка загрузки данных профиля');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!user) return <div className="error">Пользователь не найден</div>;

  return (
    <div className="profile">
      <h1>Профиль пользователя</h1>
      
      <div className="tabs">
        <button 
          className={activeTab === 'profile' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('profile')}
        >
          Профиль
        </button>
        <button 
          className={activeTab === 'lots' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('lots')}
        >
          Мои лоты ({lots.length})
        </button>
        <button 
          className={activeTab === 'orders' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('orders')}
        >
          Мои заказы ({orders.length})
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'profile' && (
          <div className="profile-info">
            <div className="info-group">
              <label>Email:</label>
              <span>{user.email}</span>
            </div>
            <div className="info-group">
              <label>Тип аккаунта:</label>
              <span>{user.is_seller ? 'Продавец' : 'Покупатель'}</span>
            </div>
            <div className="info-group">
              <label>Статус верификации:</label>
              <span>{user.verified ? 'Верифицирован' : 'Не верифицирован'}</span>
            </div>
            <div className="info-group">
              <label>Дата регистрации:</label>
              <span>{new Date(user.created_at).toLocaleDateString()}</span>
            </div>
            
            {!user.is_seller && (
              <button className="btn btn-secondary">
                Стать продавцом
              </button>
            )}
          </div>
        )}
        
        {activeTab === 'lots' && (
          <div className="lots-section">
            <h2>Мои лоты</h2>
            {lots.length === 0 ? (
              <p>У вас пока нет лотов</p>
            ) : (
              <div className="lots-list">
                {lots.map(lot => (
                  <div key={lot.id} className="lot-item">
                    <h3>{lot.title}</h3>
                    <p>Статус: {lot.status}</p>
                    <p>Цена: {lot.price} {lot.currency}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'orders' && (
          <div className="orders-section">
            <h2>Мои заказы</h2>
            {orders.length === 0 ? (
              <p>У вас пока нет заказов</p>
            ) : (
              <div className="orders-list">
                {orders.map(order => (
                  <div key={order.id} className="order-item">
                    <h3>Заказ #{order.id}</h3>
                    <p>Статус: {order.status}</p>
                    <p>Дата: {new Date(order.created_at).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;