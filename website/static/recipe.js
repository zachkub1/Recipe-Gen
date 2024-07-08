function generate_recipe() {
    document.getElementById('response').innerHTML = 'Generating recipe...';

    var ingredients = document.getElementById('ingredients').value;
    var diet = document.getElementById('ingredient-restrictions').value;
    var servings = document.getElementById('servings').value;
    var calories = document.getElementById('calories').value;
    var protein = document.getElementById('protein').value;
    var fats = document.getElementById('fats').value;
    var carbs = document.getElementById('carbs').value;

    var formData = new FormData();
    formData.append('ingredients', ingredients);
    formData.append('ingredient-restrictions', diet);
    formData.append('num_people', servings);
    formData.append('min_calories', calories.split('-')[0] || 0);
    formData.append('max_calories', calories.split('-')[1] || 0);
    formData.append('min_protein', protein.split('-')[0] || 0);
    formData.append('max_protein', protein.split('-')[1] || 0);
    formData.append('min_fats', fats.split('-')[0] || 0);
    formData.append('max_fats', fats.split('-')[1] || 0);
    formData.append('min_carbs', carbs.split('-')[0] || 0);
    formData.append('max_carbs', carbs.split('-')[1] || 0);

    fetch('/generate-recipe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var formattedRecipe = data.recipe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                         .replace(/\*(.*?)\*/g, '<em>$1</em>')
                                         .replace(/\n/g, '<br>');
        document.getElementById('response').innerHTML = formattedRecipe;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = 'Error occurred while generating recipe.';
    });
}
