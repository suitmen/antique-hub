import React, { useState } from 'react';
import axios from 'axios';
import './CreateLot.css';

const CreateLot = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    currency: 'RUB',
    category: '',
    era: '',
    material: '',
    image_urls: []
  });
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    setImages(files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (images.length > 5) {
      setError('Можно загрузить не более 5 изображений');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess(false);
    
    try {
      // В реальном приложении здесь должна быть загрузка изображений на сервер
      // и получение URL изображений
      const imageUrls = images.map((_, index) => `/uploads/image-${Date.now()}-${index}.jpg`);
      
      const lotData = {
        ...formData,
        price: parseFloat(formData.price),
        image_urls: imageUrls
      };
      
      // Отправка данных лота на сервер
      await axios.post('/api/lots/', lotData);
      
      setSuccess(true);
      setFormData({
        title: '',
        description: '',
        price: '',
        currency: 'RUB',
        category: '',
        era: '',
        material: '',
        image_urls: []
      });
      setImages([]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка создания лота');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-lot">
      <h1>Создать новый лот</h1>
      
      {success && (
        <div className="success-message">
          Лот успешно создан и отправлен на модерацию
        </div>
      )}
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="lot-form">
        <div className="form-group">
          <label htmlFor="title">Название*</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Описание*</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="5"
            required
          />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="price">Цена*</label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              step="0.01"
              min="0"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="currency">Валюта*</label>
            <select
              id="currency"
              name="currency"
              value={formData.currency}
              onChange={handleChange}
              required
            >
              <option value="RUB">RUB (₽)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
            </select>
          </div>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="category">Категория*</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="">Выберите категорию</option>
              <option value="furniture">Мебель</option>
              <option value="jewelry">Ювелирные изделия</option>
              <option value="paintings">Картины</option>
              <option value="sculptures">Скульптуры</option>
              <option value="ceramics">Керамика</option>
              <option value="books">Книги</option>
              <option value="other">Другое</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="era">Эпоха*</label>
            <select
              id="era"
              name="era"
              value={formData.era}
              onChange={handleChange}
              required
            >
              <option value="">Выберите эпоху</option>
              <option value="ancient">Древний мир</option>
              <option value="medieval">Средневековье</option>
              <option value="18th">XVIII век</option>
              <option value="19th">XIX век</option>
              <option value="20th">XX век</option>
              <option value="contemporary">Современное</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="material">Материал</label>
          <input
            type="text"
            id="material"
            name="material"
            value={formData.material}
            onChange={handleChange}
            placeholder="Дерево, металл, керамика и т.д."
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="images">Изображения (не более 5)</label>
          <input
            type="file"
            id="images"
            multiple
            accept="image/*"
            onChange={handleImageChange}
          />
          <div className="image-preview">
            {images.map((file, index) => (
              <div key={index} className="image-preview-item">
                {file.name}
              </div>
            ))}
          </div>
        </div>
        
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? 'Создание...' : 'Создать лот'}
        </button>
      </form>
    </div>
  );
};

export default CreateLot;