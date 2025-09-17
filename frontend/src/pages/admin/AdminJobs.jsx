import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

export default function AdminJobs() {
  const [jobs, setJobs] = useState([]);
  const [err, setErr] = useState("");

  const fetchJobs = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/cvs/jobs/");
      setJobs(res.data);
    } catch (e) {
      setErr(e.message);
    }
  };

  const toggleJob = async (id) => {
    try {
      const token = localStorage.getItem("access_token"); // stocke ton access token après login
      await axios.post(
        `http://127.0.0.1:8000/api/cvs/my-candidates/${id}/`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      fetchJobs();
    } catch (e) {
      alert("Erreur toggle: " + (e.response?.data || e.message));
    }
  };

  const delJob = async (id) => {
    if (!confirm("Supprimer ce job ?")) return;
    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(`http://127.0.0.1:8000/api/cvs/jobs/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchJobs();
    } catch (e) {
      alert("Erreur suppression: " + (e.response?.data || e.message));
    }
  };



  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div>
      <h3>Jobs</h3>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <table
        width="100%"
        border="1"
        cellPadding="8"
        style={{ borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>Titre</th>
            <th>Lieu</th>
            <th>Actif</th>
            <th>Créé</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((j) => (
            <tr key={j.id}>
              <td>
                <Link to={`/admin/jobs/${j.id}/candidates`}>{j.title}</Link>
              </td>
              <td>{j.location || "-"}</td>
              <td>{j.is_active ? "✅" : "⛔️"}</td>
              <td>{new Date(j.created_at).toLocaleString()}</td>
              <td style={{ display: "flex", gap: 8 }}>
                <Link to={`/admin/jobs/${j.id}/candidates`}>👥</Link>
                <Link to={`/admin/jobs/${j.id}/edit`}>✏️</Link>
                <button onClick={() => toggleJob(j.id)}>On/Off</button>
                <button
                  onClick={() => delJob(j.id)}
                  style={{ color: "crimson" }}
                >
                  Suppr
                </button>
              </td>
            </tr>
          ))}
          {jobs.length === 0 && (
            <tr>
              <td colSpan="5">Aucun job pour l’instant</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
