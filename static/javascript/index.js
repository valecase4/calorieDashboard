// Form for adding a new food
const formContainer = document.getElementById("formContainer")

// Background effect
const overlay = document.getElementById("overlay")

// text inputs where user can add a new food
const foodNameInput = document.getElementById("foodNameInput")
const foodQuantityInput = document.getElementById("foodQuantityInput")

// Function that displays the form for adding a new food
function openForm(mealName) {
    formContainer.classList.add("active")
    overlay.classList.add("active")

    // Meal name input in the form for adding a new food
    const mealNameInput = document.getElementById("mealNameInput")
    mealNameInput.value = mealName
}

// Function to reset the form's inputs 
function resetForm() {
    foodNameInput.value = ""
    foodQuantityInput.value = "1"
}

// Function that handles the click on overlay background effect
function onClickOverlay() {
    formContainer.classList.remove("active")
    overlay.classList.remove("active")
}

// Call the function
overlay.addEventListener("click", () => {
    onClickOverlay()
    resetForm()
})

// Function that handles suggestions when the user wants to enter a new food name
foodNameInput.addEventListener("input", function() {
    const currentInput = foodNameInput.value 

    // Div container for suggestion items
    const suggestionDiv = document.getElementById("suggestions")
    suggestionDiv.innerHTML = ''
    suggestionDiv.classList.remove("disp-none")

    if (currentInput.length === 0) {
        suggestionDiv.classList.add("disp-none")
    }

    fetch(`/api/suggest-foods/${currentInput}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                suggestionDiv.classList.add("disp-none")
            }
            data.forEach(item => {
                // Create a suggestion item
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = item[1]
                suggestionItem.classList.add('suggestion-item'); 

                suggestionItem.addEventListener('click', () => {
                    foodNameInput.value = item[1];
                    suggestionDiv.innerHTML = '';
                    suggestionDiv.classList.add("disp-none")

                    console.log(foodNameInput.value)
                });

                suggestionDiv.appendChild(suggestionItem);
            })
        })
})

// Form to add a new food
const newFoodForm = document.getElementById("newFoodForm")

newFoodForm.addEventListener("submit", (e) => {
    const foodNameValue = foodNameInput.value 

    if (foodNameValue.length === 0) {
        e.preventDefault()
        alert("Inserire un alimento valido.")
    }
    console.log(foodNameValue)
})