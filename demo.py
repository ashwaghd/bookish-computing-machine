#!/usr/bin/env python3
import subprocess
import time
import os
import sys

def run_command(command, description=None):
    """Run a command with a description and wait for user input to continue."""
    if description:
        print("\n" + "=" * 80)
        print(f"\n{description}\n")
        print("=" * 80 + "\n")
    
    print(f"Running: {command}\n")
    
    # Short pause with countdown before executing
    print("\nWaiting 10 seconds before next command (press Enter to continue sooner)...")
    for i in range(10, 0, -1):
        sys.stdout.write(f"\r{i} seconds... ")
        sys.stdout.flush()
         # Allow user to skip the wait by pressing Enter
        if os.name == 'nt':  # Windows
            import msvcrt
            if msvcrt.kbhit():
                if msvcrt.getch() == b'\r':
                    break
            time.sleep(1)
        else:  # Unix/Linux/Mac
            import select
            if select.select([sys.stdin], [], [], 1)[0]:
                sys.stdin.readline()
                break
    
    sys.stdout.write("\rExecuting now!\n\n")
    sys.stdout.flush()
    
    # Run the command
    process = subprocess.run(command, shell=True, text=True)
    
    # Wait between commands
    print("\nWaiting 10 seconds before next command (press Enter to continue sooner)...")
    for i in range(10, 0, -1):
        sys.stdout.write(f"\rContinuing in {i} seconds... ")
        sys.stdout.flush()
        
        # Allow user to skip the wait by pressing Enter
        if os.name == 'nt':  # Windows
            import msvcrt
            if msvcrt.kbhit():
                if msvcrt.getch() == b'\r':
                    break
            time.sleep(1)
        else:  # Unix/Linux/Mac
            import select
            if select.select([sys.stdin], [], [], 1)[0]:
                sys.stdin.readline()
                break
    
    print("\n")

def main():
    print("\n" + "=" * 80)
    print("\nFAST FOOD NUTRITION DATABASE CLI DEMO\n")
    print("By: Trenonn Shumway, Schuyler Baer, and Ash Wagner\n")
    print("=" * 80 + "\n")
    print("This demo will showcase the main features of the Fast Food Nutrition CLI.")
    print("Press Enter at any time during the wait to proceed to the next command.\n")
    
    # Create the database
    run_command("python3 create_database.py", "Creating the database from CSV files")
    
    # List all companies
    run_command("python3 nutrition_cli.py companies", "Listing all fast food companies in the database")
    
    # List items for a specific company
    run_command("python3 nutrition_cli.py items --company 'McDonald'", 
                "Listing all items from McDonald's")
    
    # Max protein within calorie limit
    run_command("python3 nutrition_cli.py max-protein 1000 --algorithm dp", 
                "Finding items that maximize protein within 1000 calories using dynamic programming")
    
    # Max protein with company filter
    run_command("python3 nutrition_cli.py max-protein 1500 --company 'Wendy' --algorithm greedy", 
                "Finding Wendys items that maximize protein within 1500 calories using greedy algorithm")
    
    # Max protein with item limit
    run_command("python3 nutrition_cli.py max-protein 2000 --items 3 --algorithm ilp", 
                "Finding up to 3 items that maximize protein within 2000 calories using ILP")
    
    # Max calories with protein minimum
    run_command("python3 nutrition_cli.py max-calories 30", 
                "Finding items that maximize calories while providing at least 30g of protein")
    
    # Max fat with protein minimum
    run_command("python3 nutrition_cli.py max-fat 25 --company 'KFC'", 
                "Finding KFC items that maximize fat while providing at least 25g of protein")
    
    # Max carbs with protein minimum
    run_command("python3 nutrition_cli.py max-carbs 20 --items 2", 
                "Finding up to 2 items that maximize carbs while providing at least 20g of protein")
    
    # Max calorie-protein balance
    run_command("python3 nutrition_cli.py max-calorie-protein --items 3 --algorithm weighted", 
                "Finding up to 3 items that maximize both calories and protein using weighted scoring")
    
    print("\n" + "=" * 80)
    print("\nDEMO COMPLETED\n")
    print("=" * 80 + "\n")
    print("You've seen the main features of the Fast Food Nutrition CLI.")
    print("Feel free to explore more commands as described in the README.md file.\n")

if __name__ == "__main__":
    main()
