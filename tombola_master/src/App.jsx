import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Main from "./components/Main";
import Footer from "./components/Footer";
import WaitingRoom from "./pages/WaitingRoom";
import GameBoard from "./pages/GameBoard";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/waiting-room" element={<WaitingRoom />} />
        <Route path="/game" element={<GameBoard />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
