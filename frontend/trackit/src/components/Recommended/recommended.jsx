import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../Navbar/navbar";
import MovieRow from "../MovieRow/movierow";
import { useCustomer } from "../../context/customercontext";
import { getRecommendations } from "../../api/recommendationApi";
import "./recommended.css";

export default function Recommended() {
  const { customerId, isLoading: isCustomerLoading } = useCustomer();
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isCustomerLoading || !customerId) return;

    let isMounted = true;
    setIsLoading(true);
    setError("");
    getRecommendations(customerId)
      .then((data) => {
        if (isMounted) setMovies(data.recommendations || []);
      })
      .catch((err) => {
        if (isMounted) setError(err.message || "Could not load recommendations.");
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => { isMounted = false; };
  }, [customerId, isCustomerLoading]);

  return (
    <div className="recommended-page">
      <Navbar />
      <main className="recommended-page__content page-content">
        <h1>Recommended For You</h1>
        {isCustomerLoading && <p>Loading your profile…</p>}
        {!isCustomerLoading && !customerId && (
          <p>Please <Link to="/register">register</Link> to get personalized recommendations.</p>
        )}
        {isLoading && (
          <section className="movie-row" aria-label="Loading recommendations">
            <div className="movie-row__track">
              {[1, 2, 3, 4, 5].map((item) => <div className="recommendation-skeleton" key={item} />)}
            </div>
          </section>
        )}
        {error && <p className="recommended-page__error">{error}</p>}
        {!isLoading && !error && customerId && movies.length === 0 && (
          <p>Click a few movies first, then come back here for recommendations.</p>
        )}
        {!isLoading && !error && movies.length > 0 && <MovieRow title="Recommended For You" movies={movies} />}
      </main>
    </div>
  );
}
