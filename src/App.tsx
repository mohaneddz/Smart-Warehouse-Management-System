import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import StockManager from './pages/StockManager';
import Logs from './pages/Logs';
import Settings from './pages/Settings';
// import WarehouseLayout from './pages/WarehouseLayout';
import Navbar from './components/Navbar';
import Titlebar from './components/Titlebar';
// import Titlebar from './components/Titlebar';

function App() {
  return (
    <Router>
      <Titlebar />
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        {/* <Route path="/warehouse-layout" element={<WarehouseLayout />} /> */}
        <Route path="/stock-manager" element={<StockManager />} />
        <Route path="/logs" element={<Logs />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
