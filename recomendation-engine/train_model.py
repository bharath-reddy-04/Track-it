"""One-time/offline trainer for the recommendation model.

Run from the Track-it directory:
    backend/myenv/bin/python recomendation-engine/train_model.py
"""

import argparse
import sys
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.recommendation_model import train_recommender  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and save the movie recommendation model.")
    parser.add_argument("--data", type=Path, default=PROJECT_ROOT.parent / "tmdb_movies_clean.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "backend" / "models" / "content_recommender.joblib")
    args = parser.parse_args()

    if not args.data.is_file():
        parser.error(f"Dataset not found: {args.data}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    recommender = train_recommender(str(args.data))
    joblib.dump(recommender, args.output, compress=3)
    print(f"Saved pretrained model for {len(recommender.movies):,} movies to {args.output}")


if __name__ == "__main__":
    main()
