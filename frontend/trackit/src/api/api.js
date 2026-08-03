import axios from "axios";

/**
 * api.js
 * ------
 * The ONLY place in the frontend that knows about the backend's base URL.
 * Every page component calls one of the functions below instead of
 * building fetch/axios calls itself — this is what keeps fetch logic out
 * of Card/MovieRow/Navbar and out of the page components' render code.
 *
 * IMPORTANT: this app never calls https://api.themoviedb.org directly.
 * All TMDB access happens server-side in the FastAPI backend, which is
 * the only place the TMDB API key exists.
 */
const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

/**
 * GET /api/home
 * @returns {Promise<Object>} { trending, popular, topRated, action, comedy, horror, romance, animation }
 */
export async function getHomeMovies() {
  const { data } = await api.get("/home");
  return data;
}

/**
 * GET /api/language/{languageCode}
 * @param {string} languageCode - ISO 639-1 code, e.g. "te" for Telugu
 * @returns {Promise<Object>} { popular, topRated, action, comedy, horror, romance, animation }
 */
export async function getLanguageMovies(languageCode) {
  const { data } = await api.get(`/language/${languageCode}`);
  return data;
}

/**
 * GET /api/genre/{genre}
 * @param {string} genre - one of: action, comedy, horror, romance, animation
 * @returns {Promise<Object>} { trending, popular, topRated }
 */
export async function getGenreMovies(genre) {
  const { data } = await api.get(`/genre/${genre}`);
  return data;
}

/**
 * GET /api/ott/{provider}
 * @param {string} provider - platform slug, e.g. "netflix", "amazon-prime-video"
 * @returns {Promise<Object>} { popular, topRated, action, comedy, romance, animation }
 */
export async function getOTTMovies(provider) {
  const { data } = await api.get(`/ott/${provider}`);
  return data;
}

/**
 * GET /api/movie/{movieId}/watch-providers
 * @returns {Promise<Object>} India's subscription providers and TMDB watch link.
 */
export async function getWatchProviders(movieId) {
  const { data } = await api.get(`/movie/${movieId}/watch-providers`);
  return data;
}

export default api;
