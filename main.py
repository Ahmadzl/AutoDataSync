# main.py
'''
Concise of the (main.py) script.
The script handles these tasks and displays results to the user,     while ensuring that all steps and errors are logged.

* Sets up logging: Records information and errors in a file named project.log.
* Read data: Loads data from a CSV file and logs any issues if they arise.
* Processes data: Processes the loaded data and logs errors if processing fails.
* Updates the database: Updates an SQL database with the processed data, logging whether the update was successful or not.
'''

import logging
from data_processing import read_csv_file, process_data, update_sql_table

# Configure logging
logging.basicConfig(
    filename='project.log',  # Log file location
    level=logging.INFO,      # Set logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

file_path = r'C:\Users\AHMAD\Desktop\Kunskapskontroll_2\Final\sales_data_sample.csv'
connection_string = 'sqlite:///example.db'  # Replace with your actual connection string
table_name = 'sales_data'

def main():
    logging.info('Starting data processing script.')

    # Read the data
    try:
        data_frame = read_csv_file(file_path)
        if data_frame is None:
            logging.error('Failed to load data from CSV file.')
            print("No data was loaded. Please check the errors above.")
            return
        logging.info('Data successfully loaded from CSV file.')
    except Exception as error:
        logging.error(f'Error reading CSV file: {error}')
        print("Error reading CSV file. Please check the log for details.")
        return

    # Process the data if available
    try:
        processed_data = process_data(data_frame)
        logging.info('Data processing completed.')
        print(processed_data.head())  # Display the first 5 rows of the processed data
    except Exception as error:
        logging.error(f'Error processing data: {error}')
        print("Error processing data. Please check the log for details.")
        return

    # Update SQL table
    try:
        update_success = update_sql_table(processed_data, connection_string, table_name)
        if update_success:
            logging.info('Data successfully updated in the SQL table.')
            print("Data successfully updated in the SQL table.")
        else:
            logging.warning('Data update failed.')
            print("Data update failed.")
    except Exception as eerror:
        logging.error(f'Error updating SQL table: {error}')
        print("Error updating SQL table. Please check the log for details.")

if __name__ == '__main__':
    main()
