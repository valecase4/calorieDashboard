// Content element
const content = document.getElementById("content")

// API call to /api/food-list
function getFoodList() {
    fetch("http://127.0.0.1:5000/api/food-list")
        .then(response => response.json())
        .then(data => {
            for (const [key, values] of Object.entries(data)) {
                const itemDiv = document.createElement("div")
                itemDiv.classList.add("row", "w-100", "flex", "column", "space-between");

                const itemColumn = document.createElement("div")
                itemColumn.classList.add("w-4", "flex", "o-center", "v-center", "b-bottom");
                itemColumn.textContent = key
                
                itemDiv.appendChild(itemColumn)

                for (const [key2, value2] of Object.entries(values)) {
                    const itemColumn = document.createElement("div")
                    itemColumn.classList.add("flex", "o-center", "v-center", "p-v-1", "w-12", "b-bottom");
                    itemColumn.textContent = value2 
                    
                    itemDiv.appendChild(itemColumn)
                } 

                const lastItemColumn = document.createElement("div")
                lastItemColumn.classList.add("w-12", "b-bottom", "flex", "p-v-1", "o-center", "v-center")

                const deleteForm = document.createElement("form")
                const foodIdInput = document.createElement("input")
                const deleteFoodBtn = document.createElement("input")

                deleteFoodBtn.classList.add("delete-btn")
                deleteFoodBtn.classList.add("b-none", "p-1", "bold", "br-default")
                
                foodIdInput.type = "hidden"
                foodIdInput.value = key
                deleteFoodBtn.type = "submit"
                deleteFoodBtn.value = "D"

                deleteForm.appendChild(deleteFoodBtn)

                deleteForm.method = "POST"
                deleteForm.action = `/delete/${key}`

                lastItemColumn.appendChild(deleteForm)  

                itemDiv.appendChild(lastItemColumn)

                content.appendChild(itemDiv)
            }
        })
}

window.addEventListener("DOMContentLoaded", () => {
    getFoodList()
})