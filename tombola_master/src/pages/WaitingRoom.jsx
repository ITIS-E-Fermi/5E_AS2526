import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function WaitingRoom() {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  const fetchPlayers = () => {
    fetch("http://localhost:3001/players")
      .then(res => res.json())
      .then(data => setPlayers(data));
  };

  useEffect(() => {
    fetchPlayers();
    const interval = setInterval(fetchPlayers, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h2>Sala di attesa</h2>
      <p>Giocatori collegati:</p>
      <ul>
        {players.map((p) => (
          <li key={p.id}>
            {p.number}. {p.username}
          </li>
        ))}
      </ul>
      <button onClick={() => navigate("/game")} style={{ marginTop: "2rem" }}>
        Avvia Gioco
      </button>
    </div>
  );
}

export default WaitingRoom;
