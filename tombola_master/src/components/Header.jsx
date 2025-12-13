import React from "react";

function Header() {
  return (
    <header style={styles.header}>
      <h1>Tombola Online</h1>
      <nav>
        <a href="#home">Home</a> | <a href="#game">Gioca</a> | <a href="#rules">Regole</a>
      </nav>
    </header>
  );
}

const styles = {
  header: {
    backgroundColor: "#282c34",
    color: "white",
    padding: "1rem",
    textAlign: "center"
  }
};

export default Header;
