import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import GetInTouchPage from './pages/GetInTouchPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/get-in-touch" element={<GetInTouchPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
