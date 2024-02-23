import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from convex import ConvexClient

#load_dotenv(".env.local")
#load_dotenv()

#client = ConvexClient(os.getenv("CONVEX_URL"))
#print(client.query("tasks:get"))



# -------------------- CSS BEGINNING --------------------

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url(https://images.pexels.com/photos/13923313/pexels-photo-13923313.jpeg);
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
background-position: calc(50% - 3rem) center;
opacity: 0.75;
filter: brightness(100%);
}

p {
color: dark-blue;
font-weight: 700;
}

h1 {
    text-align: center;
    background-color: #ff6699; /* Cor de fundo chamativa */
    color: #ffffff; /* Cor do texto */
    padding: 20px;
    border-radius: 10px; /* Bordas arredondadas */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); /* Sombra */
    border: 2px solid #ffffff; /* Borda sólida */
    background-image: linear-gradient(45deg, #808080, #aaaaaa, #000000); /* Gradiente */
    font-size: 1.2rem;
    margin-bottom: 1.2rem;
    opacity: 0.75;
}

.row-widget.stButton {
    text-align: center;
    margin-left: -1rem;
}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#-------------------- CSS END --------------------

# -------------------- GLOBAL VARIABLES BEGINNING --------------------

dataUser = {}

ingredients = {}

fruits = [
    "Apple",
    "Banana",
    "Orange",
    "Strawberry",
    "Pineapple",
    "Grape",
    "Pear",
    "Watermelon",
    "Cherry",
    "Kiwi"
]

roots = [
    "Carrot",
    "Beetroot",
    "Potato",
    "Parsnip",
    "Radish",
    "Yam",
    "Ginger",
    "Turnip",
    "Rutabaga",
    "Celery"
]

seeds = [
    "Sunflower seeds",
    "Pumpkin seeds",
    "Sesame seeds",
    "Flaxseeds",
    "Chia seeds",
    "Poppy seeds",
    "Mustard seeds",
    "Pumpkin seeds",
    "Watermelon seeds",
    "Black sesame seeds"
]

activity = [
    "Sedentary",
    "Slightly active",
    "Moderately active",
    "Very active", 
    "Extremely active",
    "Choose your Activity Factors"
]

workout = [
    1.2,
    1.375,
    1.55,
    1.725,
    1.9
]

# -------------------- GLOBAL VARIABLES END --------------------

#Function to check empty entries:

def checkEmptyInputs():
    for value in ingredients.values():
        if value == '':
            return True
    for value in dataUser.values():
        if value == '':
            return True

# -------------------- FUNCTIONS BEGINNING --------------------

#Function to calculate daily Kcal by gender

def nutritionalValues(genre, workoutNumber, weight, height, age):
    if genre == "Masculine":
        kcal = (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)) * workoutNumber
    elif genre == "Feminine":
        kcal = (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)) * workoutNumber
    else:
        return None
    protein = weight * 0.8
    carbo = (kcal * 0.55) / 4
    saturatedFat = (kcal * 0.10) / 9
    unsaturatedFat = (kcal * 0.30) / 9
    return [kcal, protein, carbo, saturatedFat, unsaturatedFat]

#Title
st.markdown("<h1>Wellness Portions</h1>", unsafe_allow_html=True)
st.write("<span class='textIntro'>The Wellness Portions offers a selection of juices and smoothies made up of at least 1 and up to 3 ingredients ranging from fruits, seeds, and roots. Each Wellness Portion contains 300 ml that will be proportionally divided among the necessary quantities of each ingredient to achieve the nutritional values proportional to the user's weight.</span>", unsafe_allow_html=True)

#Main Function

def main():
    st.sidebar.title('Wellness Portions')
    pages = st.sidebar.selectbox('To Order and To Nourish', ['To Order', 'To Nourish'])
        
    if pages == 'To Order':
        #Capturing User Data
        with st.form(key="dataUser_form"):
        #Splitting the screen into two columns
            col1, col2 = st.columns(2)
            with col1:
                for i in range(6):
                    if i == 0:
                        dataUser["Name"] = st.text_input(f"Name", key=f"dataUser_{i}")
                    elif i == 1:
                        dataUser["Age"] = st.text_input(f"Age (years)", key=f"dataUser_{i}")
                    elif i == 2:
                        dataUser["Height"] = st.text_input(f"Height (centimetres)", key=f"dataUser_{i}")
                    elif i == 3:
                        dataUser["Weight"] = st.text_input(f"Weight (kilograms)", key=f"dataUser_{i}")
                    elif i == 4:
                        mascOrFem = ["Masculine", "Feminine", "Choose your Genre"]
                        optionsmascOrFem = st.selectbox("Masculine or Feminine", mascOrFem, index=(len(mascOrFem) - 1))
                        if optionsmascOrFem and optionsmascOrFem != "Choose your Genre":
                            dataUser["Masculine or Feminine"] = optionsmascOrFem
                    elif i == 5:
                        activityFactors = activity
                        optionsActivityFactors = st.selectbox("Activity Factors", activity, index=(len(activityFactors) - 1))
                        if optionsActivityFactors and optionsActivityFactors != "Choose your Activity Factors":
                            dataUser["Activity Factors"] = optionsActivityFactors
                            workoutNumber = activity.index(dataUser["Activity Factors"])

        #Capturing Ingredients data
            with col2:
                for i in range(4):
                    if i == 0:
                        waterOrMilk = ["Water", "Milk", "Choose your Base"]
                        optionsWaterOrMilk = st.selectbox("Water or Milk", waterOrMilk, index=(len(waterOrMilk) - 1))
                        if optionsWaterOrMilk and optionsWaterOrMilk != "Choose your Base":
                            ingredients["Water or Milk"] = f"You choose {optionsWaterOrMilk}-Based juice"
                    elif i == 1:
                        fruitsSeedsRoots = ["Fruit", "Seed", "Root", "Choose your first Ingredients"]
                        optionsFruitsSeedsRoots = st.selectbox("Fruits, Seeds or Roots", fruitsSeedsRoots, index=(len(fruitsSeedsRoots) - 1))
                        if optionsFruitsSeedsRoots == "Fruit":
                            choosedFruit = st.selectbox("1º Fruits", fruits)
                            ingredients["First Ingredient"] = f"You choose {choosedFruit} to be the first ingredient"
                        elif optionsFruitsSeedsRoots == "Seed":
                            choosedSeed = st.selectbox("1º Seeds", seeds)
                            ingredients["First Ingredient"] = f"You choose {choosedSeed} to be the first ingredient"
                        elif optionsFruitsSeedsRoots == "Root":
                            choosedRoot = st.selectbox("1º Roots", roots)
                            ingredients["First Ingredient"] = f"You choose {choosedRoot} to be the first ingredient"     
                    elif i == 2:
                        fruitsSeedsRoots = ["Fruit", "Seed", "Root", "Choose your second Ingredients"]
                        optionsFruitsSeedsRoots = st.selectbox("Fruits, Seeds or Roots", fruitsSeedsRoots, index=(len(fruitsSeedsRoots) - 1))
                        if optionsFruitsSeedsRoots == "Fruit":
                            choosedFruit = st.selectbox("2º Fruits", fruits)
                            ingredients["Second Ingredient"] = f"You choose {choosedFruit} to be the second ingredient"
                        elif optionsFruitsSeedsRoots == "Seed":
                            choosedSeed = st.selectbox("2º Seeds", seeds)
                            ingredients["Second Ingredient"] = f"You choose {choosedSeed} to be the second ingredient"
                        elif optionsFruitsSeedsRoots == "Root":
                            choosedRoot = st.selectbox("2º Roots", roots)
                            ingredients["Second Ingredient"] = f"You choose {choosedRoot} to be the second ingredient"
                    elif i == 3:
                        fruitsSeedsRoots = ["Fruit", "Seed", "Root", "Choose your third Ingredients"]
                        optionsFruitsSeedsRoots = st.selectbox("Fruits, Seeds or Roots", fruitsSeedsRoots, index=(len(fruitsSeedsRoots) - 1))
                        if optionsFruitsSeedsRoots == "Fruit":
                            choosedFruit = st.selectbox("3º Fruits", fruits)
                            ingredients["Third Ingredient"] = f"You choose {choosedFruit} to be the third ingredient"
                        elif optionsFruitsSeedsRoots == "Seed":
                            choosedSeed = st.selectbox("3º Seeds", seeds)
                            ingredients["Third Ingredient"] = f"You choose {choosedSeed} to be the third ingredient"
                        elif optionsFruitsSeedsRoots == "Root":
                            choosedRoot = st.selectbox("3º Roots", roots)
                            ingredients["Third Ingredient"] = f"You choose {choosedRoot} to be the third ingredient"
            inputDataUserFormButton = st.form_submit_button("Let's blend up!")
    elif pages == 'To Nourish':
        col3, col4, col5 = st.columns(3)
        with col3:
            st.image("Smoothie-photo.png", caption='Juices and Smoothies', use_column_width=True)
        with col4:
            st.image("qrcode-pix.png", caption='QR Code', use_column_width=True)
        with col5:
            data = {
    'Nutrient': ['Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fibers', 'Total Sugars', 'Includes Added Sugars', 'Protein', 'Vitamin D', 'Calcium', 'Iron', 'Potassium', 'Vitamin A', 'Vitamin C', 'Thiamin', 'Riboflavin', 'Niacin'],
    'Values': ['6g', '2.5g', '0g', '20mg', '17g', '3g', '11g', '0g', '3g', '0mcg', '18mg', '1mg', '258mg', '29mcg', '21mg', '0mg', '0mg', '0mg', '0mg']
            }            
            df = pd.DataFrame(data)
            df.index += 1
            st.table(df)
    #if inputDataUserFormButton:
    #        pass
            



    

#Button to submit inputs and display them at the next page
#st.markdown(<button onclick="window.location.href = 'outra_pagina.html';">Ir para outra página</button>)

#if st.button("Let's blend up!"):
    #st.query_params.page = 'outra_pagina'
    #st.write("User data")
    #for key, value in dataUser.items():
    #    st.write(f"{key}: {value} {type(value)}")
    #st.write("Ingredients:")
    #for key, value in ingredients.items():
    #    st.write(f"{key}: {value}")

# -------------------- FUNCTIONS END --------------------

# -------------------- FUNCTIONS TRIGGER BEGINNING --------------------

if __name__ == "__main__":
    main()

# -------------------- FUNCTIONS TRIGGER END --------------------

#Nutritional Table

#Content 
#nutritionalValues(dataUser["Masculine or Feminine"], workout[workoutNumber], int(dataUser["Weight"]), int(dataUser["Height"]), int(dataUser["Age"]))
    
# -------------------- PAGE CHANGER BEGINNING --------------------
    
#if page_cliente == "page2":

#Page Changer Variable

# Verify the keys of Page Changer



# -------------------- PAGE CHANGER END --------------------