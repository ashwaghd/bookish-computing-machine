#!/usr/bin/env python3
import csv
import sqlite3
import os

def create_database():
    # Remove existing database if it exists
    if os.path.exists('fast_food.db'):
        os.remove('fast_food.db')
    
    # Connect to database
    conn = sqlite3.connect('fast_food.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fast_food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        item TEXT,
        calories INTEGER,
        calories_from_fat INTEGER,
        total_fat REAL,
        saturated_fat REAL,
        trans_fat REAL,
        cholesterol REAL,
        sodium REAL,
        carbs REAL,
        fiber REAL,
        sugars REAL,
        protein REAL,
        weight_watchers_points REAL
    )
    ''')
    
    # Read CSV and insert data
    with open('nutrition/FastFoodNutritionMenuV3.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            # Clean and convert data
            cleaned_row = []
            for i, value in enumerate(row):
                # Skip empty cells or convert to appropriate type
                if value.strip() == '':
                    cleaned_row.append(None)
                elif i >= 2:  # Numeric columns
                    # Remove any non-numeric characters (like '<' in '<5')
                    cleaned_value = ''.join(c for c in value if c.isdigit() or c == '.' or c == '-')
                    if cleaned_value == '':
                        cleaned_row.append(None)
                    else:
                        try:
                            cleaned_row.append(float(cleaned_value))
                        except ValueError:
                            cleaned_row.append(None)
                else:  # Text columns
                    cleaned_row.append(value)
            
            # Insert data
            if len(cleaned_row) >= 13:  # Ensure we have at least the essential columns
                cursor.execute('''
                INSERT INTO fast_food_items (
                    company, item, calories, calories_from_fat, total_fat, saturated_fat,
                    trans_fat, cholesterol, sodium, carbs, fiber, sugars, protein, weight_watchers_points
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', cleaned_row[:14])  # Limit to expected columns
    
    # Create indices for faster searching
    cursor.execute('CREATE INDEX idx_company ON fast_food_items(company)')
    cursor.execute('CREATE INDEX idx_calories ON fast_food_items(calories)')
    cursor.execute('CREATE INDEX idx_protein ON fast_food_items(protein)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully!")

if __name__ == "__main__":
    create_database() 