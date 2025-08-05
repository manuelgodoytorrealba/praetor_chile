from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()   

EMAIL = os.getenv('EMAIL_USUARIO')
PASSWORD = os.getenv('PASSWORD')
DEBUG = os.getenv('DEBUG') == 'True'