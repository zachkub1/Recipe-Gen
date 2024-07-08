from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Recipe
import google.generativeai as genai

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    return render_template('landing.html')

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/home')
@login_required
def home():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, recipes=recipes)

@views.route('/generate-recipe', methods=['POST'])
@login_required
def generate_recipe():
    # Extract form data
    ingredients = request.form.get('ingredients').split(',')
    dietary_restrictions = request.form.get('ingredient-restrictions').split(',')
    num_people = int(request.form.get('num_people'))
    min_calories = float(request.form.get('min_calories')) if request.form.get('min_calories') else 0.0
    max_calories = float(request.form.get('max_calories')) if request.form.get('max_calories') else 0.0
    min_protein = float(request.form.get('min_protein')) if request.form.get('min_protein') else 0.0
    max_protein = float(request.form.get('max_protein')) if request.form.get('max_protein') else 0.0
    min_carbs = float(request.form.get('min_carbs')) if request.form.get('min_carbs') else 0.0
    max_carbs = float(request.form.get('max_carbs')) if request.form.get('max_carbs') else 0.0
    min_fats = float(request.form.get('min_fats')) if request.form.get('min_fats') else 0.0
    max_fats = float(request.form.get('max_fats')) if request.form.get('max_fats') else 0.0

    # Generate the recipe
    api_key = 'AIzaSyBklnEi0DjnO3gMGkgKYUbrWRJphMZH9Ac'  # Replace with your API key
    generated_recipe = generate_recipe_api(
        ingredients, dietary_restrictions, num_people, min_calories, max_calories, 
        min_protein, max_protein, min_carbs, max_carbs, min_fats, max_fats
    )

    # Save the generated recipe to the database
    new_recipe = Recipe(content=generated_recipe, user_id=current_user.id)
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({'recipe': generated_recipe})

def generate_recipe_api(ingredients, dietary_restrictions, num_people, min_calories, max_calories, min_protein, max_protein, min_carbs, max_carbs, min_fats, max_fats):
    api_key = 'AIzaSyBklnEi0DjnO3gMGkgKYUbrWRJphMZH9Ac'
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        avoid_ingredients = []
        for restriction in dietary_restrictions:
            avoid_ingredients.append(f"avoid {restriction}")
        prompt = (
            f"Create a recipe using the following ingredients: {', '.join(ingredients)} "
            f"with dietary restrictions: {', '.join(avoid_ingredients)} for {num_people} people. " 
            f"Nutritional values per serving: Calories: {min_calories}-{max_calories} kcal, "
            f"Protein: {min_protein}-{max_protein}g, Carbohydrates: {min_carbs}-{max_carbs}g, Fat: {min_fats}-{max_fats}g"
        )
        
        response = model.generate_content(prompt)
        # Ensure response.text is properly formatted
        formatted_response = response.text.replace('\n', '\n<br>')
        return formatted_response
    except Exception as e:
        return str(e)

@views.route('/get-recipe/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    return jsonify({'recipe': recipe.content})

