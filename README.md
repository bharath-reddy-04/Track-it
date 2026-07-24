# OTT Recommender

A simple movie discovery and recommendation app. It uses a React frontend, a FastAPI backend, TMDB movie data, and a content-based recommendation engine.

## Features

- Browse trending, popular, top-rated, and genre-based movies.
- Filter movies by language and OTT platform.
- Create a customer profile and track clicked movies.
- Receive personalized movie recommendations based on viewing activity.

## Project structure

```
ott_recomender/
├── frontend/trackit/        # React application
├── backend/                 # FastAPI API and services
├── recomendation-engine/    # Recommendation model and movie dataset
└── supabase/                # Database migration
```

## Prerequisites

- Node.js and npm
- Python 3.10+
- A TMDB API key
- A Supabase project for customer data

## Setup

### Backend

```bash
cd backend
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
TMDB_API_KEY=your_tmdb_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
DEFAULT_WATCH_REGION=IN
CORS_ORIGINS=http://localhost:3000
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Train the recommendation model once before starting the API. This may take a
few minutes and writes a local, ignored model artifact; the API only loads this
artifact for every later session and request.

```bash
cd ..
backend/myenv/bin/python recomendation-engine/train_model.py
cd backend
uvicorn app.main:app --reload
```

To use a model stored elsewhere, set `RECOMMENDER_MODEL_PATH` to its absolute path.

The backend runs at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive API documentation.

### Frontend

In a second terminal:

```bash
cd frontend/trackit
npm install
npm start
```

Open `http://localhost:3000` in your browser.

## Database

Run `supabase/migration.sql` in your Supabase SQL editor before using customer profiles and personalized recommendations.

## Notes

- The frontend calls the FastAPI backend at `http://localhost:8000/api`.
- The backend keeps the TMDB API key private and handles all TMDB requests.
