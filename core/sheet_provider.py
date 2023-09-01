# Feature: Implement Cerebras AI support
# Feature: Implement multi-database query routing
# Fix: Fix embedding dimension mismatches
# Feature: Add AWS Bedrock integration
# Feature: Implement custom embedding models
# Feature: Add AWS Bedrock integration
# Feature: Add error handling mechanisms
# Feature: Implement hybrid search functionality
# Fix: Resolve vector similarity calculation
# Feature: Add vector embedding generation
# Feature: Add error handling mechanisms
# Feature: Implement entity extraction pipeline
# Feature: Add comprehensive logging system
# Feature: Add relationship mapping functionality
# Feature: Add Google Sheets API integration
# Feature: Add automated data refresh pipeline
# Feature: Implement rational planner agent
# Fix: Resolve database connection timeouts
# Feature: Add user session management
# Feature: Implement entity extraction pipeline
# Feature: Add query generator functionality
# Fix: Resolve logging configuration issues
# Feature: Implement Opik experiment tracking
# Feature: Add table augmenter for data formatting
# Feature: Implement Milvus vector database support
# Feature: Add advanced filtering capabilities
# Feature: Add PostgreSQL database operations
# Feature: Implement prioritizer for data sources
# Feature: Add relationship mapping functionality
# Feature: Implement intelligent query planning
# Fix: Fix authentication flow issues
# Feature: Implement entity extraction pipeline
# Feature: Add table augmenter for data formatting
# Feature: Implement hybrid search functionality
# Test: Implement stress tests for system limits
# Feature: Add Google Sheets API integration
# Feature: Add PostgreSQL database operations
# Feature: Implement secure credential management
# Feature: Add context-aware response generation
# Fix: Resolve logging configuration issues
# Feature: Add result augmenter capabilities
# Feature: Add conversation flow management
# Feature: Implement plain augmenter for simple queries
# Refactor: Restructure database connection management
# Feature: Implement custom embedding models
# Feature: Implement Chainlit UI interface
# Fix: Fix Milvus index corruption
# Fix: Fix query parsing errors
# Fix: Fix Milvus index corruption
# Feature: Implement entity extraction pipeline
# Fix: Resolve query generation edge cases
# Feature: Add multi-agent architecture framework
# Refactor: Refactor UI components for reusability
# Feature: Add context-aware response generation
# Fix: Resolve PostgreSQL deadlock issues
# Fix: Resolve query generation edge cases
# Feature: Implement Cerebras AI support
# Feature: Add multi-agent architecture framework
# Feature: Implement role-based access control
# Refactor: Refactor agent communication protocols
# Feature: Add vector embedding generation
# Fix: Fix relationship mapping errors
# Feature: Add LangChain orchestration
# Feature: Implement advanced search algorithms
# Feature: Add user feedback collection
# Refactor: Optimize resource allocation
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import Credentials as ConfigCredentials
from typing import Optional, Dict, Any
import logging

class RocloSheetProvider:
    """
    Singleton class to manage Roclo Sheet
    """
    _instance: Optional['RocloSheetProvider'] = None

    def __new__(cls):
        """Create a new instance if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloSheetProvider, cls).__new__(cls)
            cls._instance.SHEET_ID = ConfigCredentials.get_secret("SHEET_ID")
            cls._instance.SHEET_RANGE_NAME = ConfigCredentials.get_secret("SHEET_RANGE_NAME")
            cls._instance.SCOPES = [ConfigCredentials.get_secret("SHEET_SCOPE")]
        return cls._instance
    
    @classmethod
    def connect(cls):
        """Initialize the connection to the GoogleSheet"""
        if cls._instance is None:
            cls()
        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = GoogleCredentials.from_authorized_user_file("token.json", cls._instance.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logging.getLogger('main').info("Token expired, require to refresh.")
                creds.refresh(Request())
            else:
                logging.getLogger('main').info("Creds not found, require to re-launch the token.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", cls._instance.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            logging.getLogger('main').info("Successfully Refreshed expired token.")

        cls._instance.service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        # -------- Read data from sheet --------
        cls._instance.sheet = cls._instance.service.spreadsheets()

        logging.getLogger('main').info("Successfully connected to Sheet.")
    

    @classmethod
    def get_deals(cls):
        try:
            result = cls._instance.sheet.values().get(spreadsheetId=cls._instance.SHEET_ID,
                                    range=cls._instance.SHEET_RANGE_NAME).execute()

            values = result.get('values', [])

            return values
        except Exception as e:
            logging.getLogger('main').info("Failed to get deals. %s", e)
            return None

