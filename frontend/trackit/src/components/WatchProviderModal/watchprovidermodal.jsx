import { useEffect } from "react";
import "./watchprovidermodal.css";

const TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w185";

export default function WatchProviderModal({ movieTitle, result, onClose }) {
  useEffect(() => {
    const closeOnEscape = (event) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [onClose]);

  const openTmdbWatchPage = () => {
    window.open(result.link, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="watch-modal__backdrop" onMouseDown={onClose} role="presentation">
      <section
        className="watch-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="watch-modal-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <button className="watch-modal__close" onClick={onClose} aria-label="Close modal">
          ×
        </button>

        {result.available ? (
          <>
            <p className="watch-modal__eyebrow">AVAILABLE ON</p>
            <h2 id="watch-modal-title">{movieTitle}</h2>
            <div className="watch-modal__providers">
              {result.providers.map((provider) => (
                <article className="watch-modal__provider" key={provider.provider_id}>
                  {provider.logo_path ? (
                    <img
                      src={`${TMDB_IMAGE_BASE_URL}${provider.logo_path}`}
                      alt={`${provider.provider_name} logo`}
                    />
                  ) : (
                    <div className="watch-modal__logo-placeholder" aria-hidden="true" />
                  )}
                  <span>{provider.provider_name}</span>
                  <button onClick={openTmdbWatchPage}>Open {provider.provider_name}</button>
                </article>
              ))}
            </div>
            <button className="watch-modal__watch-now" onClick={openTmdbWatchPage}>
              Watch Now
            </button>
          </>
        ) : (
          <div className="watch-modal__unavailable">
            <p className="watch-modal__eyebrow">MOVIE NOT AVAILABLE</p>
            <h2 id="watch-modal-title">Movie Not Available</h2>
            <p>{result.message}</p>
            <button className="watch-modal__watch-now" onClick={onClose}>Close</button>
          </div>
        )}
      </section>
    </div>
  );
}
