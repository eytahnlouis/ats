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
  const jobId = useMemo(() => searchParams.get("job") || "", [searchParams]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [email, setEmail] = useState("");
  const [telephone, setTelephone] = useState("");
  // Style for the input fields

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  async function handleSubmit(e) {
        e.preventDefault();
            setError("");

        if (!file) return setError("Veuillez sélectionner un fichier à télécharger.");
        if (!nom || !prenom || !email || !telephone) {
            return setError("Veuillez remplir tous les champs obligatoires.");
        }
        // Create a FormData object to send the file
        const formData = new FormData();
        // Append personal information to the FormData
        formData.append("resume", file);
        formData.append("nom", nom);
        formData.append("prenom", prenom);
        formData.append("email", email);
        formData.append("telephone", telephone);
        formData.append("job", jobId);
        try {
        // Send the file to the backend API
            setLoading(true);
            await axios.post("http://127.0.0.1:8000/api/cvs/upload/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setLoading(false);
            navigate("/jobs");

        } catch (err) {
        console.error("Erreur lors du téléchargement du CV:", err) ;
        setError("Erreur lors du téléchargement du CV. Veuillez réessayer.");
        setLoading(false);
        }
    }
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
        <label htmlFor="nom">Nom*</label>
        <input
          type="text"
          id="nom"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          name="nom"
          style={inputStyle}
          placeholder="Entrez votre nom"
          required
        />
        <br />
        <label htmlFor="prenom">Prénom*</label>
        <input
          type="text"
          id="prenom"
          name="prenom"
          value={prenom}
          onChange={(e) => setPrenom(e.target.value)}
          style={inputStyle}
          placeholder="Entrez votre prénom"
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
