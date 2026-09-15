from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["smart_pantry"]

# Select collections
grocery_collection = db["grocery"]
recipe_collection = db["recipes"]


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    items = list(grocery_collection.find())

    today = datetime.today().date()

    total_items = len(items)
    fresh_items = 0
    expiring_items = 0
    expired_items = 0

    for item in items:
        expiry = datetime.strptime(
            item["expiry_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (expiry - today).days

        if days_left < 0:
            item["status"] = "Expired"
            expired_items += 1

        elif days_left <= 3:
            item["status"] = "Expiring Soon"
            expiring_items += 1

        else:
            item["status"] = "Fresh"
            fresh_items += 1

    return render_template(
        "index.html",
        items=items,
        total_items=total_items,
        fresh_items=fresh_items,
        expiring_items=expiring_items,
        expired_items=expired_items
    )


# =========================
# RECIPE SYNTHESIZER
# =========================

@app.route("/recipes")
def recipes():

    from flask import request

    pantry_items = list(grocery_collection.find())

    today = datetime.today().date()

    expiring_items = []
    expired_items = []
    fresh_items = []

    for item in pantry_items:

        expiry = datetime.strptime(
            item["expiry_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (expiry - today).days

        if days_left < 0:
            item["status"] = "Expired"
            expired_items.append(item)

        elif days_left <= 3:
            item["status"] = "Expiring Soon"
            expiring_items.append(item)

        else:
            item["status"] = "Fresh"
            fresh_items.append(item)


    # Get the ingredient selected by the client
    selected_item = request.args.get("item")


    # All available pantry ingredients
    pantry_ingredients = []

    for item in pantry_items:

        # Do not use expired items as recipe ingredients
        if item["status"] != "Expired":

            pantry_ingredients.append(
                item["item_name"].lower()
            )


    # Get all recipes
    all_recipes = list(recipe_collection.find())

    matching_recipes = []


    # If client selected an ingredient
    if selected_item:

        selected_item_lower = selected_item.lower()

        for recipe in all_recipes:

            recipe_ingredients = [
                ingredient.lower()
                for ingredient in recipe["ingredients"]
            ]

            # Recipe must contain selected ingredient
            if selected_item_lower in recipe_ingredients:

                matched_ingredients = []

                for ingredient in recipe["ingredients"]:

                    if ingredient.lower() in pantry_ingredients:

                        matched_ingredients.append(ingredient)

                recipe["matched_ingredients"] = matched_ingredients

                matching_recipes.append(recipe)


    return render_template(
        "recipes.html",
        expiring_items=expiring_items,
        expired_items=expired_items,
        fresh_items=fresh_items,
        selected_item=selected_item,
        recipes=matching_recipes
    )


    # All pantry ingredients
    pantry_ingredients = []

    for item in pantry_items:
        pantry_ingredients.append(
            item["item_name"].lower()
        )


    all_recipes = recipe_collection.find()

    priority_recipes = []
    other_recipes = []


    for recipe in all_recipes:

        matched_ingredients = []

        for ingredient in recipe["ingredients"]:

            if ingredient.lower() in pantry_ingredients:

                matched_ingredients.append(ingredient)


        if len(matched_ingredients) > 0:

            recipe["matched_ingredients"] = matched_ingredients

            uses_expiring_item = False

            for ingredient in recipe["ingredients"]:

                if ingredient.lower() in priority_ingredients:

                    uses_expiring_item = True


            if uses_expiring_item:
                priority_recipes.append(recipe)

            else:
                other_recipes.append(recipe)


    return render_template(
        "recipes.html",
        priority_recipes=priority_recipes,
        other_recipes=other_recipes,
        expiring_items=expiring_items,
        expired_items=expired_items
    )


# =========================
# GROCERY / PANTRY
# =========================

@app.route("/grocery", methods=["GET", "POST"])
def grocery():

    # Add grocery item
    if request.method == "POST":

        item = {
            "item_name": request.form["item_name"],
            "category": request.form["category"],
            "quantity": request.form["quantity"],
            "expiry_date": request.form["expiry_date"]
        }

        grocery_collection.insert_one(item)

        return redirect("/grocery")

    # Get all grocery items
    items = list(grocery_collection.find())

    # Today's date
    today = datetime.today().date()

    # Check expiry status
    for item in items:

        expiry = datetime.strptime(
            item["expiry_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (expiry - today).days

        if days_left < 0:

            item["status"] = "Expired"

        elif days_left <= 3:

            item["status"] = "Expiring Soon"

        else:

            item["status"] = "Fresh"

    # Count expiry alerts
    expiry_alerts = 0

    for item in items:

        if item["status"] == "Expired" or item["status"] == "Expiring Soon":

            expiry_alerts += 1

    return render_template(
        "grocery.html",
        items=items,
        expiry_alerts=expiry_alerts
    )


# =========================
# DELETE GROCERY ITEM
# =========================

@app.route("/delete/<item_id>")
def delete(item_id):

    from bson.objectid import ObjectId

    grocery_collection.delete_one({
        "_id": ObjectId(item_id)
    })

    return redirect("/grocery")


# =========================
# EDIT GROCERY ITEM
# =========================

@app.route("/edit/<item_id>", methods=["GET", "POST"])
def edit(item_id):

    from bson.objectid import ObjectId

    # Update item
    if request.method == "POST":

        updated_item = {
            "item_name": request.form["item_name"],
            "category": request.form["category"],
            "quantity": request.form["quantity"],
            "expiry_date": request.form["expiry_date"]
        }

        grocery_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": updated_item}
        )

        return redirect("/grocery")

    # Find item
    item = grocery_collection.find_one({
        "_id": ObjectId(item_id)
    })

    return render_template(
        "edit.html",
        item=item
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)