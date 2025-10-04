import React from "react";
import "./SearchBar.css";

const SearchBar = ({ placeholder }) => (
  <div className="search-box">
    
    <input
      className="search-input"
      placeholder={placeholder}
      type="text"
    />
  </div>
);

export default SearchBar;
