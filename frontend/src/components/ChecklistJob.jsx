import { useState } from "react";
import { useEffect } from "react";

export default function ChecklistJob({ onChange }) {
  const [keywords, setKeywords] = useState([{ id: 1, word: "exemple", weight: 1.0 }]);

  const Importance = {
    "HIGH": 5.0,
    "MEDIUM-HIGH": 4.0,
    "MEDIUM": 3.0,
    "MEDIUM-LOW": 2.0,
    "LOW": 1.0,
  };

  const style = {
    display: "flex",
    flexDirection: "row",
    gap: "12px",
    padding: "16px",
  };
  const [newWord, setNewWord] = useState(""); // pour l'input du nouveau mot
  const [newWeight, setNewWeight] = useState(1.0); // pour l'input du poids

  const addKeyword = () => {
    if (!newWord.trim()) return;
    setKeywords((...prev) => {
      const maxId = prev.length
        ? Math.max(0, ...prev.map((k) => Number(k.id || 0)))
        : 0;
      const newId = maxId + 1;
      const weight = Number.isFinite(+newWeight) ? +newWeight : 1.0;
      return [{ id: newId, word: newWord.trim(), weight }];
    });
    setNewWord("");
    setNewWeight(1.0);
  };
 useEffect(() => {
   try {
     onChange(Array.isArray(keywords) ? keywords : []);
   } catch (e) {
      alert("Erreur lors de la mise à jour des mots-clés" + e.message);
   }
 }, [keywords, onChange]);
  return (
    <div style={style}>
      <h3>Mots-clés du poste</h3>

      {/* Liste actuelle */}
      <ul> 
        {keywords.map((k) => (
          <li key={k.id}>
            {k.word} – Poids : {k.weight}
          </li>
        ))}
      </ul>

      {/* Inputs pour ajouter */}
      <input
        type="text"
        placeholder="Nouveau mot-clé"
        value={newWord}
        onChange={(e) => setNewWord(e.target.value)}
      />
      <input
        type="number"
        placeholder="Poids"
        value={newWeight}
        onChange={(e) => setNewWeight(e.target.value)}
        step="1"
      />
      <button onClick={addKeyword}>Ajouter le mot-clé</button>
      <pre>{JSON.stringify(keywords, null, 2)}</pre>

      {/* Pour voir le JSON généré */}
    </div>
  );
}
