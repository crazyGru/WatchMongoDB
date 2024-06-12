import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_directory = "log"
os.makedirs(log_directory, exist_ok=True)  # Create log directory if it doesn't exist

def setup_logging():
    log_file = os.path.join(log_directory, f"{datetime.now().strftime('%Y_%m_%d')}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def detect_update():
    # Get the MongoDB URI from environment variable
    uri = os.getenv('MONGODB_URI')
    if not uri:
        raise ValueError("MONGODB_URI environment variable not set")

    client = MongoClient(uri)

    try:
        # Verify connection
        client.admin.command('ping')
        print('Connected to MongoDB')

        database = client['harmony']  # Replace with your database name
        collection = database['profiles']  # Replace with your collection name

        # Create a change stream on the collection
        change_stream = collection.watch()

        # Listen for changes
        for change in change_stream:
            if not os.path.exists(log_directory):  # Check if log directory exists
                os.makedirs(log_directory)  # Create log directory if it doesn't exist
            setup_logging()  # Setup logging for each change event
            logging.info("Changed Document: %s", change)
            logging.info("-"*100)
            if change['operationType'] == 'insert':
                logging.info('Document inserted: %s', change['fullDocument'])
            elif change['operationType'] == 'update':
                logging.info('Document updated: %s', change['updateDescription'])
            elif change['operationType'] == 'delete':
                logging.info('Document deleted: %s', change['documentKey'])
            else:
                logging.info('Other change: %s', change)

    except ConnectionFailure:
        logging.error('Failed to connect to MongoDB')
