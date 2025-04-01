import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Logs from './pages/AddEnv';
import Titlebar from './components/Titlebar';

const App = () => {
  return (
    <Router>
      <Titlebar/>
        <Routes>
        <Route path="/" element={<Logs />} />
    </Routes>
    </Router >
  );
};

export default App;
