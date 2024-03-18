import re
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser
import glob
import logging
from typing import Optional

# Configuration
from config import CONFIG  # Assuming you have a config.py file with necessary configurations

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_contact_number(contact: str) -> str:
    """
    Clean and format the contact number.
    
    Parameters:
        contact (str): The contact number to clean.
    
    Returns:
        str: The cleaned contact number.
    """
    contact = str(contact)
    cleaned_contact = re.sub(r'\D', '', contact)
    if len(cleaned_contact) > 9:
        cleaned_contact = cleaned_contact[-9:]
    return cleaned_contact

def transform_csv(file_path: str, status: str = 'Unknown') -> pd.DataFrame:
    """
    Transform the CSV file to the desired format.
    
    Parameters:
        file_path (str): Path to the CSV file.
        status (str): Status to be assigned to each record.
    
    Returns:
        pd.DataFrame: The transformed DataFrame.
    """
    try:
        df = pd.read_csv(file_path)

        column_mappings = {
            'Card ID': 'card_id',
            'User contact': 'user_contact',
            'User Mobile': 'user_contact',
            'Timestamp': 'timestamp',
            'Comment': 'comment'
        }
        df.rename(columns=column_mappings, inplace=True)

        if 'status' not in df.columns:
            df['status'] = status
        if 'comment' not in df.columns:
            df['comment'] = ''
        
        desired_columns = ['card_id', 'user_contact', 'timestamp', 'status', 'comment']
        df = df.reindex(columns=desired_columns).fillna('')
        df['user_contact'] = df['user_contact'].apply(clean_contact_number)
        df['timestamp'] = df['timestamp'].apply(lambda x: parser.parse(x).strftime('%Y-%m-%d %H:%M:%S'))

        return df
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return pd.DataFrame()

def load_data(engine, df: pd.DataFrame) -> None:
    """
    Load data into the database.
    
    Parameters:
        engine: The SQLAlchemy engine instance.
        df (pd.DataFrame): DataFrame to be inserted into the database.
    """
    if df.empty:
        logging.warning("Empty DataFrame. No data to insert.")
        return
    
    try:
        df.to_sql('card_status_events', con=engine, if_exists='append', index=False)
        logging.info("Data inserted successfully!")
    except SQLAlchemyError as e:
        logging.error(f"Error inserting data into database: {e}")

def main() -> None:
    """
    Main function to process CSV files and load them into the database.
    """
    try:
        DATABASE_URI = f"postgresql+psycopg2://{CONFIG['DB_USER']}:{CONFIG['DB_PASSWORD']}@{CONFIG['DB_HOST']}:{CONFIG['DB_PORT']}/{CONFIG['DB_NAME']}"
        engine = create_engine(DATABASE_URI)
        logging.info(f"Database connection established! {DATABASE_URI}")

        file_paths = glob.glob(CONFIG['DATA_PATH'])

        for file_path in file_paths:
            if "delivered" in file_path.lower():
                status = 'Delivered'
            elif "returned" in file_path.lower():
                status = 'Returned'
            elif "delivery exceptions" in file_path.lower():
                status = 'Delivery Exceptions'
            elif "pickup" in file_path.lower():
                status = 'Picked Up'

            logging.info(f"Processing file: {file_path}")
            df_transformed = transform_csv(file_path, status=status)
            load_data(engine, df_transformed)
    except Exception as e:
        logging.error("Error processing files. Exiting...")
        logging.exception(e)

if __name__ == "__main__":
    logging.info("ETL Pipeline started!")
    main()