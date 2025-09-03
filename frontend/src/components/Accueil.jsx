import React from 'react';
import { Link } from 'react-router-dom';
 function Accueil() {
  return (
    <div style={{ margin: "2rem auto", maxWidth: 800, padding: "2rem", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h1>Bienvenue sur notre site de recrutement</h1>
      <p>
        Notre plateforme met en relation les entreprises à la recherche de talents et les candidats souhaitant trouver un emploi.
        Explorez nos offres d'emploi, postulez facilement et gérez votre profil en ligne.
      </p>
      <p>
        Que vous soyez une entreprise ou un candidat, nous avons les outils pour vous aider à atteindre vos objectifs de recrutement.
      </p>
    </div>
  );
}
export default Accueil;
// Ce composant affiche un message de bienvenue et une brève description du site de recrutement
// Il est utilisé comme page d'accueil de l'application