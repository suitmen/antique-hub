import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Admin.css';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [users, setUsers] = useState([]);
  const [lots, setLots] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const [usersResponse, lotsResponse, ticketsResponse] = await Promise.all([
        axios.get('/api/admin/users/'),
        axios.get('/api/admin/lots/'),
        axios.get('/api/admin/tickets/')
      ]);
      
      setUsers(usersResponse.data);
      setLots(lotsResponse.data);
      setTickets(ticketsResponse.data);
    } catch (err) {
      setError('Ошибка загрузки данных админки');
    } finally {
      setLoading(false);
    }
  };

  const handleUserUpdate = async (userId, updates) => {
    try {
      await axios.put(`/api/admin/users/${userId}`, updates);
      fetchAdminData(); // Обновляем данные после изменения
    } catch (err) {
      alert('Ошибка обновления пользователя: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    }
  };

  const handleLotUpdate = async (lotId, updates) => {
    try {
      await axios.put(`/api/admin/lots/${lotId}`, updates);
      fetchAdminData(); // Обновляем данные после изменения
    } catch (err) {
      alert('Ошибка обновления лота: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    }
  };

  const handleTicketUpdate = async (ticketId, updates) => {
    try {
      await axios.put(`/api/admin/tickets/${ticketId}`, updates);
      fetchAdminData(); // Обновляем данные после изменения
    } catch (err) {
      alert('Ошибка обновления тикета: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    }
  };

  const handleExport = async (type) => {
    try {
      const response = await axios.get(`/api/admin/export/${type}`);
      const blob = new Blob([response.data.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `antiquehub-${type}-${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Ошибка экспорта: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="admin">
      <h1>Админка AntiqueHub</h1>
      
      <div className="admin-tabs">
        <button 
          className={activeTab === 'dashboard' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('dashboard')}
        >
          Дашборд
        </button>
        <button 
          className={activeTab === 'users' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('users')}
        >
          Пользователи ({users.length})
        </button>
        <button 
          className={activeTab === 'lots' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('lots')}
        >
          Лоты ({lots.length})
        </button>
        <button 
          className={activeTab === 'tickets' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('tickets')}
        >
          Тикеты ({tickets.length})
        </button>
        <button 
          className={activeTab === 'export' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('export')}
        >
          Экспорт
        </button>
      </div>
      
      <div className="admin-content">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>Статистика</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Пользователи</h3>
                <p>{users.length}</p>
              </div>
              <div className="stat-card">
                <h3>Лоты</h3>
                <p>{lots.length}</p>
              </div>
              <div className="stat-card">
                <h3>Тикеты</h3>
                <p>{tickets.length}</p>
              </div>
              <div className="stat-card">
                <h3>Продавцы</h3>
                <p>{users.filter(u => u.is_seller).length}</p>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'users' && (
          <div className="users-section">
            <h2>Управление пользователями</h2>
            <div className="users-list">
              {users.map(user => (
                <div key={user.id} className="user-item">
                  <div className="user-info">
                    <h3>{user.email}</h3>
                    <p>ID: {user.id}</p>
                    <p>Роль: {user.role}</p>
                    <p>Продавец: {user.is_seller ? 'Да' : 'Нет'}</p>
                    <p>Верифицирован: {user.verified ? 'Да' : 'Нет'}</p>
                  </div>
                  <div className="user-actions">
                    <button 
                      onClick={() => handleUserUpdate(user.id, { verified: !user.verified })}
                      className="btn btn-secondary"
                    >
                      {user.verified ? 'Отменить верификацию' : 'Верифицировать'}
                    </button>
                    <button 
                      onClick={() => handleUserUpdate(user.id, { role: user.role === 'admin' ? 'buyer' : 'admin' })}
                      className="btn btn-secondary"
                    >
                      {user.role === 'admin' ? 'Сделать пользователем' : 'Сделать админом'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'lots' && (
          <div className="lots-section">
            <h2>Управление лотами</h2>
            <div className="lots-list">
              {lots.map(lot => (
                <div key={lot.id} className="lot-item">
                  <div className="lot-info">
                    <h3>{lot.title}</h3>
                    <p>ID: {lot.id}</p>
                    <p>Цена: {lot.price} {lot.currency}</p>
                    <p>Категория: {lot.category}</p>
                    <p>Статус: {lot.status}</p>
                    <p>Одобрен: {lot.is_approved ? 'Да' : 'Нет'}</p>
                  </div>
                  <div className="lot-actions">
                    <button 
                      onClick={() => handleLotUpdate(lot.id, { is_approved: !lot.is_approved })}
                      className="btn btn-secondary"
                    >
                      {lot.is_approved ? 'Отклонить' : 'Одобрить'}
                    </button>
                    <button 
                      onClick={() => handleLotUpdate(lot.id, { status: lot.status === 'approved' ? 'pending' : 'approved' })}
                      className="btn btn-secondary"
                    >
                      {lot.status === 'approved' ? 'На проверку' : 'Одобрить'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'tickets' && (
          <div className="tickets-section">
            <h2>Управление тикетами</h2>
            <div className="tickets-list">
              {tickets.map(ticket => (
                <div key={ticket.id} className="ticket-item">
                  <div className="ticket-info">
                    <h3>{ticket.subject}</h3>
                    <p>ID: {ticket.id}</p>
                    <p>Пользователь: {ticket.user_id}</p>
                    <p>Категория: {ticket.category}</p>
                    <p>Статус: {ticket.status}</p>
                  </div>
                  <div className="ticket-actions">
                    <button 
                      onClick={() => handleTicketUpdate(ticket.id, { status: 'in_progress' })}
                      className="btn btn-secondary"
                    >
                      В работе
                    </button>
                    <button 
                      onClick={() => handleTicketUpdate(ticket.id, { status: 'resolved' })}
                      className="btn btn-secondary"
                    >
                      Решен
                    </button>
                    <button 
                      onClick={() => handleTicketUpdate(ticket.id, { status: 'closed' })}
                      className="btn btn-secondary"
                    >
                      Закрыт
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'export' && (
          <div className="export-section">
            <h2>Экспорт данных</h2>
            <div className="export-buttons">
              <button onClick={() => handleExport('users')} className="btn btn-primary">
                Экспорт пользователей
              </button>
              <button onClick={() => handleExport('lots')} className="btn btn-primary">
                Экспорт лотов
              </button>
              <button onClick={() => handleExport('orders')} className="btn btn-primary">
                Экспорт заказов
              </button>
              <button onClick={() => handleExport('tickets')} className="btn btn-primary">
                Экспорт тикетов
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Admin;