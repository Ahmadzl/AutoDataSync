# data_processing.py
'''
Concise of the (data_processing.py) script.
Logging Setup: Configures logging to record events and errors in project.log.

read_csv_file Function: Reads data from a CSV file into a pandas DataFrame. 
It handles various errors (e.g., file not found, empty file, parsing issues, encoding errors) and logs them.

process_data Function: Processes the DataFrame by:

    * Converting ORDERDATE to datetime.
    * Filling missing values in key columns (ORDERNUMBER and SALES) with default values.
    * Converting PRICEEACH to numeric and filling missing values with the median.
    * Removing the ADDRESSLINE2 column .
    * Adding a TOTALVALUE column calculated from QUANTITYORDERED and PRICEEACH.
    * Dropping rows with missing values after conversions. 
    * Logging successful processing or any errors encountered.
    * update_sql_table Function: Updates an SQL table with the processed data using SQLAlchemy. 
    * It logs success or failure and returns boolean indicating the result.
'''

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import logging

# Configure logging
logging.basicConfig(
    filename='project.log',  # Log file location
    level=logging.INFO,      # Set logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

def read_csv_file(file_path, encoding='latin1'):
    # Function to read data from CSV file.
    # Args:
    # file_path : Path to the CSV file.
    # encoding : Encoding of the file. Default is 'latin1'.
    # Returns:
    # DataFrame: The data as pandas DataFrame.
    try:
        data = pd.read_csv(file_path, encoding=encoding)
        logging.info('Data successfully read from the file.')
        return data
    except FileNotFoundError:
        logging.error(f'The file was not found at the specified path: {file_path}')
    except pd.errors.EmptyDataError:
        logging.error('The file is empty.')
    except pd.errors.ParserError:
        logging.error('There was an error parsing the data.')
    except UnicodeDecodeError as error:
        logging.error(f'An encoding error occurred: {error}')
    except Exception as error:
        logging.error(f'An unexpected error occurred: {error}')

def process_data(data_frame):
    # Function to process the data.
    # Args:
    # data_frame (DataFrame): The data read from the CSV file.
    # Returns:
    # DataFrame: The data after processing.
    try:    
        # Drop 'ADDRESSLINE2' column from DataFrame.
        data_frame.drop(columns=['ADDRESSLINE2'], inplace=True, errors='ignore')
            
        # Convert ORDERDATE column to datetime type, invalid parsing will be set as NaT
        data_frame['ORDERDATE'] = pd.to_datetime(data_frame['ORDERDATE'], errors='coerce')
        
        # Fill missing values in key columns with appropriate default values or median
        data_frame['ORDERNUMBER'].fillna('Unknown', inplace=True)
        data_frame['SALES'].fillna(0, inplace=True)  # Assuming missing sales means 0
        
        # Convert PRICEEACH to numeric type, replacing errors with NaN
        data_frame['PRICEEACH'] = pd.to_numeric(data_frame['PRICEEACH'], errors='coerce')
        
        # Fill missing values in PRICEEACH with median or a reasonable value
        median_price = data_frame['PRICEEACH'].median()
        data_frame['PRICEEACH'].fillna(median_price, inplace=True)
        
        # Calculate TOTALVALUE and handle any remaining missing values
        data_frame['TOTALVALUE'] = data_frame['QUANTITYORDERED'] * data_frame['PRICEEACH']
        data_frame.dropna(subset=['QUANTITYORDERED', 'TOTALVALUE'], inplace=True)
        
        # Log any remaining missing values
        missing_values_count = data_frame.isnull().sum().sum()
        if missing_values_count > 0:
            logging.warning(f"Rows with missing values dropped: {missing_values_count}")
        
        logging.info('Data has been processed successfully.')
        return data_frame
    except Exception as error:
        logging.error(f'Error processing data: {error}')
        return None


def update_sql_table(data_frame, connection_string, table_name):
    # Update SQL table processed data.
    # Args:
    # data_frame (DataFrame): processed data.
    # connection_string : SQLAlchemy connection string for database.
    # table_name : name of the table to update.
    # Returns:
    # bool: True if update is successful, False otherwise.
    try:
        engine = create_engine(connection_string)
        data_frame.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info('Data successfully updated in the SQL table.')
        return True
    except OperationalError as error:
        logging.error(f'Error updating SQL table: {error}')
        return False
