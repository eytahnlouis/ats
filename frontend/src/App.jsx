import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Accueil from "./components/Accueil";
import Jobs from "./pages/Jobs";
import AdminPage from "./components/AdminPage";
import Upload from "./pages/Upload";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (

    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/" element={<Accueil/>} />
        <Route path="/jobs" element={<Jobs/>} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="*" element={<h1>Page non trouvée</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
