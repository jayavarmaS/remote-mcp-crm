import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG URL:", SUPABASE_URL)  # 👈 add this

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)