import React from "react";
import { NavLink } from "react-router-dom";
import "./navbar.css";

// List of navigation items.
// Keeping this as data (instead of hardcoding JSX) makes it easy to
// add/remove/reorder links without touching the markup below.
const NAV_ITEMS = [
  { label: "Home", path: "/" },
   { label: "OTT", path: "/ott" },
  { label: "Recommended", path: "/recommended" },
  { label: "Language", path: "/language" },
  { label: "Genre", path: "/genre" },
 
  { label: "Chat", path: "/chat" },
  { label: "Register", path: "/register" },
];

/**
 * Navbar
 * ------
 * Fixed, Netflix-style top navigation bar for the OTT site.
 *
 * - Uses <nav>/<ul>/<li> for semantic, accessible markup.
 * - Uses React Router's NavLink so the active route is automatically
 *   given an "active" class (see Navbar.css) without manual state.
 * - Fully responsive: items wrap/shrink gracefully on small screens.
 */
function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar__container">
        {/* Brand/logo area - purely visual, not part of the required nav items */}
        <div className="navbar__brand">Track !t</div>

        <ul className="navbar__list">
          {NAV_ITEMS.map((item) => (
            <li key={item.path} className="navbar__item">
              <NavLink
                to={item.path}
                // "end" ensures the Home ("/") link is only active on an exact match,
                // so it doesn't stay highlighted when on other routes.
                end={item.path === "/"}
                className={({ isActive }) =>
                  isActive ? "navbar__link navbar__link--active" : "navbar__link"
                }
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
