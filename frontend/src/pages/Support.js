import React, { useState, useEffect } from 'react';
import api from '../api/config';
import './Support.css';

const Support = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    subject: '',
    message: '',
    category: 'item',
    order_id: null
  });

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      const response = await api.get('/support/tickets');
      setTickets(response.data);
    } catch (err) {
      setError('Ошибка загрузки тикетов');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await api.post('/support/tickets', formData);
      
      // Сброс формы и обновление списка тикетов
      setFormData({
        subject: '',
        message: '',
        category: 'item',
        order_id: null
      });
      setShowForm(false);
      fetchTickets();
    } catch (err) {
      alert('Ошибка создания тикета: ' + (err.response?.data?.detail || 'Неизвестная ошибка'));
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: '#ffc107',
      in_progress: '#17a2b8',
      resolved: '#28a745',
      closed: '#6c757d'
    };
    return colors[status] || '#6c757d';
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="support">
      <div className="support-header">
        <h1>Техническая поддержка</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Отмена' : 'Создать тикет'}
        </button>
      </div>
      
      {showForm && (
        <div className="ticket-form">
          <h2>Создать новый тикет</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="subject">Тема*</label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="category">Категория*</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
              >
                <option value="payment">Оплата</option>
                <option value="item">Предмет</option>
                <option value="account">Аккаунт</option>
                <option value="delivery">Доставка</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="order_id">ID заказа (опционально)</label>
              <input
                type="number"
                id="order_id"
                name="order_id"
                value={formData.order_id}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="message">Сообщение*</label>
              <textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleChange}
                rows="5"
                required
              />
            </div>
            
            <button type="submit" className="btn btn-primary">
              Отправить
            </button>
          </form>
        </div>
      )}
      
      <div className="tickets-list">
        <h2>Мои тикеты</h2>
        {tickets.length === 0 ? (
          <p>У вас пока нет тикетов</p>
        ) : (
          <div className="tickets">
            {tickets.map(ticket => (
              <div key={ticket.id} className="ticket-item">
                <div className="ticket-header">
                  <h3>{ticket.subject}</h3>
                  <span 
                    className="ticket-status"
                    style={{backgroundColor: getStatusColor(ticket.status)}}
                  >
                    {ticket.status}
                  </span>
                </div>
                <p className="ticket-category">Категория: {ticket.category}</p>
                <p className="ticket-message">{ticket.message}</p>
                <p className="ticket-date">
                  Создан: {new Date(ticket.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Support;