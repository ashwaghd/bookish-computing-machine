![Screenshot from 2025-04-29 16-24-49](https://github.com/user-attachments/assets/aedc637a-7f55-477c-b99f-8a1bc3040a7f)
# Fast Food Nutrition Database CLI

A command-line application for analyzing fast food nutrition data using various optimization algorithms. This tool helps users find the best combinations of fast food items to maximize or balance nutritional values.

## Setup Instructions

1. **Set up the database**
   ```
   python3 create_database.py
   ```
   This will create a SQLite database from the CSV files in the nutrition folder.

2. **For Integer Linear Programming (optional)**
   ```
   pip3 install pulp
   ```
   This installs the PuLP library needed for ILP optimization.

3. **Run the CLI commands**
   ```
   python3 nutrition_cli.py [command] [arguments]
   ```

## Available Commands

### List Companies
Lists all fast food companies in the database.

```
python3 nutrition_cli.py companies
```

### List Items
Lists all food items, optionally filtered by company name.

```
python3 nutrition_cli.py items [--company COMPANY]
```

**Examples:**
```
python3 nutrition_cli.py items
python3 nutrition_cli.py items --company "McDonald"
```

### Max Protein
Finds items that maximize protein within a specified calorie limit.

```
python3 nutrition_cli.py max-protein CALORIES [--company COMPANY] [--items ITEMS] [--algorithm {dp,greedy,ilp}]
```

**Parameters:**
- `CALORIES`: Maximum calorie limit
- `--company`: (Optional) Filter by company name
- `--items`: (Optional) Maximum number of items to include
- `--algorithm`: (Optional) Algorithm to use:
  - `dp`: Dynamic programming (optimal for small datasets)
  - `greedy`: Greedy heuristic (faster for large datasets)
  - `ilp`: Integer Linear Programming (optimal solution, requires PuLP)

**Examples:**
```
python3 nutrition_cli.py max-protein 1000
python3 nutrition_cli.py max-protein 1500 --company "McDonald" --algorithm ilp
python3 nutrition_cli.py max-protein 2000 --items 3 --algorithm greedy
```

### Max Calories
Finds items that maximize calories while meeting a minimum protein requirement.

```
python3 nutrition_cli.py max-calories PROTEIN [--company COMPANY] [--items ITEMS] [--algorithm {mixed,ilp}]
```

**Parameters:**
- `PROTEIN`: Minimum protein required (grams)
- `--company`: (Optional) Filter by company name
- `--items`: (Optional) Maximum number of items to include
- `--algorithm`: (Optional) Algorithm to use:
  - `mixed`: Mixed approach using exhaustive search for small datasets, greedy for large
  - `ilp`: Integer Linear Programming (optimal solution, requires PuLP)

**Examples:**
```
python3 nutrition_cli.py max-calories 30
python3 nutrition_cli.py max-calories 25 --company "KFC" --algorithm ilp
python3 nutrition_cli.py max-calories 40 --items 2
```

### Max Fat
Finds items that maximize total fat while meeting a minimum protein requirement.

```
python3 nutrition_cli.py max-fat PROTEIN [--company COMPANY] [--items ITEMS] [--algorithm {mixed,ilp}]
```

**Parameters:**
- `PROTEIN`: Minimum protein required (grams)
- `--company`: (Optional) Filter by company name
- `--items`: (Optional) Maximum number of items to include
- `--algorithm`: (Optional) Algorithm to use:
  - `mixed`: Mixed approach using exhaustive search for small datasets, greedy for large
  - `ilp`: Integer Linear Programming (optimal solution, requires PuLP)

**Examples:**
```
python3 nutrition_cli.py max-fat 30
python3 nutrition_cli.py max-fat 25 --company "Burger King" --algorithm ilp
python3 nutrition_cli.py max-fat 20 --items 3
```

### Max Carbs
Finds items that maximize carbohydrates while meeting a minimum protein requirement.

```
python3 nutrition_cli.py max-carbs PROTEIN [--company COMPANY] [--items ITEMS] [--algorithm {mixed,ilp}]
```

**Parameters:**
- `PROTEIN`: Minimum protein required (grams)
- `--company`: (Optional) Filter by company name
- `--items`: (Optional) Maximum number of items to include
- `--algorithm`: (Optional) Algorithm to use:
  - `mixed`: Mixed approach using exhaustive search for small datasets, greedy for large
  - `ilp`: Integer Linear Programming (optimal solution, requires PuLP)

**Examples:**
```
python3 nutrition_cli.py max-carbs 20
python3 nutrition_cli.py max-carbs 15 --company "Pizza Hut" --algorithm ilp
python3 nutrition_cli.py max-carbs 25 --items 2
```

### Max Calorie-Protein
Finds items that maximize both calories and protein with a limit on the number of items.

```
python3 nutrition_cli.py max-calorie-protein [--items ITEMS] [--company COMPANY] [--algorithm {weighted,ilp}]
```

**Parameters:**
- `--items`: (Optional) Maximum number of items to include (default: 5)
- `--company`: (Optional) Filter by company name
- `--algorithm`: (Optional) Algorithm to use:
  - `weighted`: Weighted scoring approach (default)
  - `ilp`: Integer Linear Programming (optimal solution, requires PuLP)

**Examples:**
```
python3 nutrition_cli.py max-calorie-protein
python3 nutrition_cli.py max-calorie-protein --items 3 --algorithm ilp
python3 nutrition_cli.py max-calorie-protein --company "McDonald" --items 2
```

## Algorithms Used

The application offers multiple optimization algorithms:

1. **Dynamic Programming (Knapsack)**
   - Used by: max-protein (with --algorithm dp)
   - Finds the mathematically optimal solution for the classic knapsack problem
   - Works well for smaller datasets but can be memory-intensive for large problems

2. **Greedy Heuristic**
   - Used by: max-protein (with --algorithm greedy)
   - Sorts items by protein-to-calorie ratio and selects them sequentially
   - Fast but may not find the optimal solution

3. **Mixed Approach**
   - Used by: max-calories, max-fat, max-carbs (with --algorithm mixed)
   - Uses exhaustive search for smaller datasets to find the optimal solution
   - Falls back to a greedy algorithm for larger datasets to maintain performance

4. **Weighted Scoring**
   - Used by: max-calorie-protein (with --algorithm weighted)
   - Ranks items by a weighted score that balances calories and protein
   - Selects the top N items with the highest combined scores

5. **Integer Linear Programming (ILP)**
   - Available for all optimization commands with --algorithm ilp
   - Finds the mathematically optimal solution using the PuLP library
   - Can handle larger datasets than dynamic programming
   - Requires the PuLP library to be installed

## Use Cases

- **Bodybuilders**: Use `max-protein` to find meals with maximum protein for muscle building
- **Bulking**: Use `max-calories` or `max-calorie-protein` to find calorie-dense meals
- **Keto Diet**: Use `max-fat` with a low carb filter to find keto-friendly options
- **Carb Loading**: Use `max-carbs` to find high-carbohydrate meal combinations

## Database Management

- To dump the database to CSV:
  ```
  python3 dump_database.py
  ```

- To rebuild the database:
  ```
  python3 create_database.py
  ```

## About Integer Linear Programming (ILP)

Integer Linear Programming is a mathematical optimization technique that finds the best solution to a problem with constraints. In this application:

- ILP provides mathematically optimal solutions (unlike greedy approaches)
- It can handle larger datasets than dynamic programming
- It's more flexible for complex constraints
- The implementation uses PuLP, a Python library that interfaces with various ILP solvers

To use ILP, add `--algorithm ilp` to any optimization command. If PuLP is not installed, the application will automatically fall back to the default algorithm.
