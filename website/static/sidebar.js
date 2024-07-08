document.getElementById('toggle-sidebar').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    if (sidebar.style.left === '0px') {
        sidebar.style.left = '-250px';
    } else {
        sidebar.style.left = '0px';
    }
});

function showRecipe(recipeId) {
    fetch(`/get-recipe/${recipeId}`)
        .then(response => response.json())
        .then(data => {
            var formattedRecipe = data.recipe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                             .replace(/\*(.*?)\*/g, '<em>$1</em>')
                                             .replace(/\n/g, '<br>');
            document.getElementById('response').innerHTML = formattedRecipe;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').innerHTML = 'Error occurred while retrieving recipe.';
        });
}
