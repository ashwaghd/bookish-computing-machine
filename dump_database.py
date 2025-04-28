#!/usr/bin/env python3
import csv
import sqlite3
import os

def dump_database(output_file='nutrition/fast_food_dump.csv'):
    # Connect to database
    conn = sqlite3.connect('fast_food.db')
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute('PRAGMA table_info(fast_food_items)')
    columns = [info[1] for info in cursor.fetchall()]
    columns.pop(0)  # Remove the ID column
    
    # Get all data
    cursor.execute('SELECT * FROM fast_food_items')
    rows = cursor.fetchall()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(columns)  # Write header
        
        for row in rows:
            csv_writer.writerow(row[1:])  # Skip the ID column
    
    conn.close()
    print(f"Database dumped to {output_file} successfully!")

if __name__ == "__main__":
    dump_database() 