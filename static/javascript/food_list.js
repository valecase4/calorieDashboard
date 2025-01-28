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
                lastItemColumn.classList.add("w-12", "b-bottom", "flex", "p-v-1")

                itemDiv.appendChild(lastItemColumn)

                content.appendChild(itemDiv)
            }
        })
}

window.addEventListener("DOMContentLoaded", () => {
    getFoodList()
})