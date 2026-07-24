"""
Supabase client initialization.

Requires the following environment variables to be set:
- SUPABASE_URL
- SUPABASE_KEY (service role or anon key with appropriate RLS policies)
"""

import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)