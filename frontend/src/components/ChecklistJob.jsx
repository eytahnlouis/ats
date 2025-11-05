import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

export default function ChecklistJob({ keywords: initialKeywords = [], onChange }) {
  const [keywords, setKeywords] = useState(initialKeywords);
    useEffect(() => {
      setKeywords(initialKeywords);
    }, [initialKeywords]);

  const style = {
    display: "flex",
    flexDirection: "row",
    gap: "12px",
    padding: "6px",
  };
  const [newWord, setNewWord] = useState(""); // pour l'input du nouveau mot
  const [newWeight, setNewWeight] = useState(1.0); // pour l'input du poids

  const addKeyword = () => {
    if (!newWord.trim()) return;
    const newId = uuidv4();
    const weight = Number.isFinite(+newWeight) ? +newWeight : 1.0;

    setKeywords((prev) => {
      const next = [...prev, { id: newId, word: newWord.trim(), weight }];
      if (onChange) onChange(next); // ✅ Propagation immédiate
      return next;
    });

    setNewWord("");
    setNewWeight(1.0);
  };
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
    </div>
  );
}
