import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Accueil from "./components/Accueil";
import Jobs from "./pages/Jobs";
import AdminLayout from "./pages/admin/AdminLayout";
import AdminJobs from "./pages/admin/AdminJobs";
import AdminJobForm from "./pages/admin/AdminJobForm";
import AdminJobCandidates from "./pages/admin/AdminJobCandidates";
import Upload from "./pages/Upload";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Accueil />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="*" element={<h1>Page non trouvée</h1>} />
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminJobs />} />
          <Route path="jobs/new" element={<AdminJobForm />} />
          <Route path="jobs/:id/edit" element={<AdminJobForm />} />
          <Route path="jobs/:id/candidates" element={<AdminJobCandidates />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
