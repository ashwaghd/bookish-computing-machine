#!/usr/bin/env python3
import argparse
import sqlite3
from knapsack import knapsack_max_protein, greedy_max_protein, knapsack_max_calories, knapsack_max_fat, knapsack_max_carbs, knapsack_max_calorie_protein
import os

def get_db_connection():
    """Connect to the database and return the connection object."""
    if not os.path.exists('fast_food.db'):
        print("Error: Database file not found. Run create_database.py first.")
        exit(1)
        
    return sqlite3.connect('fast_food.db')

def list_companies(args):
    """List all companies in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT company FROM fast_food_items ORDER BY company')
    companies = cursor.fetchall()
    
    print("Available companies:")
    for company in companies:
        print(f"- {company[0]}")
    
    conn.close()

def list_items(args):
    """List items with optional filtering by company."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT company, item, calories, protein FROM fast_food_items'
    params = []
    
    if args.company:
        query += ' WHERE company LIKE ?'
        params.append(f'%{args.company}%')
    
    query += ' ORDER BY company, item'
    
    cursor.execute(query, params)
    items = cursor.fetchall()
    
    if items:
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Protein (g)':<10}")
        print("-" * 90)
        for company, item, calories, protein in items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {protein:<10}")
    else:
        print("No items found matching your criteria.")
    
    conn.close()

def max_protein(args):
    """Find items that maximize protein within a calorie limit."""
    calorie_limit = args.calories
    item_limit = args.items
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, calories, protein, item, company 
    FROM fast_food_items 
    WHERE calories IS NOT NULL AND protein IS NOT NULL AND calories > 0
    '''
    
    if args.company:
        query += ' AND company LIKE ?'
        cursor.execute(query, [f'%{args.company}%'])
    else:
        cursor.execute(query)
    
    items = cursor.fetchall()
    
    if not items:
        print("No suitable items found.")
        conn.close()
        return
    
    print(f"Finding max protein meals within {calorie_limit} calories...")
    if item_limit:
        print(f"Limited to a maximum of {item_limit} items.")
    
    # Always display algorithm name
    algorithm_name = ""
    
    # Choose algorithm based on problem size
    if len(items) > 100 and calorie_limit > 1000:
        algorithm_name = "Greedy heuristic (not knapsack - using protein-to-calorie ratio)"
        print(f"Using {algorithm_name}...")
        selected_items = greedy_max_protein(items, calorie_limit, item_limit)
    else:
        algorithm_name = "Optimal 0/1 knapsack with dynamic programming"
        print(f"Using {algorithm_name}...")
        selected_items = knapsack_max_protein(items, calorie_limit, item_limit)
    
    if selected_items:
        total_calories = sum(item[1] for item in selected_items)
        total_protein = sum(item[2] for item in selected_items)
        
        print("\nSelected items:")
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Protein (g)':<10}")
        print("-" * 90)
        
        for _, calories, protein, item, company in selected_items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {protein:<10}")
        
        print("\nSummary:")
        print(f"Total items: {len(selected_items)}")
        print(f"Total calories: {total_calories}")
        print(f"Total protein: {total_protein:.2f}g")
        print(f"Protein/calorie ratio: {total_protein/total_calories:.4f}g per calorie")
    else:
        print("No solution found. Try increasing the calorie limit.")
    
    conn.close()

def max_calories(args):
    """Find items that maximize calories while meeting a minimum protein requirement."""
    protein_min = args.protein
    item_limit = args.items
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, calories, protein, item, company 
    FROM fast_food_items 
    WHERE calories IS NOT NULL AND protein IS NOT NULL AND protein > 0
    '''
    
    if args.company:
        query += ' AND company LIKE ?'
        cursor.execute(query, [f'%{args.company}%'])
    else:
        cursor.execute(query)
    
    items = cursor.fetchall()
    
    if not items:
        print("No suitable items found.")
        conn.close()
        return
    
    print(f"Finding max calorie meals with at least {protein_min}g of protein...")
    if item_limit:
        print(f"Limited to a maximum of {item_limit} items.")
    
    algorithm_name = "Mixed approach: exhaustive search for small datasets, greedy for large"
    print(f"Using {algorithm_name}...")
    
    # Use the new knapsack function
    selected_items = knapsack_max_calories(items, protein_min, item_limit)
    
    if selected_items:
        total_calories = sum(item[1] for item in selected_items)
        total_protein = sum(item[2] for item in selected_items)
        
        print("\nSelected items:")
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Protein (g)':<10}")
        print("-" * 90)
        
        for _, calories, protein, item, company in selected_items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {protein:<10}")
        
        print("\nSummary:")
        print(f"Total items: {len(selected_items)}")
        print(f"Total calories: {total_calories}")
        print(f"Total protein: {total_protein:.2f}g")
        print(f"Calorie/protein ratio: {total_calories/total_protein:.2f} calories per gram of protein")
    else:
        print("No solution found. Try decreasing the protein requirement.")
    
    conn.close()

def max_fat(args):
    """Find items that maximize total fat while meeting a minimum protein requirement."""
    protein_min = args.protein
    item_limit = args.items
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, calories, protein, item, company, total_fat
    FROM fast_food_items 
    WHERE protein IS NOT NULL AND protein > 0 AND total_fat IS NOT NULL
    '''
    
    if args.company:
        query += ' AND company LIKE ?'
        cursor.execute(query, [f'%{args.company}%'])
    else:
        cursor.execute(query)
    
    items = cursor.fetchall()
    
    if not items:
        print("No suitable items found.")
        conn.close()
        return
    
    print(f"Finding max fat meals with at least {protein_min}g of protein...")
    if item_limit:
        print(f"Limited to a maximum of {item_limit} items.")
        
    algorithm_name = "Mixed approach: exhaustive search for small datasets, greedy for large"
    print(f"Using {algorithm_name}...")
    
    # Use the new knapsack function
    selected_items = knapsack_max_fat(items, protein_min, item_limit)
    
    if selected_items:
        total_calories = sum(item[1] for item in selected_items if item[1] is not None)
        total_protein = sum(item[2] for item in selected_items)
        total_fat = sum(item[5] for item in selected_items)
        
        print("\nSelected items:")
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Fat (g)':<10} {'Protein (g)':<10}")
        print("-" * 110)
        
        for _, calories, protein, item, company, fat in selected_items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {fat:<10} {protein:<10}")
        
        print("\nSummary:")
        print(f"Total items: {len(selected_items)}")
        print(f"Total calories: {total_calories}")
        print(f"Total fat: {total_fat:.2f}g")
        print(f"Total protein: {total_protein:.2f}g")
        print(f"Fat/protein ratio: {total_fat/total_protein:.2f}g of fat per gram of protein")
    else:
        print("No solution found. Try decreasing the protein requirement.")
    
    conn.close()

def max_carbs(args):
    """Find items that maximize carbs while meeting a minimum protein requirement."""
    protein_min = args.protein
    item_limit = args.items
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, calories, protein, item, company, total_fat, carbs
    FROM fast_food_items 
    WHERE protein IS NOT NULL AND protein > 0 AND carbs IS NOT NULL
    '''
    
    if args.company:
        query += ' AND company LIKE ?'
        cursor.execute(query, [f'%{args.company}%'])
    else:
        cursor.execute(query)
    
    items = cursor.fetchall()
    
    if not items:
        print("No suitable items found.")
        conn.close()
        return
    
    print(f"Finding max carbs meals with at least {protein_min}g of protein...")
    if item_limit:
        print(f"Limited to a maximum of {item_limit} items.")
        
    algorithm_name = "Mixed approach: exhaustive search for small datasets, greedy for large"
    print(f"Using {algorithm_name}...")
    
    # Use the new knapsack function
    selected_items = knapsack_max_carbs(items, protein_min, item_limit)
    
    if selected_items:
        total_calories = sum(item[1] for item in selected_items if item[1] is not None)
        total_protein = sum(item[2] for item in selected_items)
        total_carbs = sum(item[6] for item in selected_items)
        
        print("\nSelected items:")
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Carbs (g)':<10} {'Protein (g)':<10}")
        print("-" * 110)
        
        for _, calories, protein, item, company, _, carbs in selected_items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {carbs:<10} {protein:<10}")
        
        print("\nSummary:")
        print(f"Total items: {len(selected_items)}")
        print(f"Total calories: {total_calories}")
        print(f"Total carbs: {total_carbs:.2f}g")
        print(f"Total protein: {total_protein:.2f}g")
        print(f"Carbs/protein ratio: {total_carbs/total_protein:.2f}g of carbs per gram of protein")
    else:
        print("No solution found. Try decreasing the protein requirement.")
    
    conn.close()

def max_calorie_protein(args):
    """Find items that maximize both calories and protein with a limit on items."""
    item_limit = args.items if args.items else 5  # Default to 5 items if not specified
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, calories, protein, item, company 
    FROM fast_food_items 
    WHERE calories IS NOT NULL AND protein IS NOT NULL AND calories > 0 AND protein > 0
    '''
    
    if args.company:
        query += ' AND company LIKE ?'
        cursor.execute(query, [f'%{args.company}%'])
    else:
        cursor.execute(query)
    
    items = cursor.fetchall()
    
    if not items:
        print("No suitable items found.")
        conn.close()
        return
    
    print(f"Finding maximum calorie-protein combination with {item_limit} items...")
    print("Using top-K selection with weighted calorie-protein scoring")
    
    # Use the new function
    selected_items = knapsack_max_calorie_protein(items, item_limit)
    
    if selected_items:
        total_calories = sum(item[1] for item in selected_items)
        total_protein = sum(item[2] for item in selected_items)
        
        print("\nSelected items:")
        print(f"{'Company':<20} {'Item':<50} {'Calories':<10} {'Protein (g)':<10}")
        print("-" * 90)
        
        for _, calories, protein, item, company in selected_items:
            print(f"{company[:19]:<20} {item[:49]:<50} {calories:<10} {protein:<10}")
        
        print("\nSummary:")
        print(f"Total items: {len(selected_items)}")
        print(f"Total calories: {total_calories}")
        print(f"Total protein: {total_protein:.2f}g")
        print(f"Calories/item: {total_calories/len(selected_items):.1f}")
        print(f"Protein/item: {total_protein/len(selected_items):.1f}g")
    else:
        print("No solution found.")
    
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Fast Food Nutrition Database CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List companies command
    companies_parser = subparsers.add_parser('companies', help='List all companies')
    companies_parser.set_defaults(func=list_companies)
    
    # List items command
    items_parser = subparsers.add_parser('items', help='List food items')
    items_parser.add_argument('--company', help='Filter by company name (partial match)')
    items_parser.set_defaults(func=list_items)
    
    # Max protein command
    max_protein_parser = subparsers.add_parser('max-protein', help='Find items that maximize protein within calorie limit')
    max_protein_parser.add_argument('calories', type=int, help='Maximum calorie limit')
    max_protein_parser.add_argument('--company', help='Filter by company name (partial match)')
    max_protein_parser.add_argument('--items', type=int, help='Maximum number of items to include')
    max_protein_parser.set_defaults(func=max_protein)
    
    # Max calories command
    max_calories_parser = subparsers.add_parser('max-calories', help='Find items that maximize calories while meeting protein minimum')
    max_calories_parser.add_argument('protein', type=int, help='Minimum protein required (grams)')
    max_calories_parser.add_argument('--company', help='Filter by company name (partial match)')
    max_calories_parser.add_argument('--items', type=int, help='Maximum number of items to include')
    max_calories_parser.set_defaults(func=max_calories)
    
    # Max fat command
    max_fat_parser = subparsers.add_parser('max-fat', help='Find items that maximize total fat while meeting protein minimum')
    max_fat_parser.add_argument('protein', type=int, help='Minimum protein required (grams)')
    max_fat_parser.add_argument('--company', help='Filter by company name (partial match)')
    max_fat_parser.add_argument('--items', type=int, help='Maximum number of items to include')
    max_fat_parser.set_defaults(func=max_fat)
    
    # Max carbs command
    max_carbs_parser = subparsers.add_parser('max-carbs', help='Find items that maximize carbs while meeting protein minimum')
    max_carbs_parser.add_argument('protein', type=int, help='Minimum protein required (grams)')
    max_carbs_parser.add_argument('--company', help='Filter by company name (partial match)')
    max_carbs_parser.add_argument('--items', type=int, help='Maximum number of items to include')
    max_carbs_parser.set_defaults(func=max_carbs)
    
    # Add the new max-calorie-protein command
    max_calorie_protein_parser = subparsers.add_parser('max-calorie-protein', 
                                                     help='Find items that maximize both calories and protein')
    max_calorie_protein_parser.add_argument('--items', type=int, default=5, 
                                          help='Maximum number of items to include (default: 5)')
    max_calorie_protein_parser.add_argument('--company', help='Filter by company name (partial match)')
    max_calorie_protein_parser.set_defaults(func=max_calorie_protein)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()