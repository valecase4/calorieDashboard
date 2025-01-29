from flask import Blueprint, jsonify, Response
from db import BackendDB
import json
from datetime import datetime

api_routes = Blueprint('api_routes', __name__, url_prefix='/api')
backend_db = BackendDB("host='localhost' dbname='tracciamentoCalorie' user='postgres' password='root'")

# 
@api_routes.route('/best-five-foods', methods=['GET', 'POST'])
def best_five_foods():
    return 

# Return food suggestions based on user input (form for adding a new food)
@api_routes.route("/suggest-foods/<substring>")
def suggest_foods(substring):
    result = backend_db.get_similar_foods_names(substring)
    return jsonify(result)

# Return the average amount of calories on a daily basis
@api_routes.route("/average-calories")
def average_calories():
    result = backend_db.get_average_calories()
    return jsonify(result)

# get the 5 best foods per meal by occurrences
@api_routes.route("/best-foods-per-meal")
def best_foods_per_meal():
    result = {
        "Colazione": [],
        "Pranzo": [],
        "Cena": [],
        "Spuntini": []
    }

    for meal_name in ['Colazione', 'Pranzo', 'Cena', 'Spuntini']:
        result[meal_name] = backend_db.get_best_foods_per_meal_by_occurrences(meal_name)
    return jsonify(result)

# Get the average amount of proteins per meal on a daily basis
@api_routes.route("/average-protein-per-meal")
def average_protein_per_meal():
    result = {
        "Colazione": [],
        "Pranzo": [],
        "Cena": [],
        "Spuntini": []
    }

    for meal_name in ['Colazione', 'Pranzo', 'Cena', 'Spuntini']:
        result[meal_name] = backend_db.get_average_amount_proteins_per_meal(meal_name)
    return jsonify(result)

# Get the entire list of foods. Each food is correlated with its nutritional values
@api_routes.route("/food-list")
def food_list():
    foods = {}
    result = backend_db.get_food_list()
    
    for item in result:
        id = item[0]
        name = item[1]
        calories = float(item[2]) if item[2] is not None else None
        proteins = float(item[3]) if item[3] is not None else None
        carbs = float(item[4]) if item[4] is not None else None
        sugars = float(item[5]) if item[5] is not None else None
        fats = float(item[6]) if item[6] is not None else None
        saturated_fats = float(item[7]) if item[7] is not None else None

        food = {
            "name": name,
            "calories": calories,
            "proteins": proteins,
            "carbs": carbs,
            "sugars": sugars,
            "fats": fats,
            "saturated_fats": saturated_fats
        }

        foods[id] = food

    response_json = json.dumps(foods, ensure_ascii=False)
    return Response(response_json, content_type="application/json")

# For each macronutrient, get its total amount on a specific date
@api_routes.route("/total-macros-per-date/<date>")
def total_macros_per_date(date):
    """
    Get the total amount for each macronutrient for a specific date
    """
    result = backend_db.get_total_macros_per_date(date)
    print(result)

    return jsonify(result)

# Get details about a food
@api_routes.route("/nutritional-values/<int:food_id>")
def nutritional_values(food_id):
    """
    Get details about a specific food
    """
    best_nutrient = backend_db.get_best_nutrient_per_food(food_id)
    average_percentages = backend_db.get_percentage_contribution_by_food(food_id)[0]
    occurrences_last_seven_days = backend_db.get_total_occurrences_by_food(food_id)[0][0]
    occurrences_last_month = backend_db.get_total_occurrences_by_food(food_id=food_id, last_days=30)[0][0]
    
    food_details = {
        "food_id": food_id,
        "food_name": best_nutrient[0][1],
        "nutrientePrincipale": best_nutrient[0][-2],
        "quantitaNutrientePrincipale": best_nutrient[0][-1],
        "mediaPercentualeProteine": average_percentages[0],
        "mediaPercentualeCalorie": average_percentages[1],
        "mediaPercentualeCarboidrati": average_percentages[2],
        "mediaPercentualeZuccheri": average_percentages[3],
        "mediaPercentualeGrassi": average_percentages[4],
        "mediaPercentualeGrassiSaturi": average_percentages[5],
        "occorrenzeUltimaSettimana": occurrences_last_seven_days,
        "occorrenzeUltimoMese": occurrences_last_month
    }
    return jsonify(food_details)

@api_routes.route("/days-ordered-by-calories")
def days_ordered_by_calories():
    """
    Get the day names (Monday, Tuesday, Wednesday ...) ordered by the amount of calories for those specific days
    """
    ordered_days = backend_db.get_days_ordered_by_total_calories()
    italian_format = {
        "Monday": "Lunedì", 
        "Tuesday": "Martedì",
        "Wednesday": "Mercoledì",
        "Thursday": "Giovedì",
        "Friday": "Venerdì",
        "Saturday": "Sabato",
        "Sunday": "Domenica"
    }
    ordered_days_dict = {italian_format[i[0].strip()]: float(i[1]) for i in ordered_days}
    return jsonify(ordered_days_dict)

@api_routes.route("best-foods-per-week-day/<weekday>")
def best_foods_per_week_day(weekday):
    """
    Get the best 5 five foods by occurrences for a specific week day.
    """
    best_foods = backend_db.get_best_foods_by_week_day(weekday)
    best_foods_dict = {i[2]: i[0] for i in best_foods}
    return jsonify(best_foods_dict)

@api_routes.route("foods-per-week-day-insights/<food_id>")
def foods_per_week_day_insights(food_id):
    """
    Get detailed insights about a food related to potential week days trends.
    """
    week_day_insights = backend_db.get_best_two_days_of_a_food(food_id)
    italian_format = {
        "Monday": "Lunedì", 
        "Tuesday": "Martedì",
        "Wednesday": "Mercoledì",
        "Thursday": "Giovedì",
        "Friday": "Venerdì",
        "Saturday": "Sabato",
        "Sunday": "Domenica"
    }
    find_most_paired_food = backend_db.get_most_frequent_food_in_pairs(food_id)[0][0]
    occurrences_most_paired_food = backend_db.get_most_frequent_food_in_pairs(food_id)[0][1]
    if week_day_insights[0]:
        food_name = week_day_insights[0][0]
        week_day_insights_dict = {
            "id": food_id, 
            "alimento": food_name, 
            "giorniSelezionati": [italian_format[d[1].strip()] for d in week_day_insights],
            "ciboPiuFrequenteInCoppia": find_most_paired_food,
            "occorrenzeCiboPiuFrequenteInCoppia": occurrences_most_paired_food
        }
    return jsonify(week_day_insights_dict)

@api_routes.route("/average-energy-spread")
def average_energy_spread():
    average_calories_spread = backend_db.get_energy_spread()
    average_calories_spread_dict = {i[0]: i[1] for i in average_calories_spread}
    return jsonify(average_calories_spread_dict)

# Get total calories for the last 7 days
@api_routes.route("/calories-trend-last-seven-days")
def calories_trend_last_seven_days():
    last_seven_days_calories = backend_db.get_calories_last_seven_days()
    last_seven_days_calories_dict = {f"{i[0].strftime("%d-%m-%Y")}": round(i[1], 2) for i in last_seven_days_calories}
    return jsonify(last_seven_days_calories_dict)

# Get the most important goals
@api_routes.route("/most-important-goals")
def get_most_important_goals():
    """
    Get the most important goals based on priority from 'goals' table 
    """
    most_important_goals = backend_db.get_most_important_goals()
    most_important_goals_list = []
    for goal in most_important_goals:
        print(goal)
        if goal[5] == 'entro_range':
            goal_dict = {
                "macro": goal[1],
                "valoreIdeale": goal[2],
                "valoreMinimo": goal[2] + goal[3],
                "valoreMassimo": goal[2] + goal[4],
                "regola": "entro_range"
            }
            most_important_goals_list.append(goal_dict)
        elif goal[5] == 'meglio_sopra':
            goal_dict = {
                "macro": goal[1],
                "valoreIdeale": goal[2],
                "valoreMinimo": goal[2],
                "valoreMassimo": goal[4],
                "regola": "meglio_sopra"
            }
            most_important_goals_list.append(goal_dict)
    return jsonify(most_important_goals_list)

# Get all the goals
@api_routes.route("/all-goals")
def get_all_goals():
    """
    Get all goals from goals table
    """
    all_goals = backend_db.get_all_goals()
    all_goals_list = []
    for goal in all_goals:
        print(goal)
        if goal[5] == 'entro_range':
            goal_dict = {
                "macro": goal[1],
                "valoreIdeale": goal[2],
                "valoreMinimo": goal[2] + goal[3],
                "valoreMassimo": goal[2] + goal[4],
                "regola": "entro_range"
            }
            all_goals_list.append(goal_dict)
        elif goal[5] == 'meglio_sopra':
            goal_dict = {
                "macro": goal[1],
                "valoreIdeale": goal[2],
                "valoreMinimo": goal[2],
                "valoreMassimo": goal[4],
                "regola": "meglio_sopra"
            }
            all_goals_list.append(goal_dict)
    return jsonify(all_goals_list)

# Return the last seven days (date format)
@api_routes.route("/last-seven-dates")
def last_seven_dates():
    """
    Return the last seven dates
    """
    dates = backend_db.get_last_seven_dates()
    return jsonify(dates)

# Return the last thirty days (date format)
@api_routes.route("/last-thirty-dates")
def last_thirty_dates():
    """
    Return the last thirty dates
    """
    dates = backend_db.get_last_thirty_dates()
    return jsonify(dates)