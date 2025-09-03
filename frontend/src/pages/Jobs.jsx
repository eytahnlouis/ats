import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();


  useEffect(() => {
    async function fetchJobs() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/cvs/jobs/");
        setJobs(res.data);
        setLoading(false);
      } catch {
        setError("Erreur lors du chargement des jobs");
        setLoading(false);
      }
    }
    fetchJobs();
  }, []);

  if (loading) return <p>Chargement...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (jobs.length === 0) return <p>Aucun job pour l’instant</p>;

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h2>Liste des Jobs</h2>
      {jobs.map((job) => (
        <div
          key={job.id}
          style={{
            border: "1px solid #aaa",
            borderRadius: 8,
            marginBottom: 15,
            padding: 16,
          }}
        >
          <h3>{job.title}</h3>
          <p>
            <b>Description:</b> {job.description}
          </p>
          <p>
            <b>Lieu:</b> {job.location}
          </p>
          <div>
            <b>Mots-clés:</b>
            {job.keywords && job.keywords.length > 0 ? (
              <ul>
                {job.keywords.map((kw, i) => (
                  <li key={i}>
                    {kw.word}
                  </li>
                ))}
              </ul>
            ) : (
              <span> Aucun</span>
            )}
            <button
              style={{
                backgroundColor: "#28a745",
                color: "#fff",
                border: "none",
                padding: "0.5rem 1rem",
                borderRadius: 4,
                cursor: "pointer",
              }}
              onClick={() => { 
                // Logique pour postuler au job
                 navigate(`/upload?job_id=${job.id}`);
              }}
            >
              Postuler
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
