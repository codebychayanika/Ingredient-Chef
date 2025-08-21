from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# अपनी Spoonacular API key यहाँ डालें
API_KEY = "8813b0f1a60b4e30a767c535c01c70bf"

@app.route("/recommend", methods=["POST"])
def recommend_recipes():
    data = request.get_json()
    ingredients = data.get("ingredients")

    if not ingredients:
        return jsonify({"error": "Ingredients list is empty"}), 400

    ingredients_csv = ",".join(ingredients)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_csv}&number=5&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        recipes = response.json()
        return jsonify(recipes)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recipe_details/<int:recipe_id>", methods=["GET"])
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        details = response.json()
        return jsonify(details)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)