import React from "react";
import { useNavigate } from "react-router-dom";

function Main() {
  const navigate = useNavigate();

  const resetDb = () => {
    fetch("http://localhost:3001/reset", { method: "DELETE" })
      .then(res => res.json())
      .then(data => alert(data.message));
  };

  return (
    <main style={{ textAlign: "center", padding: "2rem" }}>
      <h2>Benvenuto nella Tombola!</h2>
      <p>Gioca online con cartelle interattive e divertiti con amici e colleghi.</p>
      <button onClick={() => navigate("/waiting-room")}>Inizia la partita</button>
      <button onClick={resetDb} style={{ marginLeft: "1rem" }}>
        Reset Database
      </button>
    </main>
  );
}

export default Main;
