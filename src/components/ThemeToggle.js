import React from "react";

const ThemeToggle = ({ darkMode, toggleTheme }) => {
  return (
    <button
      className="p-2 rounded bg-gray-800 text-white dark:bg-white dark:text-black transition"
      onClick={toggleTheme}
    >
      {darkMode ? "Light Mode" : "Dark Mode"}
    </button>
  );
};

export default ThemeToggle;
