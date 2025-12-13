import React, { useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";

function GameBoard() {
  const [extracted, setExtracted] = useState([]);
  const numbers = Array.from({ length: 90 }, (_, i) => i + 1);
  const navigate = useNavigate();
  const [wins, setWins] = useState([]);

  const extractNumber = () => {
  fetch("http://localhost:3001/draw", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      setExtracted([...extracted, data.number]);
    });
};


  const fetchWins = () => {
    fetch("http://localhost:3001/wins")
      .then(res => res.json())
      .then(data => setWins(data));
  };

  useEffect(() => {
    fetchWins();
    const interval = setInterval(fetchWins, 5000);
    return () => clearInterval(interval);
  }, []);



  // Suddividi in 6 schede da 5x3
  const cards = [];
  for (let i = 0; i < 6; i++) {
    const start = i * 15;
    cards.push(numbers.slice(start, start + 15));
  }

  return (
   <div style={{ display: "flex", padding: "2rem" }}>
      {/* Colonna sinistra: legenda vincite */}
      <div style={{ width: "25%", paddingRight: "1rem" }}>
        <h3>Legenda vincite</h3>
        <ul>
          {wins.map((w) => (
            <li key={w.id}>
              {w.username} → {w.type}
            </li>
          ))}
        </ul>
      </div>

      {/* Tabellone centrale */}
      <div style={{ width: "60%", textAlign: "center" }}>
        <h2>Tabellone</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(10, 40px)", gap: "5px" }}>
          {numbers.map((num) => (
            <div
              key={num}
              style={{
                width: "40px",
                height: "40px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                border: "1px solid #ccc",
                backgroundColor: extracted.includes(num) ? "#90ee90" : "white"
              }}
            >
              {num}
            </div>
          ))}
        </div>

        <button onClick={extractNumber} style={{ marginTop: "2rem" }}>
          Estrai Numero
        </button>
        <button onClick={() => navigate("/")} style={{ marginTop: "1rem", marginLeft: "1rem" }}>
          Fine Gioco
        </button>
      </div>
    </div>
  );
}

export default GameBoard;
