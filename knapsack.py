# sat solver , integer linear programming

def knapsack_max_protein(items, calorie_limit, item_limit=None):
    n = len(items)
    
    dp = [[0 for _ in range(calorie_limit + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item_id, calories, protein, _, _ = items[i-1]
        calories = int(calories)
        
        for w in range(1, calorie_limit + 1):
            if calories <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-calories] + protein)
            else:
                dp[i][w] = dp[i-1][w]
    
    w = calorie_limit
    selected_items = []
    
    for i in range(n, 0, -1):
        item_id, calories, protein, _, _ = items[i-1]
        calories = int(calories)
        
        if w >= calories and dp[i][w] != dp[i-1][w]:
            selected_items.append(items[i-1])
            w -= calories
            
            if item_limit is not None and len(selected_items) >= item_limit:
                break
    
    return selected_items

def greedy_max_protein(items, calorie_limit, item_limit=None):
    items_with_ratio = []
    for item in items:
        item_id, calories, protein, item_name, company = item
        if calories > 0:
            ratio = protein / calories
            items_with_ratio.append((item_id, calories, protein, item_name, company, ratio))
    
    items_with_ratio.sort(key=lambda x: x[5], reverse=True)
    
    selected_items = []
    total_calories = 0
    
    for item in items_with_ratio:
        item_id, calories, protein, item_name, company, _ = item
        if total_calories + calories <= calorie_limit:
            selected_items.append((item_id, calories, protein, item_name, company))
            total_calories += calories
            
            if item_limit is not None and len(selected_items) >= item_limit:
                break
    
    return selected_items

def knapsack_max_calories(items, protein_min, item_limit=None):
    valid_items = [item for item in items if item[1] is not None and item[2] is not None 
                  and item[1] > 0 and item[2] > 0]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    min_protein_combinations = []
    
    valid_items.sort(key=lambda item: item[1]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    def find_combinations(start_idx, current_items, current_protein, current_calories):
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_calories))
            return
        
        if len(current_items) >= max_item_count:
            return
            
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            calories = item[1]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_calories + calories)
            current_items.pop()
    
    if n <= 15 and max_item_count <= 4:
        find_combinations(0, [], 0, 0)
        
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        selected_items = []
        total_protein = 0
        
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_fat(items, protein_min, item_limit=None):
    valid_items = [item for item in items if item[2] > 0 and item[5] is not None]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    scale_factor = 1
    max_fat = max(item[5] for item in valid_items)
    if max_fat > 100:
        scale_factor = 2
    
    min_protein_combinations = []
    
    valid_items.sort(key=lambda item: item[5]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    def find_combinations(start_idx, current_items, current_protein, current_fat):
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_fat))
            return
        
        if len(current_items) >= max_item_count:
            return
            
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            fat = item[5]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_fat + fat)
            current_items.pop()
    
    if n <= 15 and max_item_count <= 4:
        find_combinations(0, [], 0, 0)
        
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        selected_items = []
        total_protein = 0
        
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_carbs(items, protein_min, item_limit=None):
    valid_items = [item for item in items if item[2] > 0 and item[6] is not None]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    min_protein_combinations = []
    
    valid_items.sort(key=lambda item: item[6]/item[2], reverse=True)
    
    max_item_count = item_limit if item_limit else n
    
    def find_combinations(start_idx, current_items, current_protein, current_carbs):
        if current_protein >= protein_min:
            min_protein_combinations.append((current_items[:], current_carbs))
            return
        
        if len(current_items) >= max_item_count:
            return
            
        for i in range(start_idx, n):
            item = valid_items[i]
            protein = item[2]
            carbs = item[6]
            
            current_items.append(item)
            find_combinations(i + 1, current_items, current_protein + protein, current_carbs + carbs)
            current_items.pop()
    
    if n <= 15 and max_item_count <= 4:
        find_combinations(0, [], 0, 0)
        
        if min_protein_combinations:
            min_protein_combinations.sort(key=lambda x: x[1], reverse=True)
            return min_protein_combinations[0][0]
        return []
    else:
        selected_items = []
        total_protein = 0
        
        for item in valid_items:
            if total_protein < protein_min and len(selected_items) < max_item_count:
                selected_items.append(item)
                total_protein += item[2]
                
        return selected_items

def knapsack_max_calorie_protein(items, item_limit):
    valid_items = [item for item in items if item[1] is not None and item[2] is not None 
                  and item[1] > 0 and item[2] > 0]
    
    n = len(valid_items)
    if n == 0:
        return []
    
    items_with_score = []
    for item in valid_items:
        item_id, calories, protein, item_name, company = item[:5]
        score = calories + (protein * 20)
        items_with_score.append((item, score))
    
    items_with_score.sort(key=lambda x: x[1], reverse=True)
    
    selected_items = []
    for i in range(min(item_limit, len(items_with_score))):
        selected_items.append(items_with_score[i][0])
    
    return selected_items