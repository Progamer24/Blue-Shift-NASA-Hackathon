import React from "react";
import SearchBar from "../components/SearchBar";
import "../styles/components.css";

const Home = () => (
  <div className="star-background">
    <nav className="navbar">
      <span className="nav-item left">Blue shift</span>
      <div className="nav-right">
<<<<<<< HEAD
        <span className="nav-item">Galaxy |</span>
        <span className="nav-item">Solar system</span>
        <span className="nav-item">| Earth</span>
=======
        <span className="nav-item">galaxy</span>
        <span className="nav-item">Solar system</span>
        <span className="nav-item">earth</span>
>>>>>>> c69abe53c6959fa8793c5ab03e60da718bc98188
      </div>
    </nav>
    <div className="center-container">
      <SearchBar placeholder="Search stars or constellations..." />
    </div>
  </div>
);

export default Home;
