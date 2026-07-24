import React, { useState } from "react";
import Navbar from "../Navbar/navbar";
import MovieRow from "../MovieRow/movierow";
import { getGenreMovies } from "../../api/api";
import "./genre.css";

// Genres available in the dropdown, paired with the slug the backend's
// GET /api/genre/{genre} expects (must match GENRE_IDS keys in
// backend/app/utils/constants.py).
const GENRE_OPTIONS = [
  { label: "Action", slug: "action" },
  { label: "Comedy", slug: "comedy" },
  { label: "Horror", slug: "horror" },
  { label: "Romance", slug: "romance" },
  { label: "Animation", slug: "animation" },
];

// Row titles + the key each one comes back under from GET /api/genre/{genre}.
const CATEGORY_LABELS = [
  { key: "trending", title: "Trending Movies" },
  { key: "popular", title: "Popular Movies" },
  { key: "topRated", title: "Top Rated Movies" },
];

/**
 * Genre
 * -----
 * Lets the user pick a genre, then loads Trending/Popular/Top Rated rows
 * scoped to that genre via GET /api/genre/{genre} on the FastAPI backend.
 * No movies are shown until the user picks a genre and clicks Submit.
 * This component never talks to TMDB directly.
 */
function Genre() {
  const [selectedGenre, setSelectedGenre] = useState(GENRE_OPTIONS[0].slug);
  // moviesByCategory stays null until the first successful submit, which is
  // what keeps the rows hidden before the user has made a selection.
  const [moviesByCategory, setMoviesByCategory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await getGenreMovies(selectedGenre);
      setMoviesByCategory(data);
    } catch (err) {
      console.error("Failed to load movies for genre:", err);
      setError("Something went wrong while loading movies. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="genre-page">
      <Navbar />

      <main className="genre-page__content page-content">
        {/* Section 1: Page heading */}
        <h1 className="genre-page__heading">Genre Movies</h1>

        {/* Section 2: Genre selection */}
        <form className="genre-select" onSubmit={handleSubmit}>
          <label htmlFor="genre-select-input" className="genre-select__label">
            Select Genre
          </label>

          <select
            id="genre-select-input"
            className="genre-select__dropdown"
            value={selectedGenre}
            onChange={(event) => setSelectedGenre(event.target.value)}
          >
            {GENRE_OPTIONS.map((option) => (
              <option key={option.slug} value={option.slug}>
                {option.label}
              </option>
            ))}
          </select>

          <button type="submit" className="genre-select__submit" disabled={loading}>
            {loading ? "Loading..." : "Submit"}
          </button>
        </form>

        {/* Section 3: Movie rows — only appear after a successful submit */}
        {loading && <p className="genre-page__status">Loading movies…</p>}

        {error && <p className="genre-page__status genre-page__status--error">{error}</p>}

        {!loading &&
          !error &&
          moviesByCategory &&
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

export default Genre;