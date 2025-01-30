from flask import Flask, render_template, request, redirect, url_for, flash
from db import (
    create_table_user, 
    get_user_credentials, 
    create_foods_table, 
    create_meals_table,
    create_foods_values_table,
    create_meal_entries_table,
    create_goals_table
)
from db import BackendDB
from dotenv import load_dotenv
import os
from utils import get_current_date, RegexConverter
from datetime import datetime, timedelta
from api import api_routes

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
# Regex converter for routes
app.url_map.converters['regex'] = RegexConverter
app.register_blueprint(api_routes)

backend_db = BackendDB("host='localhost' dbname='tracciamentoCalorie' user='postgres' password='root'")

#-----------------------------------------------------------------------------------------------------------------------
# LOGIN ROUTE

@app.route("/", methods=['GET', 'POST'])
def login():
    user = get_user_credentials()
    error = None

    username, password = user[1], user[2]

    if request.method == 'POST':
        username_input = request.form.get("username")
        password_input = request.form.get("password")

        if username_input != username or password_input != password:
            error = "Credenziali errate. Riprovare"
            flash(error)
        else:
            return redirect(url_for('index', date=get_current_date()))

    return render_template("login.html", error=error)

#-----------------------------------------------------------------------------------------------------------------------
# HOMEPAGE ROUTE

@app.route(r"/<regex('\d{2}-\d{2}-\d{4}'):date>", methods=['GET', 'POST'])
def index(date):
    # Convert date to italian format
    date_obj = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")

    all_meals = backend_db.get_all_meals()
    all_meal_entries_for_current_date = backend_db.get_all_meal_entries(date)

    if request.method == 'POST':
        food_name_input = request.form.get("foodNameInput")
        try:
            food_id = backend_db.get_food_id_by_food_name(food_name_input)[0]

            if food_id:
                food_quantity = request.form.get("foodQuantityInput")
                meal_id = request.form.get("mealNameInput")
                backend_db.enter_meal_entry(
                    food_id, 
                    food_quantity,
                    meal_id,
                    date
                )
                return redirect(url_for('index', date=date))
        except:
            return redirect(url_for("new_food", food_name=food_name_input))

    return render_template("index.html", all_meals=all_meals, date_obj=date_obj, all_meal_entries_for_current_date=all_meal_entries_for_current_date)

#-----------------------------------------------------------------------------------------------------------------------
# USER DASHBOARD

@app.route("/user-dashboard", methods=['GET', 'POST'])
def user_dashboard():
    return render_template("user_dashboard.html")

#------------------------------------------------------------------------------------------------------------------------

@app.route("/food-list", methods=['GET', 'POST'])
def food_list():
    return render_template("food_list.html")

#------------------------------------------------------------------------------------------------------------------------

@app.route("/delete/<int:food_id>", methods=['GET', 'POST'])
def delete_food(food_id):
    """
    Delete from food values table
    """
    print("Executed")

    backend_db.delete_food_from_foods(food_id)
    return redirect(url_for("index", date=get_current_date()))

@app.route("/delete-meal-entry/<int:entry_id>", methods=['GET', 'POST'])
def delete_meal_entry(entry_id):
    """
    Delete a meal entry
    """
    backend_db.delete_meal_entry(entry_id)
    return redirect(url_for("index", date=get_current_date()))

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/new_food/<food_name>", methods=['GET', 'POST'])
def new_food(food_name):
    if request.method == 'POST':
        backend_db.enter_food_name(food_name)

        calories = request.form.get("caloriesInput")
        proteins = request.form.get("proteinsInput")
        carbs = request.form.get("carbsInput")
        sugars = request.form.get("sugarsInput")
        fats = request.form.get("fatsInput")
        saturated_fats = request.form.get("saturatedFatsInput")

        food_id = backend_db.get_food_id_by_food_name(food_name)[0]

        backend_db.enter_food_values(food_id, calories, proteins, carbs, sugars, fats, saturated_fats)

        return redirect(url_for("index", date=get_current_date()))
    return render_template("new_food.html", food_name=food_name)

#------------------------------------------------------------------------------------------------------------------------

@app.route("/yesterday", methods=['GET', 'POST'])
def yesterday():
    if request.method == 'POST':
        current_date = request.form.get("currentDate")
        previous_date = (datetime.strptime(current_date, "%d-%m-%Y") - timedelta(days=1)).strftime("%d-%m-%Y")

        return redirect(url_for('index', date=previous_date))
    
@app.route("/tomorrow", methods=['GET', 'POST'])
def tomorrow():
    if request.method == 'POST':
        current_date = request.form.get("currentDate")
        next_day = (datetime.strptime(current_date, "%d-%m-%Y") + timedelta(days=1)).strftime("%d-%m-%Y")

        return redirect(url_for('index', date=next_day))
    
#------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # TABLES CREATION
    create_table_user()
    create_foods_table()
    create_meals_table()
    create_foods_values_table()
    create_meal_entries_table()
    create_goals_table()
    app.run(debug=True)