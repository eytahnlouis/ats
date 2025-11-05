import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

export default function AdminJobCandidates() {
  const { id } = useParams(); // job UUID
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/api/cvs/jobs/${id}/candidates/`,
          { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } }
        );
        setRows(res.data);
      } catch (e) {
        setErr(e.message);
      }
    })();
  }, [id]);

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h3>Candidats du job</h3>
        <Link to="/admin">← Retour Jobs</Link>
      </div>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <table
        width="100%"
        border="1"
        cellPadding="8"
        style={{ borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>Nom</th>
            <th>Email</th>
            <th>Téléphone</th>
            <th>Score</th>
            <th>Reçu</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan="5">Aucun candidat</td>
            </tr>
          ) : (
            rows.map((c) => (
              <tr key={c.id}>
                <td>{c.name}</td>
                <td>{c.email}</td>
                <td>{c.phone}</td>
                <td>
                  <b>{c.score}</b>
                </td>
                <td>{new Date(c.created_at).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
