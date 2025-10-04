import React from "react";
import SearchBar from "../components/SearchBar";
import "../styles/components.css";

const Home = () => (
  <div className="star-background">
    <nav className="navbar">
      <span className="nav-item left">Blue shift</span>
      <div className="nav-right">
        <span className="nav-item">galaxy</span>
        <span className="nav-item">Solar system</span>
        <span className="nav-item">earth</span>
      </div>
    </nav>
    <div className="center-container">
      <SearchBar placeholder="Search stars or constellations..." />
    </div>
  </div>
);

export default Home;
