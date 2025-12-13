import React from "react";

function Footer() {
  return (
    <footer style={styles.footer}>
      <p>© 2025 Tombola Web - Tutti i diritti riservati</p>
    </footer>
  );
}

const styles = {
  footer: {
    backgroundColor: "#f1f1f1",
    padding: "1rem",
    textAlign: "center",
    marginTop: "2rem"
  }
};

export default Footer;
