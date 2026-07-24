import React from "react";
import Card from "../Card/card";
import "./movierow.css";

/**
 * MovieRow
 * --------
 * Renders a titled, horizontally-scrollable row of movie Cards.
 * This component is fully reusable — it just needs a title and a
 * movies array, and knows nothing about where that data came from.
 *
 * Props:
 *   title  (string) - Row heading, e.g. "Trending Movies"
 *   movies (array)  - Array of movie objects, each rendered as a <Card />
 */
function MovieRow({ title, movies = [] }) {
  // Avoid rendering an empty row (e.g. while data is still loading)
  if (!movies.length) return null;

  return (
    <section className="movie-row">
      <h2 className="movie-row__title">{title}</h2>

      <div className="movie-row__track">
        {movies.map((movie) => (
          <Card key={movie.id} movie={movie} />
        ))}
      </div>
    </section>
  );
}

export default MovieRow;