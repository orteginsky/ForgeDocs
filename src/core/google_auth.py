import os
import logging
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build, Resource
from .config import settings

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

class GoogleClientManager:
    _instance = None
    _docs_service = None
    _drive_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleClientManager, cls).__new__(cls)
            cls._instance._initialize_services()
        return cls._instance

    def _initialize_services(self):
        """
        Initializes Google API services. 
        Priority:
        1. FORGE_DOCS_TOKEN (Env var with full JSON)
        2. GOOGLE_TOKEN_FILE (Local path to token.json)
        """
        creds = None
        
        # 1. Try from Environment Variable (Secret Manager integration in Cloud Run)
        if settings.FORGE_DOCS_TOKEN:
            try:
                token_data = json.loads(settings.FORGE_DOCS_TOKEN)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
                logger.info("Credentials loaded from FORGE_DOCS_TOKEN environment variable.")
            except Exception as e:
                logger.error(f"Error parsing FORGE_DOCS_TOKEN: {e}")

        # 2. Try from Local File
        if not creds:
            if os.path.exists(settings.GOOGLE_TOKEN_FILE):
                try:
                    creds = Credentials.from_authorized_user_file(settings.GOOGLE_TOKEN_FILE, SCOPES)
                    logger.info(f"Credentials loaded from local file: {settings.GOOGLE_TOKEN_FILE}")
                except Exception as e:
                    logger.error(f"Error reading local token file: {e}")
            else:
                error_msg = f"No credentials found. Provide FORGE_DOCS_TOKEN or check {settings.GOOGLE_TOKEN_FILE}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)

        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token expired, refreshing...")
            try:
                creds.refresh(Request())
                if not settings.FORGE_DOCS_TOKEN and os.path.exists(settings.GOOGLE_TOKEN_FILE):
                    with open(settings.GOOGLE_TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise

        if not creds or not creds.valid:
            raise RuntimeError("Invalid credentials and failed to refresh.")

        try:
            self._docs_service = build('docs', 'v1', credentials=creds)
            self._drive_service = build('drive', 'v3', credentials=creds)
            logger.info("Google Services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to build Google Services: {str(e)}")
            raise e

    @property
    def docs(self) -> Resource:
        return self._docs_service

    @property
    def drive(self) -> Resource:
        return self._drive_service

# Singleton access point
google_client = GoogleClientManager()
