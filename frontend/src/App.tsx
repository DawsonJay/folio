import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import GetInTouchPage from './pages/GetInTouchPage';
import MessageSentPage from './pages/MessageSentPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/get-in-touch" element={<GetInTouchPage />} />
        <Route path="/get-in-touch/sent" element={<MessageSentPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
