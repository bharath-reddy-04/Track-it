import { Routes, Route } from "react-router-dom";
import Home from "./components/Home/home";
import Language from "./components/Language/language";
import Genre from "./components/Genre/genre";
import OTT from "./components/OTT/ott";
import Chat from "./components/Chat/chat";
import Register from "./components/Register/register";
import Recommended from "./components/Recommended/recommended";
import "./App.css";

/**
 * App
 * ---
 * Top-level app shell. Each page renders its own Navbar, so App just sets
 * up routing. Every page fetches data through src/api/api.js, which talks
 * to the FastAPI backend — never directly to TMDB.
 */
function App() {
  return (
    
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/language" element={<Language />} />
          <Route path="/genre" element={<Genre />} />
          <Route path="/ott" element={<OTT />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/register" element={<Register />} />
          <Route path="/recommended" element={<Recommended />} />
          

          {/* Add a route for Recommended here once that page exists,
              e.g. <Route path="/recommended" element={<Recommended />} /> */}
        </Routes>
      </div>
    
  );
}

export default App;

 
