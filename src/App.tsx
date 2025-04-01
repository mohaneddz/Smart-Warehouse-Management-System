import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Logs from './pages/AddEnv';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Logs />} />
      </Routes>
    </Router>
  );
};

export default App;
