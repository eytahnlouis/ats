import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useSearchParams } from "react-router-dom";
import { useMemo } from "react";

export default function Upload() {
  const inputStyle = {
    backgroundColor: "#f0f0f0",
    border: "1px solid #ccc",
    padding: "10px",
    borderRadius: "40em",
  };
  // State variables to manage file upload and personal information
  const [searchParams] = useSearchParams();
  const jobId = useMemo(() => {
    const id = searchParams.get("job_id");
    if (!id) {
      console.warn("Paramètre 'job' manquant dans l'URL");
    }
    return id || "";
  }, [searchParams]); // Job ID from URL
  const jobTitle = searchParams.get("title") || "Le poste";
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [telephone, setTelephone] = useState("");
  // Style for the input fields

  const handleFileChange = (e) => {
    // Gestion du changement de fichier
    setFile(e.target.files[0]);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation côté client
    if (!file) {
      setError("Veuillez sélectionner un fichier CV");
      return;
    }
    const maxSize = 3 * 1024 * 1024;
    if (file.size > maxSize) {
      setError("Fichier trop volumineux (max 3MB)");
      e.target.value = "";
      return;
    }

    // Validation extension
    const allowedExtensions = ["pdf", "doc", "docx"];
    const ext = file.name.split(".").pop().toLowerCase();
    if (!allowedExtensions.includes(ext)) {
      setError(
        `Format non supporté. Utilisez: ${allowedExtensions.join(", ")}`
      );
      e.target.value = "";
      return;
    }
    if (!jobId) {
      setError(
        "Aucune offre sélectionnée. Veuillez choisir une offre d'emploi."
      );
      return;
    }

    const formData = new FormData();
    formData.append("name", nom);
    formData.append("email", email);
    formData.append("phone", telephone);
    formData.append("job", jobId);

    setLoading(true);
    let candidateId = null;

    // Premier appel : créer le candidat
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/cvs/upload/",
        formData
      );

      candidateId = response.data.candidate.id; // Récupérer l'ID du candidat créé
    } catch (error) {
      console.error("Erreur upload:", error.response?.data || error.message);
      setError(error.response?.data?.detail || "Erreur lors de l'upload");
      setLoading(false);
      return; // Arrêter si le premier appel échoue
    }

    // Deuxième appel : uploader le CV avec l'ID du candidat
    const resumeFormData = new FormData();
    resumeFormData.append("file", file);


    try {
      const resumeResponse = await axios.post(
        `http://127.0.0.1:8000/api/cvs/upload-resume/${candidateId}/`,
        resumeFormData
      );
      console.log("Resume upload réussi:", resumeResponse.data);
      // Redirection après succès complet
      navigate("/jobs");
    } catch (error) {
      switch (error.response?.status) {
        case 400:
          setError("Données de CV invalides.");
          break;
        case 413:
          setError("Le fichier de CV est trop volumineux.");
          break;
        case 415:
          setError("Format de fichier de CV non supporté.");
          break;
        case 404:
          setError("Point de terminaison d'upload de CV introuvable.");
          break;
        case 500:
          setError("Erreur serveur lors de l'upload du CV.");
          break;
        default:
          setError("Erreur inconnue lors de l'upload du CV.");
      }
      console.error("Erreur upload CV:", error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div
      style={{
        maxWidth: 600,
        margin: "2rem auto",
        padding: "2rem",
        borderRadius: "8px",
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
      }}
    >
      <h2>Uploader un CV</h2>
      <h4>Pour postuler au poste: {jobTitle}</h4>
      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column" }}
      >
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
          required
        />
        <label htmlFor="file" style={{ display: "block", marginTop: "1rem" }}>
          Sélectionner un fichier (PDF, DOC, DOCX)
        </label>
        <br />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button
          type="submit"
          disabled={loading}
          style={{
            backgroundColor: "#4CAF50",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "40em",
            cursor: "pointer",
            fontSize: "16px",
            marginTop: "1rem",
          }}
        >
          {loading ? "Chargement..." : "Télécharger"}
        </button>
        <h3>Informations personnelles</h3>
        <label htmlFor="nom">Nom et prenom *</label>
        <input
          type="text"
          id="nom"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          name="nom"
          style={inputStyle}
          placeholder="Entrez votre nom et prénom"
          required
        />

        <br />
        <label htmlFor="email">Email*</label>
        <input
          type="email"
          id="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={inputStyle}
          placeholder="Entrez votre email"
          required
        />
        <br />
        <label htmlFor="telephone">Téléphone*</label>
        <input
          type="tel"
          id="telephone"
          name="telephone"
          value={telephone}
          onChange={(e) => setTelephone(e.target.value)}
          style={inputStyle}
          placeholder="Entrez votre numéro de téléphone"
          required
        />
        <br />
      </form>
    </div>
  );
}
