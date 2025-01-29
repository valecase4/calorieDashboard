import psycopg2

url = "host='localhost' dbname='tracciamentoCalorie' user='postgres' password='root'"

conn = psycopg2.connect(url)

# TABLES CREATION
# ---------------------------------------------------------------------------------------------------------------------

def create_table_user():
    """
    Create users table
    """
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        user_password VARCHAR(50) NOT NULL
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_foods_table():
    """
    Create foods table
    """
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS foods (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_meals_table():
    """
    Create meals table
    """
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS meals (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_foods_values_table():
    """
    Create foods values table (per 100g)
    e.g., Greek Yogurt has 9g of proteins per 100g
    """
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS food_values (
        id SERIAL PRIMARY KEY,
        food_id INT NOT NULL,
        calories NUMERIC(10, 2) NOT NULL,
        proteins NUMERIC(10, 2) NOT NULL,
        carbs NUMERIC(10, 2) NOT NULL,
        sugars NUMERIC(10, 2) NOT NULL,
        fats NUMERIC(10, 2) NOT NULL,
        saturated_fats NUMERIC(10, 2) NOT NULL,
        FOREIGN KEY (food_id) REFERENCES foods (id)
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_meal_entries_table():
    """
    Create meal entries table
    """    
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS meal_entries (
        entry_id SERIAL PRIMARY KEY,
        food_id INT NOT NULL,
        quantity NUMERIC(10, 2) NOT NULL,
        meal_id INT NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (food_id) REFERENCES foods (id),
        FOREIGN KEY (meal_id) REFERENCES meals (id)
    )
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_goals_table():
    """
    Create table that stores the user's goals
    """
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS goals (
        id SERIAL PRIMARY KEY,
        type TEXT NOT NULL,                   
        target_value FLOAT NOT NULL,          
        tolerance_min FLOAT NOT NULL,         
        tolerance_max FLOAT NOT NULL,         
        rule TEXT NOT NULL,                  
        priority INTEGER NOT NULL,            
        description TEXT                      
    );
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()

# --------------------------------------------------------------------------------------------------------------------

def get_user_credentials():
    """
    Get and return login credentials
    """
    cursor = conn.cursor()

    query = """
    SELECT * FROM users
    """

    cursor.execute(query)
    user = cursor.fetchone()
    conn.commit()
    cursor.close()

    return user

class BackendDB:
    def __init__(self, url_string):
        self.url_string = url_string
        self.conn = psycopg2.connect(self.url_string)

    def get_food_list(self):
        """
        Get all food items with the corresponding nutritional values
        """
        cursor = self.conn.cursor()

        query = """
        SELECT 
            food_values.id, foods.name, food_values.calories, food_values.proteins, food_values.carbs, food_values.sugars, food_values.fats, food_values.saturated_fats
        FROM 
            food_values
        INNER JOIN
            foods
        ON 
            food_values.food_id = foods.id
        """

        cursor.execute(query)
        result = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return result

    def get_all_meals(self):
        """
        Get all meals (names)
        """
        cursor = self.conn.cursor()

        query = """
        SELECT *
        FROM meals
        """

        cursor.execute(query)
        result = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return result
    
    def get_similar_foods_names(self, substring):
        """
        Get the most similar food names based on user input.
        E.g., user type "u", return "uova" ("uova" stands for "eggs")
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
            id, 
            name
        FROM 
            foods
        WHERE
            name ILIKE '%' || '{substring}' || '%'
        ORDER BY
            name ASC
        LIMIT 10;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def get_average_calories(self):
        """
        Get the average amount of calories on a daily basis.
        """
        cursor = self.conn.cursor()
        
        query = """
        SELECT 
	        me.date, SUM(me.quantity * fv.calories / 100) AS total_calories
        FROM 
            meal_entries AS me
        INNER JOIN
            foods AS f
        ON 
            me.food_id = f.id
        INNER JOIN
            food_values AS fv
        ON 
            f.id = fv.food_id
        GROUP BY 
            me.date
        ORDER BY
            me.date DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_best_foods_per_meal_by_occurrences(self, meal_name):
        """
        Get the best 5 foods per meal based on the number of occurrences
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
            foods.id AS food_id,
            foods.name AS food_name,
            COUNT(*) AS occurrences
        FROM 
            meal_entries
        INNER JOIN 
            foods 
        ON 
            meal_entries.food_id = foods.id
        INNER JOIN 
            meals ON meals.id = meal_entries.meal_id
        WHERE 
            meals.name = '{meal_name}'
        GROUP BY (foods.id, foods.name)
        ORDER BY occurrences DESC
        LIMIT 5;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def get_average_amount_proteins_per_meal(self, meal_name):
        """
        Get the average amount of proteins for the specified meal on a daily basis
        """
        cursor = self.conn.cursor()
        query = f"""
        SELECT 
            ROUND(SUM(food_values.proteins * meal_entries.quantity / 100), 2), meal_entries.date
        FROM 
            meal_entries
        INNER JOIN 
            food_values
        ON 
            meal_entries.food_id = food_values.food_id
        INNER JOIN
            meals
        ON 
            meal_entries.meal_id = meals.id
        WHERE 
            meals.name = '{meal_name}'
        GROUP BY meal_entries.date
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_total_macros_per_date(self, date):
        """
        For each macronutrient (calories, proteins, carbs etc...), get the total amout for a specified date
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
            ROUND(SUM(fv.proteins * me.quantity / 100), 2) AS total_proteins,
            ROUND(SUM(fv.carbs * me.quantity / 100), 2) AS total_carbs,
            ROUND(SUM(fv.fats * me.quantity / 100), 2) AS total_fats,
            ROUND(SUM(fv.calories * me."quantity" / 100), 2) AS total_calories,
            ROUND(SUM(fv.saturated_fats * me.quantity / 100), 2) AS total_saturated_fats,
            ROUND(SUM(fv.sugars * me.quantity / 100), 2) AS total_sugars
        FROM 
            meal_entries AS me
        JOIN 
            foods AS f ON me.food_id = f.id
        JOIN 
            food_values AS fv ON f.id = fv.food_id
        WHERE 
            me.date = '{date}';
        """

        cursor.execute(query)
        results = cursor.fetchall()[0]

        output_dict = {
            "proteine": results[0] if results[0] is not None else None,
            "carboidrati": results[1] if results[1] is not None else None,
            "grassi": results[2] if results[2] is not None else None,
            "calorie": results[3] if results[3] is not None else None,
            "grassi_saturi": results[4] if results[4] is not None else None,
            "zuccheri": results[5] if results[5] is not None else None,
        }

        self.conn.commit()
        cursor.close()
        return output_dict
    
    def get_best_nutrient_per_food(self, food_id):
        """
        Return the best nutrient for a specific food and its value per 100g
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
            foods.id,
            foods.name,
            CASE
                WHEN proteins >= GREATEST(carbs, fats, saturated_fats, sugars) THEN 'Proteine'
                WHEN carbs >= GREATEST(proteins, fats, saturated_fats, sugars) THEN 'Carboidrati'
                WHEN fats >= GREATEST(proteins, carbs, saturated_fats, sugars) THEN 'Grassi'
                WHEN saturated_fats >= GREATEST(proteins, carbs, fats, sugars) THEN 'Grassi Saturi'
                WHEN sugars >= GREATEST(proteins, carbs, fats, saturated_fats) THEN 'Zuccheri'
            END AS best_nutrient,
            CASE 
                WHEN proteins >= GREATEST(carbs, fats, saturated_fats, sugars) THEN proteins
                WHEN carbs >= GREATEST(proteins, fats, saturated_fats, sugars) THEN carbs
                WHEN fats >= GREATEST(proteins, carbs, saturated_fats, sugars) THEN fats
                WHEN saturated_fats >= GREATEST(proteins, carbs, fats, sugars) THEN saturated_fats
                WHEN sugars >= GREATEST(proteins, carbs, fats, saturated_fats) THEN sugars
            END AS "value_per_100g"
        FROM food_values
        INNER JOIN foods
        ON food_values.food_id = foods.id
        WHERE food_id = {food_id}
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def get_percentage_contribution_by_food(self, food_id):
        """
        Compute the average contribution of a specific food on each macro nutrient on a daily basis
        """
        cursor = self.conn.cursor()

        query = f"""
        WITH t1 AS (
            SELECT 
                me.date, 
                SUM (me.quantity * fv.proteins / 100) AS total_proteins,
                SUM (me.quantity * fv.calories / 100) AS total_calories,
                SUM (me.quantity * fv.carbs / 100) AS total_carbs,
                SUM (me.quantity * fv.sugars / 100) AS total_sugars,
                SUM (me.quantity * fv.fats / 100) AS total_fats,
                SUM (me.quantity * fv.saturated_fats / 100) AS total_saturated_fats
            FROM meal_entries AS me
            INNER JOIN food_values AS fv
            ON me.food_id = fv.food_id                           
            WHERE me.food_id = {food_id}
            GROUP BY me.date
        ),
        t2 AS (
            SELECT 		
                me.date,
                ROUND(SUM(fv.proteins * me.quantity / 100), 2) AS total_proteins,
                ROUND(SUM(fv.carbs * me.quantity / 100), 2) AS total_carbs,
                ROUND(SUM(fv.fats * me.quantity / 100), 2) AS total_fats,
                ROUND(SUM(fv.calories * me."quantity" / 100), 2) AS total_calories,
                ROUND(SUM(fv.saturated_fats * me.quantity / 100), 2) AS total_saturated_fats,
                ROUND(SUM(fv.sugars * me.quantity / 100), 2) AS total_sugars
            FROM 
                meal_entries AS me
            JOIN 
                foods AS f ON me.food_id = f.id
            JOIN 
                food_values AS fv ON f.id = fv.food_id
            GROUP BY me.date
        )
        SELECT 
            ROUND(AVG(t1.total_proteins / t2.total_proteins * 100), 2) AS avg_protein_percentage,
            ROUND(AVG(t1.total_calories / t2.total_calories * 100), 2) AS avg_calories_percentage,
            ROUND(AVG(t1.total_carbs / t2.total_carbs * 100), 2) AS avg_carbs_percentage,
            ROUND(AVG(t1.total_sugars / t2.total_sugars * 100), 2) AS avg_sugars_percentage,
            ROUND(AVG(t1.total_fats / t2.total_fats * 100), 2) AS avg_fats_percentage,
            ROUND(AVG(t1.total_saturated_fats / t2.total_saturated_fats * 100), 2) AS avg_saturated_fats_percentage
        FROM t1
        INNER JOIN t2
        ON t1.date = t2.date
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_total_occurrences_by_food(self, food_id, last_days=7):
        """
        Get the total occurrences for a specific food id in the last 7 days by default
        """
        cursor = self.conn.cursor()

        query = f"""
        WITH t1 AS (
        SELECT
            me.date,
            COUNT(*) AS occurrences_per_day
        FROM meal_entries AS me
        WHERE me.food_id = {food_id}
        GROUP BY me.date
        ORDER BY me.date DESC
        LIMIT {last_days}
        )
        SELECT 
            SUM (t1.occurrences_per_day)
        FROM t1
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_days_ordered_by_total_calories(self):
        """
        Get the day names (Monday, Tuesday, Wednesday ...) ordered by the amount of calories for those specific days
        """
        cursor = self.conn.cursor()

        query = """
        SET lc_time = 'it_IT.UTF-8';

        WITH t1 AS (
            SELECT
                me.date,
                TO_CHAR(me.date, 'Day') AS day_name,
                ROUND(SUM(me.quantity * fv.calories / 100), 2) AS total_calories
            FROM meal_entries AS me
            INNER JOIN food_values AS fv
            ON me.food_id = fv.food_id
            GROUP BY (me.date, day_name)
        )
        SELECT 
            t1.day_name,
            ROUND(AVG(t1.total_calories), 2)
        FROM t1
        GROUP BY (t1.day_name)
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_best_foods_by_week_day(self, week_day):
        """
        Get the best 5 five foods by occurrences for a specific week day.
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
         	foods.name,
         	COUNT(food_id) AS occurrences,
            foods.id
        FROM (
            SELECT 
                me.food_id, 
                TO_CHAR(me.date, 'Day') AS day_name
            FROM meal_entries AS me
        ) AS subquery
        INNER JOIN foods
        ON food_id = foods.id
        WHERE TRIM(day_name) = '{week_day}'
        GROUP BY (foods.name,foods.id)
        ORDER BY occurrences DESC
        LIMIT 5;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_best_two_days_of_a_food(self, food_id):
        """
        Get the two days on which a given food is consumed most frequently
        """
        cursor = self.conn.cursor()

        query = f"""
        WITH t1 AS (
            SELECT 
                foods.name, 
                TO_CHAR(me.date, 'Day') AS day_name
            FROM meal_entries AS me
            INNER JOIN foods 
            ON foods.id = me.food_id
            WHERE foods.id = {food_id}
        )
        SELECT 
            t1.name,
            t1.day_name,
            COUNT(*) AS occurrences
        FROM t1
        GROUP BY (t1.name, t1.day_name)
        ORDER BY occurrences DESC
        LIMIT 2;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_most_frequent_food_in_pairs(self, food_id):
        """
        Given a food, get the most frequent food in pairs with that given food
        """
        cursor = self.conn.cursor()

        query = f"""
        SELECT 
            foods.name AS paired_food,
            COUNT(*) AS occurrences
        FROM 
            meal_entries AS me1
        INNER JOIN
            meal_entries AS me2 ON me1.date = me2.date AND me1.meal_id = me2.meal_id
        INNER JOIN 
            foods ON foods.id = me2.food_id
        WHERE 
            me1.food_id = {food_id} AND me2.food_id <> {food_id}
        GROUP BY 
            foods.name
        ORDER BY
            occurrences DESC
        LIMIT 1;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def get_energy_spread(self):
        """
        Compute how the average daily calories are divided between the different meals on average
        """
        cursor = self.conn.cursor()

        query = """
            WITH total_calories AS (
                SELECT 
                    m.name AS meal_name,
                    SUM(fv.calories * me.quantity / 100) AS total_calories
                FROM 
                    meal_entries AS me
                JOIN 
                    foods AS f ON me.food_id = f.id
                JOIN 
                    food_values AS fv ON f.id = fv.food_id
                JOIN
                    meals AS m ON me.meal_id = m.id
                GROUP BY 
                    m.name
            ),
            days_count AS (
                SELECT 
                    COUNT(DISTINCT date) AS total_days
                FROM 
                    meal_entries
            ),
            average_daily_calories AS (
                SELECT 
                    AVG(daily_calories.total_calories) AS average_daily_calories
                FROM (
                    SELECT 
                        me.date,
                        SUM(fv.calories * me.quantity / 100) AS total_calories
                    FROM 
                        meal_entries AS me
                    JOIN 
                        foods AS f ON me.food_id = f.id
                    JOIN 
                        food_values AS fv ON f.id = fv.food_id
                    GROUP BY 
                        me.date
                    ) AS daily_calories
            ),
            tt2 AS (
                SELECT 
                    tc.meal_name,
                    (tc.total_calories / NULLIF(dc.total_days, 0)) AS average_calories_per_meal,
                    adc.average_daily_calories
                FROM 
                    total_calories AS tc, days_count AS dc, average_daily_calories AS adc
            )
            SELECT 
                tt2.meal_name,
                ROUND(AVG(average_calories_per_meal / average_daily_calories * 100), 2)
            FROM tt2
            GROUP BY meal_name
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def get_calories_last_seven_days(self):
        """
        Get the amount of calories for the last 7 days
        """
        cursor = self.conn.cursor()

        query = """
        SELECT 
            me.date,
            SUM(fv.calories * me.quantity / 100) AS total_calories
        FROM 
            meal_entries AS me
        JOIN 
            foods AS f ON me.food_id = f.id
        JOIN 
            food_values AS fv ON f.id = fv.food_id
        GROUP BY 
            me.date
        ORDER BY me.date DESC 
        LIMIT 7;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results
    
    def get_most_important_goals(self):
        """
        Get the most important goals based on priority from 'goals' table 
        """
        cursor = self.conn.cursor()

        query = """
        SELECT *
        FROM goals 
        WHERE goals.priority >= ALL (
            SELECT goals.priority
            FROM goals
        )
        """

        cursor.execute(query)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results


    
