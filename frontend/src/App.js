import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import LotList from './pages/LotList';
import LotDetail from './pages/LotDetail';
import CreateLot from './pages/CreateLot';
import Profile from './pages/Profile';
import Support from './pages/Support';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/lots" element={<LotList />} />
            <Route path="/lots/:id" element={<LotDetail />} />
            <Route path="/create-lot" element={<CreateLot />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/support" element={<Support />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;