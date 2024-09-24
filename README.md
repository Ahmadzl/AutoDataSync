Data Processing and Display Project

Project :
1- Reads and processes data from a CSV file.
2- Updates the database with the processed data.
3- Fetches data from the database and displays it in a Tkinter window.

This project consists of several scripts that work together to load, process, update, and display data.

Libraries Used :
* pandas
* sqlalchemy
* sqlite3
* tkinter
* unittest

Scripts
1- main.py
This is the main script for the project. 
It performs the following tasks:
    Setup Logging: Configures logging to record events and errors in a file named (project.log).
    Read Data: Loads data from CSV file and logs any issues that arise during this process.
    Process Data: Processes the loaded data and logs errors if the processing fails.
    Update Database: Updates SQL database with the processed data and logs whether the update was successful.

Requirements:
CSV file containing the data.
SQL database connection string (update connection_string with your actual database connection details).

*** Before running the script make sure that the file_path and connection_string are set correctly ***
*** Execute the script (python main.py) ***

2- data_processing.py
This is the data processing and database updates script for the project. 
Includes the following functions:
    Logging Setup: Configures logging to record events and errors in (project.log).
    read_csv_file Function: Reads data from CSV file into a DataFrame, handling various errors like file not found, empty file, parsing issues and encoding errors.
    process_data Function: Processes the DataFrame by converting columns to the appropriate types and adding a new calculated column. Logs successful processing or errors.
    update_sql_table Function: Updates SQL table with the processed data using SQLAlchemy. 
    Logs success or failure and returns a boolean indicating the result.

*** No direct execution is required *** 
*** This script is used internally and imported by other scripts. No direct execution is required ***

3- test_data_processing.py
This script is used for unit testing the functions in data_processing.py. 
It checks that data processing and database updates work as expected.
Includes the following functions:
    Data Processing Test: Verifies that the processed DataFrame is not empty, contains the TOTALVALUE column, and that this column is numeric.
    Database Update Test: Ensures that the update_sql_table function updates the SQL table successfully.

*** Execute the script  to verify functionality (python test_data_processing.py) ***

4-view_database.py
Displays data from the database in Tkinter window. 
Includes the following functions:
    Logging Setup: Configures logging to (project.log).
    fetch_data_from_db Function: Connects to SQLite database to retrieve data and column names.
    display_data_in_tkinter Function: Shows the data in a Tkinter window using a Treeview widget with support for sorting, row coloring, and scrollbars.
    sort_by_column Function: Sorts the Treeview data by the selected column.

*** Execute the script (python view_database.py) ***

Each script has been crafted to make your workflow smoother and more efficient. 
I drew inspiration from my own experience dealing with large datasets in previous projects.

While developing this project, I remembered a time when data presented a major challenge and I needed a quick solution.

I know that working with data can sometimes be complex but I’m confident that these tools will help simplify things.

If you encounter any difficulties try searching online often solutions are closer than you might think.

I hope this project helps streamline your data processing and visualization tasks and proves useful for you. 

This project uses a free and experimental dataset sourced from Kaggle. 
Please note that this data is for experimental purposes only and may not fully represent real-world data. 
For more information about the dataset and its usage you can visit the (https://www.kaggle.com/) 

If you have any suggestions or run into issues, I'd love to hear from you at (ahmadzl@hotmail.com). 
Thank you for using me project.
Enjoy working with your data!

*** Note:**
*** I have set up a Task Scheduler by named 'Data Processing and SQL Update Task' to run automatically at specific times. ***
*** That data processing and SQL database updates as scheduled. ***
