# view_database.py
'''
Concise of the (view_database.py) script.
The script integrates data processing, database updates
Logging: Configures logging to project.log.

Functions:
    * fetch_data_from_db: Connects to an SQLite database, retrieves data and column names.
    * display_data_in_tkinter: Shows the data in a Tkinter window using a Treeview widget, with sorting, row coloring, and scrollbars.
    * sort_by_column: Sorts Treeview data by column.

Main Workflow:
    * Reads and processes data from a CSV file.
    * Updates the database with the processed data.
    * Fetches and displays the data from the database in a Tkinter window.
'''

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from data_processing import read_csv_file, process_data, update_sql_table
import logging

# Configure logging
logging.basicConfig(
    filename='project.log',  # Log file location
    level=logging.INFO,      # Set logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

def fetch_data_from_db(db_path, table_name):
    # Fetch data and column names from the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]  # Extract column names from PRAGMA table_info
        
        # Fetch data
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()
        
        conn.close()
        return data, column_names
    except Exception as e:
        logging.error(f'Error fetching data from database: {e}')
        return None, None

def display_data_in_tkinter(data, column_names):
    root = tk.Tk()
    root.title("Database Viewer")

    # Set window size and position
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    # Create a frame to hold the Treeview and Scrollbars
    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')

    # Check if data is available
    if not data:
        messagebox.showerror("Error", "No data to display.")
        root.destroy()
        return

    # Create Treeview widget
    tree = ttk.Treeview(frame, columns=column_names, show='headings')

    # Style for header
    style = ttk.Style()
    style.configure("Treeview.Heading",
                    background="black",  # Black background for header
                    foreground="black",  # Black text
                    font=("Helvetica", 10, "bold"))

    # Style for Treeview
    style.configure("Treeview",
                    background="white",  # White background for rows
                    foreground="black")
    style.map("Treeview",
              background=[('selected', '#c0c0c0')])  # Light gray background for selected row

    # Set the column headings and bind click event for sorting
    for col in column_names:
        tree.heading(col, text=col, command=lambda _col=col: sort_by_column(tree, _col, False))

    # Insert data into the Treeview
    for index, row in enumerate(data):
        tag = 'even' if index % 2 == 0 else 'odd'
        tree.insert('', 'end', values=row, tags=(tag,))

    # Configure row colors
    tree.tag_configure('even', background='white')
    tree.tag_configure('odd', background='#f0f0f0')  # Light gray background for odd rows

    # Create vertical scrollbar and link it to the Treeview
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')

    # Create horizontal scrollbar and link it to the Treeview
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.pack(side='bottom', fill='x')

    # Pack the Treeview
    tree.pack(expand=True, fill='both')

    # Display the total number of rows at the bottom of the window
    total_rows = len(data)
    total_label = tk.Label(root, text=f"Total rows: {total_rows}", font=("Helvetica", 10))
    total_label.pack(side='bottom', pady=10)

    root.mainloop()

def sort_by_column(tree, col, descending):
    # Sort the table by column
    # Get all the data in the Treeview
    data = [(tree.set(k, col), k) for k in tree.get_children('')]

    # Sort the data by the given column
    data.sort(reverse=descending)

    # Rearrange items in the Treeview based on the sorted data
    for index, (val, k) in enumerate(data):
        tree.move(k, '', index)

    # Reverse the sort order for the next click
    tree.heading(col, command=lambda: sort_by_column(tree, col, not descending))

if __name__ == "__main__":
    # Specify file path and database path
    file_path = r'C:\Users\AHMAD\Desktop\Kunskapskontroll_2\Final\sales_data_sample.csv'
    db_path = 'example.db'
    table_name = 'sales_data'
    connection_string = f'sqlite:///{db_path}'

    # Read, process, and save data using the imported functions
    data_frame = read_csv_file(file_path)
    if data_frame is not None:
        processed_data = process_data(data_frame)
        update_sql_table(processed_data, connection_string, table_name)

    # Fetch data and column names from the database and display in Tkinter
    data, column_names = fetch_data_from_db(db_path, table_name)
    if data:
        display_data_in_tkinter(data, column_names)
    else:
        messagebox.showerror("Error", "No data found in the database.")