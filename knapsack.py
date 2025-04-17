def knapsack_max_protein(items, calorie_limit, item_limit=None):
    """
    Solves the 0/1 Knapsack problem to maximize protein while staying under calorie limit.
    
    Args:
        items: List of tuples (id, calories, protein, item_name, company)
        calorie_limit: Maximum calories allowed
        item_limit: Maximum number of items allowed (optional)
        
    Returns:
        List of selected item IDs that maximize protein while staying under calorie limit
    """
    n = len(items)
    
    # Create a 2D table for dynamic programming
    # dp[i][w] represents the maximum protein for first i items with calorie limit w
    dp = [[0 for _ in range(calorie_limit + 1)] for _ in range(n + 1)]
    
    # Build table in bottom-up manner
    for i in range(1, n + 1):
        item_id, calories, protein, _, _ = items[i-1]
        calories = int(calories)
        
        for w in range(1, calorie_limit + 1):
            if calories <= w:
                # Include the current item
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-calories] + protein)
            else:
                # Cannot include current item
                dp[i][w] = dp[i-1][w]
    
    # Find the items used in the solution
    w = calorie_limit
    selected_items = []
    
    for i in range(n, 0, -1):
        item_id, calories, protein, _, _ = items[i-1]
        calories = int(calories)
        
        # If including this item gives us the optimal solution
        if w >= calories and dp[i][w] != dp[i-1][w]:
            selected_items.append(items[i-1])
            w -= calories
            
            # If we've reached our item limit, stop adding items
            if item_limit is not None and len(selected_items) >= item_limit:
                break
    
    return selected_items

def greedy_max_protein(items, calorie_limit, item_limit=None):
    """
    Uses a greedy approach for large datasets where the knapsack DP solution might be too slow.
    Sorts items by protein-to-calorie ratio and selects them until the limit is reached.
    """
    # Calculate protein-to-calorie ratio for each item
    items_with_ratio = []
    for item in items:
        item_id, calories, protein, item_name, company = item
        if calories > 0:  # Avoid division by zero
            ratio = protein / calories
            items_with_ratio.append((item_id, calories, protein, item_name, company, ratio))
    
    # Sort by ratio (highest first)
    items_with_ratio.sort(key=lambda x: x[5], reverse=True)
    
    selected_items = []
    total_calories = 0
    
    for item in items_with_ratio:
        item_id, calories, protein, item_name, company, _ = item
        if total_calories + calories <= calorie_limit:
            selected_items.append((item_id, calories, protein, item_name, company))
            total_calories += calories
            
            # If we've reached our item limit, stop adding items
            if item_limit is not None and len(selected_items) >= item_limit:
                break
    
    return selected_items

def knapsack_max_calories(items, protein_min, item_limit=None):
    """
    Implements a true knapsack algorithm to maximize calories while meeting a minimum protein requirement.
    """
    # Filter out items with no protein or no calories
    valid_items = [item for item in items if item[1] is not None and item[2] is not None 
                  and item[1] > 0 and item[2] > 0]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    # Use the same approach as knapsack_max_fat
    min_protein_combinations = []
    
    # Sort by calories-to-protein ratio (highest first) for better greedy selection
    valid_items.sort(key=lambda item: item[1]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    # Try all possible combinations up to max_item_count
    def find_combinations(start_idx, current_items, current_protein, current_calories):
        # If we've met the protein minimum, save this combination
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_calories))
            return
        
        # If we've reached the item limit, stop
        if len(current_items) >= max_item_count:
            return
            
        # Try adding each remaining item
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            calories = item[1]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_calories + calories)
            current_items.pop()
    
    # If dataset is too large, use a greedy approach instead
    if n <= 15 and max_item_count <= 4:  # Only use recursive for small datasets
        find_combinations(0, [], 0, 0)
        
        # Find the combination with the maximum calories
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        # Use greedy approach for larger datasets
        selected_items = []
        total_protein = 0
        
        # First, add items until we meet the protein minimum
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_fat(items, protein_min, item_limit=None):
    """
    Implements a true knapsack algorithm to maximize fat while meeting a minimum protein requirement.
    """
    # Filter out items with no protein or no fat data
    valid_items = [item for item in items if item[2] > 0 and item[5] is not None]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    # Scale fat values for DP table if needed
    scale_factor = 1
    max_fat = max(item[5] for item in valid_items)
    if max_fat > 100:
        scale_factor = 2  # Scale down for large fat values
    
    # Create a more efficient approach using a different DP formulation
    # Instead of a 3D table, we'll use a simpler approach
    
    # First, find combinations that meet the protein minimum
    min_protein_combinations = []
    
    # Sort by fat-to-protein ratio (highest first) for better greedy selection
    valid_items.sort(key=lambda item: item[5]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    # Try all possible combinations up to max_item_count
    def find_combinations(start_idx, current_items, current_protein, current_fat):
        # If we've met the protein minimum, save this combination
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_fat))
            return
        
        # If we've reached the item limit, stop
        if len(current_items) >= max_item_count:
            return
            
        # Try adding each remaining item
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            fat = item[5]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_fat + fat)
            current_items.pop()
    
    # If dataset is too large, use a greedy approach instead
    if n <= 15 and max_item_count <= 4:  # Only use recursive for small datasets
        find_combinations(0, [], 0, 0)
        
        # Find the combination with the maximum fat
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        # Use greedy approach for larger datasets
        selected_items = []
        total_protein = 0
        
        # First, add items until we meet the protein minimum
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_carbs(items, protein_min, item_limit=None):
    """
    Implements a true knapsack algorithm to maximize carbs while meeting a minimum protein requirement.
    """
    # Filter out items with no protein or no carbs data
    valid_items = [item for item in items if item[2] > 0 and item[6] is not None]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    # Use the same approach as knapsack_max_fat
    min_protein_combinations = []
    
    # Sort by carbs-to-protein ratio (highest first) for better greedy selection
    valid_items.sort(key=lambda item: item[6]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    # Try all possible combinations up to max_item_count
    def find_combinations(start_idx, current_items, current_protein, current_carbs):
        # If we've met the protein minimum, save this combination
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_carbs))
            return
        
        # If we've reached the item limit, stop
        if len(current_items) >= max_item_count:
            return
            
        # Try adding each remaining item
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            carbs = item[6]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_carbs + carbs)
            current_items.pop()
    
    # If dataset is too large, use a greedy approach instead
    if n <= 15 and max_item_count <= 4:  # Only use recursive for small datasets
        find_combinations(0, [], 0, 0)
        
        # Find the combination with the maximum carbs
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        # Use greedy approach for larger datasets
        selected_items = []
        total_protein = 0
        
        # First, add items until we meet the protein minimum
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_calorie_protein(items, item_limit):
    """
    Finds items that maximize both calories and protein with a limit on items.
    """
    # Filter out items with no calories or protein
    valid_items = [item for item in items if item[1] is not None and item[2] is not None 
                  and item[1] > 0 and item[2] > 0]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    # Calculate a score for each item combining calories and protein
    # Use a reasonable weighting factor that doesn't overly favor one or the other
    # For fast food, calories typically range from 100-1000, while protein ranges from 1-50g
    items_with_score = []
    for item in valid_items:
        item_id, calories, protein, item_name, company = item[:5]
        # Give protein a higher weight to make it equally important to calories
        score = calories + (protein * 20)  # Weight protein higher
        items_with_score.append((item, score))
    
    # Sort by combined score (highest first)
    items_with_score.sort(key=lambda x: x[1], reverse=True)
    
    # Take the top N items (where N is the item_limit)
    selected_items = []
    for i in range(min(item_limit, len(items_with_score))):
        selected_items.append(items_with_score[i][0])
    
    return selected_items