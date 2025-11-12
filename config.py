"""Configuration for Pied Piper Legal Simulator"""
import os
from dotenv import load_dotenv

# Load secrets from global.env
load_dotenv(os.path.expanduser("~/.config/secrets/global.env"))

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# App Config
APP_NAME = "Pied Piper Legal Simulator"
APP_VERSION = "1.0.0"
DEBUG = True

# Database
DUCKDB_PATH = "data/legal_simulator.duckdb"

# Agent Config
MAX_RETRIES = 3
TEMPERATURE = 0.7

