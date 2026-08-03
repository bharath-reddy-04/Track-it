import { useState } from "react";
import { useCustomer } from "../../context/customercontext";
import { trackMovieClick } from "../../api/customerapi";
import { getWatchProviders } from "../../api/api";
import WatchProviderModal from "../WatchProviderModal/watchprovidermodal";
import "./card.css";

export default function Card({ movie }) {
  const { customerId } = useCustomer();
  const [watchProviderResult, setWatchProviderResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleClick() {
    if (isLoading) return;
    setIsLoading(true);

    if (customerId) {
      trackMovieClick({
        customerId,
        movie: {
          id: movie.id, title: movie.title, poster_path: movie.poster_path,
          backdrop_path: movie.backdrop_path, release_date: movie.release_date,
          vote_average: movie.vote_average,
        },
      }).catch((err) => console.error("Failed to track movie click:", err));
    }

    try {
      setWatchProviderResult(await getWatchProviders(movie.id));
    } catch (err) {
      console.error("Failed to load watch providers:", err);
      setWatchProviderResult({ available: false, message: "Unable to check OTT availability right now. Please try again." });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <div className={`card${isLoading ? " card--loading" : ""}`} onClick={handleClick} role="button" tabIndex="0" onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") handleClick(); }} aria-label={`View where to watch ${movie.title}`}>
      <img
        className="card__poster"
        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
        alt={movie.title}
      />
      <h3 className="card__title">{movie.title}</h3>
      </div>
      {watchProviderResult && <WatchProviderModal movieTitle={movie.title} result={watchProviderResult} onClose={() => setWatchProviderResult(null)} />}
    </>
  );
}
