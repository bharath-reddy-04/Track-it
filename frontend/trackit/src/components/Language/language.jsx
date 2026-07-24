import React, { useState } from "react";
import Navbar from "../Navbar/navbar";
import MovieRow from "../MovieRow/movierow";
import { getLanguageMovies } from "../../api/api";
import "./language.css";

// Languages available in the dropdown, paired with the ISO 639-1 codes the
// backend's GET /api/language/{code} expects. Just display data — the
// actual fetch happens in api/api.js.
const LANGUAGE_OPTIONS = [
  { label: "English", code: "en" },
  { label: "Hindi", code: "hi" },
  { label: "Telugu", code: "te" },
  { label: "Tamil", code: "ta" },
  { label: "Malayalam", code: "ml" },
  { label: "Kannada", code: "kn" },
  { label: "Bengali", code: "bn" },
  { label: "Marathi", code: "mr" },
  { label: "Japanese", code: "ja" },
  { label: "Korean", code: "ko" },
  { label: "French", code: "fr" },
  { label: "Spanish", code: "es" },
  { label: "German", code: "de" },
  { label: "Chinese", code: "zh" },
];

// Row titles + the key each one comes back under from GET /api/language/{code}.
// Note: the backend's language response has no "trending" row (language
// filtering isn't meaningful against TMDB's trending endpoint).
const CATEGORY_LABELS = [
  { key: "popular", title: "Popular Movies" },
  { key: "topRated", title: "Top Rated Movies" },
  { key: "action", title: "Action Movies" },
  { key: "comedy", title: "Comedy Movies" },
  { key: "horror", title: "Horror Movies" },
  { key: "romance", title: "Romance Movies" },
  { key: "animation", title: "Animation Movies" },
];

/**
 * Language
 * --------
 * Lets the user pick a language, then loads Popular/Top Rated/genre rows
 * filtered to that language via GET /api/language/{code} on the FastAPI
 * backend. No movies are shown until the user picks a language and clicks
 * Submit. This component never talks to TMDB directly.
 */
function Language() {
  const [selectedLanguage, setSelectedLanguage] = useState(LANGUAGE_OPTIONS[0].code);
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
      const data = await getLanguageMovies(selectedLanguage);
      setMoviesByCategory(data);
    } catch (err) {
      console.error("Failed to load movies for language:", err);
      setError("Something went wrong while loading movies. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="language-page">
      <Navbar />

      <main className="language-page__content page-content">
        {/* Section 1: Page heading */}
        <h1 className="language-page__heading">Language Movies</h1>

        {/* Section 2: Language selection */}
        <form className="language-select" onSubmit={handleSubmit}>
          <label htmlFor="language-select-input" className="language-select__label">
            Select Language
          </label>

          <select
            id="language-select-input"
            className="language-select__dropdown"
            value={selectedLanguage}
            onChange={(event) => setSelectedLanguage(event.target.value)}
          >
            {LANGUAGE_OPTIONS.map((option) => (
              <option key={option.code} value={option.code}>
                {option.label}
              </option>
            ))}
          </select>

          <button type="submit" className="language-select__submit" disabled={loading}>
            {loading ? "Loading..." : "Submit"}
          </button>
        </form>

        {/* Section 3: Movie rows — only appear after a successful submit */}
        {loading && <p className="language-page__status">Loading movies…</p>}

        {error && <p className="language-page__status language-page__status--error">{error}</p>}

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

export default Language;