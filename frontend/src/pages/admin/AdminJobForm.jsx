import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import ChecklistJob from "../../components/ChecklistJob";
export default function AdminJobForm() {
  const { id } = useParams(); // si présent → mode edit
  const nav = useNavigate();
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [err, setErr] = useState("");
  const [keywords, setKeywords] = useState([]); // existant : input CSV
  const [checklistKeywords, setChecklistKeywords] = useState([]); // reçu depuis ChecklistJob

  useEffect(() => {
    const load = async () => {
      if (!id) return;
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/cvs/jobs/`);
        const job = res.data.find((j) => j.id === id);
        if (job) {
          setTitle(job.title);
          setLocation(job.location || "");
          setDescription(job.description || "");
          setKeywords(
            Array.isArray(job.keywords) ? job.keywords : job.keywords || []
          );
        }
      } catch (e) {
        setErr(e.message);
      }
    };
    load();
  }, [id]);

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem("refresh_token"); // clé attendue pour le refresh token
    if (!refresh) throw new Error("no_refresh_token");
    const res = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
      refresh,
    });
    const newAccess = res.data.access;
    if (!newAccess) throw new Error("refresh_failed");
    localStorage.setItem("refresh_token", newAccess);
    return newAccess;
  };
  async function save(e) {
    e.preventDefault();
    setErr("");
    const token = localStorage.getItem("access_token");
    // Ensure keywordsArray is always an array of trimmed strings
    const keywordsArray =
      checklistKeywords && checklistKeywords.length > 0
        ? checklistKeywords.map((k) => ({
            word: String(k.word || "").trim(),
            weight: Number.isFinite(+k.weight) ? +k.weight : 1.0,
          }))
        : Array.isArray(keywords)
        ? keywords.map((w) => ({ word: String(w || "").trim(), weight: 1.0 }))
        : [];

    try {
      if (id) {
        await axios.put(
          `http://127.0.0.1:8000/api/cvs/jobs/${id}/`,
          {
            title,
            location,
            description,
            keywords: keywordsArray,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      } else {
        await axios.post(
          `http://127.0.0.1:8000/api/cvs/jobs/create/`,
          {
            title,
            location,
            description,
            keywords: keywordsArray,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
      nav("/admin");
    } catch (e) {
      // si token invalide, tenter un refresh puis réessayer une fois
      const apiCode = e.response?.data?.code;
      if (apiCode === "token_not_valid" || e.response?.status === 401) {
        try {
          const newAccess = await refreshAccessToken();
          // réessayer la requête avec le nouveau token
          if (id) {
            await axios.put(
              `http://127.0.0.1:8000/api/cvs/jobs/${id}/`,
              { title, location, description, keywords: keywordsArray },
              { headers: { Authorization: `Bearer ${newAccess}` } }
            );
          } else {
            await axios.post(
              `http://127.0.0.1:8000/api/cvs/jobs/create/`,
              { title, location, description, keywords: keywordsArray },
              { headers: { Authorization: `Bearer ${newAccess}` } }
            );
          }
          return;
        } catch (refreshErr) {
          setErr("Session expirée, veuillez vous reconnecter.");
          nav("/login"); // adapter route login si besoin
          return refreshErr;
        }
      }
      setErr(e.response?.data ? JSON.stringify(e.response.data) : e.message);
    }
  }

  return (
    <div>
      <h3>{id ? "Éditer un job" : "Créer un job"}</h3>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <form onSubmit={save} style={{ display: "grid", gap: 12 }}>
        <input
          placeholder="Titre"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          placeholder="Lieu"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <textarea
          placeholder="Description"
          rows={6}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <ChecklistJob onChange={setChecklistKeywords} />
        <button type="submit">{id ? "Mettre à jour" : "Créer"}</button>
      </form>
    </div>
  );
}