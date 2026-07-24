import React, { useEffect, useState } from "react";
import Navbar from "../Navbar/navbar";
import MovieRow from "../MovieRow/movierow";
import { getHomeMovies } from "../../api/api";
import "./home.css";

// Row titles + the key each one comes back under from GET /api/home.
// This is just display data (not fetch logic), so it's fine to keep here —
// the actual API call lives in api/api.js.
const CATEGORY_LABELS = [
  { key: "trending", title: "Trending Movies" },
  { key: "popular", title: "Popular Movies" },
  { key: "topRated", title: "Top Rated Movies" },
  { key: "action", title: "Action Movies" },
  { key: "comedy", title: "Comedy Movies" },
  { key: "horror", title: "Horror Movies" },
  { key: "romance", title: "Romance Movies" },
  { key: "animation", title: "Animation Movies" },
];

/**
 * Home
 * ----
 * The main browsing page: a fixed Navbar followed by one MovieRow per
 * category. All data comes from a single call to GET /api/home on the
 * FastAPI backend — this component never talks to TMDB directly.
 */
function Home() {
  const [moviesByCategory, setMoviesByCategory] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadHome() {
      try {
        const data = await getHomeMovies();
        if (isMounted) {
          setMoviesByCategory(data);
        }
      } catch (err) {
        console.error("Failed to load home movies:", err);
        if (isMounted) {
          setError("Something went wrong while loading movies. Please try again.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadHome();

    // Prevent state updates if the component unmounts before the fetch resolves.
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="home">
      <Navbar />

      <main className="home__content page-content">
        {isLoading && <p className="home__status">Loading movies…</p>}

        {error && <p className="home__status home__status--error">{error}</p>}

        {!isLoading &&
          !error &&
          CATEGORY_LABELS.map((category) => (
            <MovieRow
              key={category.key}
              title={category.title}
              movies={moviesByCategory[category.key] || []}
            />
          ))}
      </main>
    </div>
  );
}

export default Home;