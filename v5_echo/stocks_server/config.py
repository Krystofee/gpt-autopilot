from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

# Ensure the API key is set
if not API_KEY:
    raise ValueError('API key not found. Please set it in the .env file.')