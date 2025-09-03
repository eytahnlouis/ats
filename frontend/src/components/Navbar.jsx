import { Link, useLocation } from "react-router-dom";
import React from "react";
import useAuth from "../hooks/useAuth";
("../hooks/useAuth");

function Navbar() {
  const isLoggedIn = useAuth();
  // useAuth est un hook personnalisé qui vérifie si l'utilisateur est connecté
  const location = useLocation();
  // useLocation est un hook de react-router-dom qui permet d'obtenir l'URL actuelle
  // Il est utilisé pour mettre en surbrillance le lien actif dans la barre de navigation

  return (
    <nav
      style={{
        background: "#23272f",
        color: "#fff",
        padding: "1rem",
        display: "flex",
        justifyContent: "space-between",
        borderRadius: "50em",
        cursor: "pointer",
        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
        width: "60%",
        margin: "auto auto",
      }}
    >
      <div>
        <Link
          to="/"
          style={{ color: "#fff", textDecoration: "none", fontWeight: "bold" }}
        >
          ATS
        </Link>
      </div>
      <div style={{ display: "flex", gap: "2rem" }}>
        <Link
          to="/jobs"
          style={{
            color: location.pathname === "/jobs" ? "FFD700" : "fff",
            textDecoration: "none",
          }}
        >
          Jobs
        </Link>
        {isLoggedIn ? (
          <>
            <Link
              to="/profile"
              style={{
                color: location.pathname === "/profile" ? "FFD700" : "fff",
                textDecoration: "none",
              }}
            >
              Profil
            </Link>
            <button
              onClick={() => {
                localStorage.removeItem("access-token");
                localStorage.removeItem("refresh-token");
                window.location.reload(); // Redirige vers la page de connexion après la déconnexion
              }}
            ></button>
            <Link
              to="/logout"
              style={{
                color: location.pathname === "/logout" ? "FFD700" : "fff",
                textDecoration: "none",
              }}
            >
              Déconnexion
            </Link>
          </>
        ) : (
          <Link
            to="/login"
            style={{
              color: location.pathname === "/login" ? "FFD700" : "fff",
              textDecoration: "none",
            }}
          >
            Connexion
          </Link>
        )}
        <Link to="/admin" style={{ color: "#fff", textDecoration: "none" }}>
          Admin
        </Link>
      </div>
    </nav>
  );
}
export default Navbar;
// Ce composant Navbar est utilisé pour la navigation dans l'application.
// Il utilise le composant Link de react-router-dom pour naviguer entre les différentes pages.
// Il y a des liens vers les pages principales de l'application : Jobs, Candidats, Admin et Login.
