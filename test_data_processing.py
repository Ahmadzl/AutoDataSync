# test_data_processing.py
'''
Concise of the (test_data_processing.py) script.
Runs the unit tests when the script is executed directly.
Setup:
    * File Path and Database Connection: Defines the path to the CSV file, SQL connection string, and table name.
    * Data Preparation: Reads the CSV file and processes the data using functions from data_processing.py.
    * If reading fails, initializes processed_data as an empty DataF.

Tests:
test_data_processing:
    * Ensures that the processed DataFrame is not empty.
    * Checks that the TOTALVALUE column is present.
    * Ensuring that 'ADDRESSLINE2' column has been removed.
    * Verifies that the TOTALVALUE column is numeric.

test_update_sql_table:
    * Tests the update_sql_table function to ensure that data is successfully updated in the SQL table.
'''

import unittest
import pandas as pd
from data_processing import read_csv_file, process_data, update_sql_table

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        # Set up file path, connection string and table name for tests.
        self.file_path = r'C:\Users\AHMAD\Desktop\Kunskapskontroll_2\Final\sales_data_sample.csv'
        self.connection_string = 'sqlite:///example.db'  # Replace with your actual connection string.
        self.table_name = 'sales_data'
        
        self.data_frame = read_csv_file(self.file_path) # Load CSV file into Data.

        if self.data_frame is not None:
            self.processed_data = process_data(self.data_frame)
        else:
            self.processed_data = pd.DataFrame()

    def test_data_processing(self):
        self.assertFalse(self.processed_data.empty, "Processed data should not be empty.")
        self.assertIn('TOTALVALUE', self.processed_data.columns, "'TOTALVALUE' column should be in the processed data.")
        self.assertNotIn('ADDRESSLINE2', self.processed_data.columns, "'ADDRESSLINE2' column should not be in the processed data.")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.processed_data['TOTALVALUE']), "'TOTALVALUE' column should be numeric.")

    def test_update_sql_table(self):
        result = update_sql_table(self.processed_data, self.connection_string, self.table_name)
        self.assertTrue(result, "Data should be updated successfully in the SQL table.")

if __name__ == '__main__':
    unittest.main()
