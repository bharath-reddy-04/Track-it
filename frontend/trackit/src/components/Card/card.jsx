import { useCustomer } from "../../context/customercontext";
import { trackMovieClick } from "../../api/customerapi";
import "./card.css";

export default function Card({ movie }) {
  const { customerId } = useCustomer();

  function handleClick() {
    if (!customerId) return;

    trackMovieClick({
      customerId,
      movie: {
        id: movie.id,
        title: movie.title,
        poster_path: movie.poster_path,
        backdrop_path: movie.backdrop_path,
        release_date: movie.release_date,
        vote_average: movie.vote_average,
      },
    }).catch((err) => {
      console.error("Failed to track movie click:", err);
    });
  }

  return (
    <div className="card" onClick={handleClick}>
      <img
        className="card__poster"
        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
        alt={movie.title}
      />
      <h3 className="card__title">{movie.title}</h3>
    </div>
  );
}