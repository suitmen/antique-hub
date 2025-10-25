import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LotCard from '../components/LotCard';
import './LotList.css';

const LotList = () => {
  const [lots, setLots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    category: '',
    era: '',
    minPrice: '',
    maxPrice: '',
    search: ''
  });

  useEffect(() => {
    fetchLots();
  }, []);

  const fetchLots = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/lots/');
      setLots(response.data);
    } catch (err) {
      setError('Ошибка загрузки лотов');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const filteredLots = lots.filter(lot => {
    // Фильтрация по поиску
    if (filters.search && !lot.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    
    // Фильтрация по категории
    if (filters.category && lot.category !== filters.category) {
      return false;
    }
    
    // Фильтрация по эпохе
    if (filters.era && lot.era !== filters.era) {
      return false;
    }
    
    // Фильтрация по цене
    if (filters.minPrice && lot.price < parseFloat(filters.minPrice)) {
      return false;
    }
    
    if (filters.maxPrice && lot.price > parseFloat(filters.maxPrice)) {
      return false;
    }
    
    return true;
  });

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="lot-list">
      <div className="filters">
        <h2>Фильтры</h2>
        <div className="filter-group">
          <input
            type="text"
            name="search"
            placeholder="Поиск по названию"
            value={filters.search}
            onChange={handleFilterChange}
          />
        </div>
        <div className="filter-group">
          <select name="category" value={filters.category} onChange={handleFilterChange}>
            <option value="">Все категории</option>
            <option value="furniture">Мебель</option>
            <option value="jewelry">Ювелирные изделия</option>
            <option value="paintings">Картины</option>
            <option value="sculptures">Скульптуры</option>
            <option value="ceramics">Керамика</option>
            <option value="books">Книги</option>
          </select>
        </div>
        <div className="filter-group">
          <select name="era" value={filters.era} onChange={handleFilterChange}>
            <option value="">Все эпохи</option>
            <option value="18th">XVIII век</option>
            <option value="19th">XIX век</option>
            <option value="20th">XX век</option>
            <option value="ancient">Древний мир</option>
            <option value="medieval">Средневековье</option>
          </select>
        </div>
        <div className="price-filters">
          <input
            type="number"
            name="minPrice"
            placeholder="Мин. цена"
            value={filters.minPrice}
            onChange={handleFilterChange}
          />
          <input
            type="number"
            name="maxPrice"
            placeholder="Макс. цена"
            value={filters.maxPrice}
            onChange={handleFilterChange}
          />
        </div>
      </div>
      
      <div className="lots">
        <h2>Каталог антиквариата</h2>
        {filteredLots.length === 0 ? (
          <p>Лоты не найдены</p>
        ) : (
          <div className="lot-grid">
            {filteredLots.map(lot => (
              <LotCard key={lot.id} lot={lot} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LotList;