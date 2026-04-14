# Agent logic for NutriSmart AI

## 1. DATA
Hardcoded food dataset in JS:
```json
{
  "pizza":   { "calories":300, "protein":12, "fat":15, "carbs":33 },
  "burger":  { "calories":295, "protein":13, "fat":14, "carbs":30 },
  "poha":    { "calories":180, "protein":4,  "fat":3,  "carbs":35 },
  "idli":    { "calories":120, "protein":3,  "fat":1,  "carbs":25 },
  "paneer":  { "calories":265, "protein":18, "fat":20, "carbs":4  },
  "rice":    { "calories":200, "protein":4,  "fat":1,  "carbs":45 },
  "roti":    { "calories":120, "protein":3,  "fat":2,  "carbs":25 },
  "salad":   { "calories":80,  "protein":2,  "fat":1,  "carbs":10 },
  "milk":    { "calories":150, "protein":8,  "fat":8,  "carbs":12 }
}
```

## 2. LOGIC

### USER SETUP
- Collect: name, age, weight, height, goal
- BMI = weight / (height/100)^2
- TDEE: 
  - Weight Loss = 1500
  - Muscle Gain = 2200
  - Balanced = 1800
- Save to localStorage

### HEALTH SCORE
- Base score = 100
- if calories > 250 → score -= 20
- if protein < 5 → score -= 10
- if fat > 15 → score -= 15
- if goal == "Weight Loss" and calories > 200 → score -= 10 extra
- if goal == "Muscle Gain" and protein < 10 → score -= 15 extra
- score = Math.max(0, score)

### STATUS
- 0–40 → Unhealthy 🔴
- 40–70 → Moderate 🟡
- 70–100 → Healthy 🟢

### SUGGESTIONS
- pizza/burger → "Try whole wheat sandwich or grilled wrap"
- low protein → "Add paneer or eggs to your meal"
- high fat → "Try steaming instead of frying"
- default → "Add more vegetables and lean protein"

### INSIGHTS
- calories > 250 → "High calorie food, consume occasionally"
- protein < 5 → "Low protein content, pair with protein source"
- balanced → "Good nutritional balance for your goal"

### MEAL LOG
- Save analyzed foods to localStorage under "mealLog"
- Entry schema: `{ food, calories, protein, fat, carbs, score, mealType, date }`
- Dashboard reads today's entries and shows total calories consumed.

### DIET PLANNER
- **Weight Loss:** breakfast:poha, lunch:salad+roti, snack:milk, dinner:idli
- **Muscle Gain:** breakfast:milk+paneer, lunch:rice+paneer, snack:milk, dinner:roti+paneer
- **Balanced:** breakfast:poha, lunch:rice+roti, snack:milk, dinner:idli+salad
- **Swap button:** cycles to next food alternative from the list.

### REPORTS
- Read last 7 days from localStorage mealLog
- Calculate daily totals
- Bar chart using Chart.js CDN
- Count most eaten foods
- Generate insight based on data

### UI UX
- Single HTML file output only.
- Side navigation and mobile bottom navigation with JS visibility toggle (no reload).
- Active navigation states handled dynamically.
