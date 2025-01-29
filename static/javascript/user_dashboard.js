// ---------------------------------------------------------------------------------------------------------------
// Section 1 

const bestFiveFoodsPerMealDiv = document.getElementById("bestFiveFoodsPerMealDiv")
const bestFiveFoodsPerMealSelect = document.getElementById("bestFiveFoodsPerMealSelect")

// Container that shows the details for a specific food
const foodDetailsDiv = document.getElementById("foodDetailsDiv")

// Background effect
const overlay = document.getElementById("overlay")

function closeOverlay() {
    overlay.classList.add("disp-none")
    foodDetailsDiv.classList.add("disp-none")
    foodWeekDaysInsightsDiv.classList.add("disp-none")
    energySpreadPieChartDiv.classList.add("disp-none")
}

overlay.addEventListener("click", () => {
    closeOverlay()
})

// Best 5 five foods per meal
function getBestFiveFoodsPerMeal(mealName) {
    fetch("http://127.0.0.1:5000/api/best-foods-per-meal")
        .then(response => response.json())
        .then(data => {
            bestFiveFoodsPerMealDiv.innerHTML = ''

            let result = data[`${mealName}`]

            let outputArray = []
            result.forEach(item => {
                const foodDetails = [item[0], item[1]]
                outputArray.push(foodDetails)
            })

            outputArray.forEach(
                array => {
                    const foodRow = document.createElement("div")
                    foodRow.classList.add("best-food-meal-item", "w-100", "h-20", "flex", "o-center", "v-center")
                    foodRow.style.borderTop = "1px solid gray"
                    foodRow.textContent = array[1]

                    foodRow.addEventListener("click", () => {
                        overlay.classList.remove("disp-none")
                        foodDetailsDiv.classList.remove("disp-none")
                        
                        // Api Call
                        displayFoodDetails(array[0])
                    })

                    bestFiveFoodsPerMealDiv.appendChild(foodRow)
                }
            )
        })
}

function displayFoodDetails (foodId) {
    fetch(`http://127.0.0.1:5000/api/nutritional-values/${foodId}`)
        .then(response => response.json())
        .then(data => {
            // First paragraph
            const foodDescription = document.getElementById("foodDescription")
            const foodDescriptionContent = `<p>L'alimento <b>${data.food_name}</b> è per te una fonte di <b>${data.nutrientePrincipale}</b> (<b>${data.quantitaNutrientePrincipale}g</b> per 100g di prodotto).</b>` 
            foodDescription.innerHTML = foodDescriptionContent
            console.log(foodDescriptionContent)

            // Second paragraph
            const foodContributionsCalories = document.getElementById("foodContributionsCalories")
            const foodContributionsCaloriesContent = `
                <p>
                    Nei giorni in cui hai consumato questo alimento, questo ha rappresentato il <b>${data.mediaPercentualeCalorie}%</b>
                    delle calorie totali giornaliere.
                </p>
            `
            foodContributionsCalories.innerHTML = foodContributionsCaloriesContent

            // Third paragraph
            const foodContributions = document.getElementById("foodContributions")
            let foodContributionsContent;
            if (data.nutrientePrincipale == "Carboidrati") {
                foodContributionsContent = `
                    <p>
                        Inoltre, negli stessi giorni, ha rappresentato il <b>${data.mediaPercentualeCarboidrati}%</b> 
                        dei <b>carboidrati</b> totali giornalieri.
                    </p>
                `
            } else if (data.nutrientePrincipale == 'Proteine') {
                foodContributionsContent = `
                    <p>
                        Inoltre, negli stessi giorni, ha rappresentato il <b>${data.mediaPercentualeProteine}%</b> 
                        delle <b>proteine</b> totali giornaliere.
                    </p>
                `
            } else if (data.nutrientePrincipale == 'Zuccheri') {
                foodContributionsContent = `
                    <p>
                        Inoltre, negli stessi giorni, ha rappresentato il <b>${data.mediaPercentualeZuccheri}%</b> 
                        degli <b>zuccheri</b> totali giornalieri.
                    </p>
                `
            } else if (data.nutrientePrincipale == "Grassi Saturi") {
                foodContributionsContent = `
                    <p>
                        Inoltre, negli stessi giorni, ha rappresentato il <b>${data.mediaPercentualeGrassiSaturi}%</b> 
                        dei <b>grassi saturi</b> totali giornalieri.
                    </p>
                `
            } else if (data.nutrientePrincipale == "Grassi") {
                foodContributionsContent = `
                    <p>
                        Inoltre, negli stessi giorni, ha rappresentato il <b>${data.mediaPercentualeGrassi}%</b> 
                        dei <b>grassi</b> totali giornalieri.
                    </p>
                `
            }
            foodContributions.innerHTML = foodContributionsContent

            // Fourth paragraph
            const howManyOccurrences = document.getElementById("howManyOccurrences")
            const howManyOccurrencesContent = `
                <p>
                    Hai consumato questo alimento <b>${data.occorrenzeUltimaSettimana} volta/e</b> negli ultimi 7 giorni e
                    <b>${data.occorrenzeUltimoMese} volta/e</b> negli ultimi 30 giorni.
                </p>
            `
            howManyOccurrences.innerHTML = howManyOccurrencesContent
        })
}

// Default API Call
window.addEventListener("DOMContentLoaded", () => {
    getBestFiveFoodsPerMeal("Colazione")
})

// Call getBestFiveFoodsPerMeal after a user's input

bestFiveFoodsPerMealSelect.addEventListener("input", () => {
    getBestFiveFoodsPerMeal(bestFiveFoodsPerMealSelect.value)
})

// ---------------------------------------------------------------------------------------------------------------
// Section 2

// Macros for a specific date

const macrosPerDateDiv = document.getElementById("macrosPerDateDiv")
const macrosDateInput = document.getElementById("macrosDateInput")

// API CALL

function getMacrosByDate(date) {
    fetch(`http://127.0.0.1:5000/api/total-macros-per-date/${date}`)
        .then(response => response.json())
        .then(
            data => {
                macrosPerDateDiv.innerHTML = ''

                for (const [key, value] of Object.entries(data)) {
                    const macroP = document.createElement("div")
                    macroP.classList.add("w-100", "h-16-6", "flex",  "row", "space-between", "v-center", "p-o-1", "b-top")
                    const firstSpan = document.createElement("span")
                    firstSpan.classList.add("bold")
                    firstSpan.textContent = key.toUpperCase()
                    const secondSpan = document.createElement("span")
                    secondSpan.classList.add("lt-sp-0-1")

                    if (value) {
                        if (key == "calorie") {
                            secondSpan.textContent = value + ' kcal'
                        } else {
                            secondSpan.textContent = value + ' g'
                        }
                    } else {
                        secondSpan.textContent = "--"
                    }

                    macroP.appendChild(firstSpan)
                    macroP.appendChild(secondSpan)

                    macrosPerDateDiv.appendChild(macroP)
                }
            }
        )
}

macrosDateInput.addEventListener("input", () => {
    const userInput = macrosDateInput.value 
    getMacrosByDate(userInput)
})

// Defult API CALL

window.addEventListener("DOMContentLoaded", () => {
    const today = new Date().toISOString().split('T')[0];
    macrosDateInput.setAttribute("max", today)
    macrosDateInput.value = today

    // Call API for today date
    getMacrosByDate(today)
})

// ---------------------------------------------------------------------------------------------------------------
// Section 3

// Get the days ordered by the average amount of calories
const bestDayByCalories = document.getElementById("bestDayByCalories")
const allDaysByCaloriesDivs = document.querySelectorAll(".day-by-calories")

// Api Call 
function getOrderedDaysByCalories () {
    fetch("http://127.0.0.1:5000/api/days-ordered-by-calories")
        .then(response => response.json())
        .then(data => {
            const sortedData = Object.fromEntries(
                Object.entries(data).sort(([, a], [, b]) => b - a)
            )
            
            for (let i=0; i<Object.keys(sortedData).length; i++) {
                const key = Object.keys(sortedData)[i]
                const value = Object.values(sortedData)[i]

                if (i === 0) {
                    bestDayByCalories.innerHTML = `
                        <p>
                            In media, il giorno in cui consumi più calorie è il <b>${key}</b>, con una media di 
                            <b>${value} kcal.</b>
                        </p>
                    `
                } else {
                    const selectedDiv = allDaysByCaloriesDivs[i-1]
                    selectedDiv.innerHTML = `
                        <span>${i+1}.</span>
                        <span><b>${key}</b></span>
                        <span><b>${value}</b> kcal</span>
                    `
                }
            }
        })
}

getOrderedDaysByCalories()

// ---------------------------------------------------------------------------------------------------------------
// Section 4
// Best foods per week day

const bestFiveFoodsPerWeekDaySelect = document.getElementById("bestFiveFoodsPerWeekDaySelect")
const bestFiveFoodsPerWeekDayDiv = document.getElementById("bestFiveFoodsPerWeekDay")

const foodWeekDaysInsightsDiv = document.getElementById("foodWeekDaysInsightsDiv")

function getBestFoodsPerWeekDay (weekDay) {
    fetch(`http://127.0.0.1:5000/api/best-foods-per-week-day/${weekDay}`)
        .then(response => response.json())
        .then(data => {
            // Clean HTML before a calling
            bestFiveFoodsPerWeekDayDiv.innerHTML = ''

            if (Object.keys(data).length === 0) {
                bestFiveFoodsPerWeekDayDiv.innerHTML = '<p>Non ho trovato alcun risultato per il giorno inserito.</p>'
            } else {
                for (let i=0; i<5; i++) {
                    const key = Object.keys(data)[i]
                    const value = Object.values(data)[i]
    
                    const foodRow = document.createElement("div")
                    foodRow.classList.add("best-food-meal-item", "w-100", "h-20", "flex", "o-center", "v-center")
                    foodRow.style.borderTop = "1px solid gray"
                    foodRow.textContent = value

                    foodRow.addEventListener("click", () => {
                        overlay.classList.remove("disp-none")
                        foodWeekDaysInsightsDiv.classList.remove("disp-none")
                        
                        // Api Call
                        getWeekDaysInsights(key)
                    })
    
                    bestFiveFoodsPerWeekDayDiv.appendChild(foodRow)
                }
            }
        })
}

// Get more detailed insights about a specific food and week days trends
function getWeekDaysInsights(foodId) {
    fetch(`http://127.0.0.1:5000/api/foods-per-week-day-insights/${foodId}`)
        .then(response => response.json())
        .then(data => {
            // First paragraph
            const twoBestWeekDays = document.getElementById("twoBestWeekDays")
            const twoBestWeekDaysContent = `<p>I giorni in cui consumi più spesso l'alimento <b>${data.alimento}</b> sono <b>${data.giorniSelezionati[0]}</b> e <b>${data.giorniSelezionati[1]}</b>` 
            twoBestWeekDays.innerHTML = twoBestWeekDaysContent

            // Second Paragraph
            const mostPairedFood = document.getElementById("mostPairedFood")
            const mostPairedFoodContent = `
                <p>
                    <b><u>Curiosità:</u></b><br><br>L'alimento che risulta accoppiato più frequentemente (all'interno di uno stesso pasto) con <b>${data.alimento}</b> è <b>${data.ciboPiuFrequenteInCoppia}</b>.
                    <br><br>Questa accoppiata è stata rilevata <b>${data.occorrenzeCiboPiuFrequenteInCoppia} volta/e</b>.
                </p>
            `
            mostPairedFood.innerHTML = mostPairedFoodContent
        })
}

// API Call when user enters an input 
bestFiveFoodsPerWeekDaySelect.addEventListener("input", () => {
    const currentWeekDay = bestFiveFoodsPerWeekDaySelect.value 
    console.log(currentWeekDay)
    getBestFoodsPerWeekDay(currentWeekDay)
})

// Default API call
window.addEventListener("DOMContentLoaded", () => {
    getBestFoodsPerWeekDay("Monday")
})

// ---------------------------------------------------------------------------------------------------------------
// Section 5
// Get and show how the calories are divided between the different meals on average (percentage)

const showCalorieSpreadBtn = document.getElementById("showCalorieSpreadBtn")
const energySpreadPieChartDiv = document.getElementById("energySpreadPieChartDiv")

showCalorieSpreadBtn.addEventListener("click", () => {
    overlay.classList.remove("disp-none")
    energySpreadPieChartDiv.classList.remove("disp-none")

    createCalorieSpreadPieChart()
})

// Plugin to draw labels on a pie chart
const drawLabelsOnSlicesPlugin = {
    id: 'drawLabelOnSlices',
    afterDraw(chart) {
        const {ctx} = chart;
        chart.data.datasets.forEach((dataset, datasetIndex) => {
            const meta = chart.getDatasetMeta(datasetIndex);
            meta.data.forEach((slice, index) => {
                const label = chart.data.labels[index]
                const value = dataset.data[index]

                const {x, y} = slice.tooltipPosition()

                ctx.fillStyle = 'white'; 
                ctx.font = '20px Red Hat Display';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fontWeight = 'bold'
                ctx.fillText(`${label}`, x, y - 10);
                ctx.fillText(`${value}`, x, y + 10); 
            })
        })
    }
}

function createCalorieSpreadPieChart() {
    fetch("http://127.0.0.1:5000/api/average-energy-spread")
        .then(response => response.json())
        .then(percentages => {
            const ctx = document.getElementById("energySpreadPieChart").getContext('2d')

            let myChart;

            if (Chart.getChart(ctx)) {
                Chart.getChart(ctx)?.destroy()
            }

            myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(percentages),
                    datasets: [{
                        label: 'Percentuale',
                        data: Object.values(percentages),
                        backgroundColor: [
                            '#074e6e',
                            '#1E81B0',
                            '#003366',
                            '#99CCFF'
                        ]
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                color: 'white',
                                font: {
                                    size: 20,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                },
                plugins: [drawLabelsOnSlicesPlugin]
            })
        })
}

function getAverageEnergySpread() {
    fetch("http://127.0.0.1:5000/api/average-energy-spread")
        .then(response => response.json())
        .then(data => {
            const entries = Object.entries(data); // Ottieni array di coppie chiave-valore
            const maxEntry = entries.reduce((max, current) => {
                const currentValue = parseFloat(current[1]);
                return currentValue > parseFloat(max[1]) ? current : max; 
            });

            // First Paragraph
            const mostCaloricMeal = document.getElementById("mostCaloricMeal")
            mostCaloricMeal.innerHTML = ''
            mostCaloricMeal.innerHTML = `
                <p>
                    Mediamente, il pasto più calorico delle tue giornate risulta essere <b>${maxEntry[0]}</b>, nel
                    quale concentri il <b>${maxEntry[1]}%</b> delle tue calorie giornaliere.
                </p>
            `

            // Second Paragraph
            const otherCaloricMeals = document.getElementById("otherCaloricMeals")
            let otherCaloricMealsContent = '<p>Inoltre, in media: <br><br><p>'

            for (const [key, value] of Object.entries(data)) {
                if (key !== maxEntry[0]) {
                    const newParagraph = `<p>&#x2022; In <b>${key}</b> concentri il <b>${value}%</b> delle calorie.</p><br>`
                    otherCaloricMealsContent = otherCaloricMealsContent + newParagraph
                }
            }

            otherCaloricMeals.innerHTML = otherCaloricMealsContent
        })
}

getAverageEnergySpread()

// ---------------------------------------------------------------------------------------------------------------
// Section 6
// Calories Trend

// Graph container (canvas)
const caloriesTrendGraphs = document.getElementById("caloriesTrendGraphs").getContext('2d')

function getCaloriesLastSevenDays() {
    fetch("http://127.0.0.1:5000/api/calories-trend-last-seven-days")
        .then(response => response.json())
        .then(calorieData => 
            {
                const myChart = new Chart(caloriesTrendGraphs, {
                    type: 'line',
                    data: {
                        labels: Object.keys(calorieData),
                        datasets: [
                            {
                                data: Object.values(calorieData),
                                label: 'Andamento Calorie',
                                borderColor: '#074e6e',
                                pointBackgroundColor: '#074e6e',
                                tension: 0.2
                            },
                            {
                                data: [3000, 3000, 3000, 3000, 3000, 3000, 3000],
                                label: 'Fabbisogno Calorico Medio',
                                borderColor: 'green',
                                pointBackgroundColor: 'green',
                                borderDash: [5, 5]
                            }
                        ]
                    },
                    options: {
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    usePointStyle: true
                                }
                            }
                        }
                    }
                })
            }
        )
}

getCaloriesLastSevenDays()

// ---------------------------------------------------------------------------------------------------------------
// Section 7

// Goals section

// Div that contains the goals description
const goalDescriptionDiv = document.getElementById("goalDescriptionDiv")

// API Call to get info about the set goals
function getGoalDescription () {
    fetch("http://127.0.0.1:5000/api/most-important-goals")
        .then(response => response.json())
        .then(data => {
            // First paragraph
            let goalDescriptionContent = `<p>I tuoi obbiettivi principali riguardano: <br><br></p>`

            data.forEach(goal => {
                const setGoalListItemContent = `
                    &#x2022; &nbsp;<b>${goal.macro.toUpperCase()}</b>: Qui il valore ideale è stato fissato a <b>${goal.valoreIdeale}${goal.macro === 'calorie' ? 'kcal' : 'g'}</b> per giorno.
                    ${
                        goal.regola === 'entro_range' ? `Per questo macronutriente, il valore minimo da raggiungere è <b>${goal.valoreMinimo}${goal.macro === 'calorie' ? 'kcal' : 'g'}</b> per giorno.
                        Il valore massimo, invece è stato settato a <b>${goal.valoreMassimo}${goal.macro === 'calorie' ? 'kcal' : 'g'}</b> per giorno.` 
                        : `Ti sei prefissato di raggiungere da <b>${goal.valoreMinimo}${goal.macro === 'calorie' ? 'kcal' : 'g'}</b> per giorno in su.`
                    }
                    <br>
                `
                goalDescriptionContent = goalDescriptionContent + setGoalListItemContent
            })

            goalDescriptionDiv.innerHTML = goalDescriptionContent
            goalDescriptionDiv.appendChild(setGoalsList)
        })
}

// API Call
getGoalDescription()

