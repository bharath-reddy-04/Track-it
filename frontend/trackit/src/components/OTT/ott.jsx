import React, { useState } from "react";
import Navbar from "../Navbar/navbar";
import MovieRow from "../MovieRow/movierow";
import { getOTTMovies } from "../../api/api";
import "./ott.css";

// Platforms available in the dropdown, paired with the slug the backend's
// GET /api/ott/{provider} expects (must match OTT_PROVIDER_IDS keys in
// backend/app/utils/constants.py). Just display data — the actual fetch
// happens in api/api.js.
const OTT_PROVIDERS = [
  { label: "Netflix", slug: "netflix" },
  { label: "Amazon Prime Video", slug: "amazon-prime-video" },
  { label: "Disney+ Hotstar", slug: "disney-hotstar" },
  { label: "ZEE5", slug: "zee5" },
  { label: "Sony LIV", slug: "sonyliv" },
  { label: "JioHotstar", slug: "jiohotstar" },
  { label: "Apple TV+", slug: "apple-tv-plus" },
  { label: "Hulu", slug: "hulu" },
  { label: "Max (HBO Max)", slug: "max" },
  { label: "Paramount+", slug: "paramount-plus" },
  { label: "Peacock", slug: "peacock" },
  { label: "Crunchyroll", slug: "crunchyroll" },
];

// Row titles + the key each one comes back under from GET /api/ott/{provider}.
// Note: the backend's OTT response has no "trending" or "horror" row.
const CATEGORY_LABELS = [
  { key: "popular", title: "Popular Movies" },
  { key: "topRated", title: "Top Rated Movies" },
  { key: "action", title: "Action Movies" },
  { key: "comedy", title: "Comedy Movies" },
  { key: "romance", title: "Romance Movies" },
  { key: "animation", title: "Animation Movies" },
];

/**
 * OTT
 * ---
 * Lets the user pick a streaming platform, then loads Popular/Top Rated/genre
 * rows filtered to that platform via GET /api/ott/{provider} on the FastAPI
 * backend. No movies are shown until the user picks a platform and clicks
 * Submit. This component never talks to TMDB directly.
 */
function OTT() {
  const [selectedProvider, setSelectedProvider] = useState(OTT_PROVIDERS[0].slug);
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
      const data = await getOTTMovies(selectedProvider);
      setMoviesByCategory(data);
    } catch (err) {
      console.error("Failed to load movies for OTT platform:", err);
      setError("Something went wrong while loading movies. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="ott-page">
      <Navbar />

      <main className="ott-page__content page-content">
        {/* Section 1: Page heading */}
        <h1 className="ott-page__heading">OTT Platforms</h1>

        {/* Section 2: OTT platform selection */}
        <form className="ott-select" onSubmit={handleSubmit}>
          <label htmlFor="ott-select-input" className="ott-select__label">
            Select OTT Platform
          </label>

          <select
            id="ott-select-input"
            className="ott-select__dropdown"
            value={selectedProvider}
            onChange={(event) => setSelectedProvider(event.target.value)}
          >
            {OTT_PROVIDERS.map((provider) => (
              <option key={provider.slug} value={provider.slug}>
                {provider.label}
              </option>
            ))}
          </select>

          <button type="submit" className="ott-select__submit" disabled={loading}>
            {loading ? "Loading..." : "Submit"}
          </button>
        </form>

        {/* Section 3: Movie rows — only appear after a successful submit */}
        {loading && <p className="ott-page__status">Loading movies…</p>}

        {error && <p className="ott-page__status ott-page__status--error">{error}</p>}

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

export default OTT;