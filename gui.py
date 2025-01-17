import pickle  
import numpy as np
from PIL import Image
import base64
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import  matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import requests
import os
from datetime import datetime

# Defining the cultivation process steps through dictionary
crop_steps = {
    "rice": [
        "1. Prepare the field by plowing and leveling the soil.",
        "2. Flood the field with water before sowing seeds.",
        "3. Sow rice seeds directly or transplant seedlings.",
        "4. Maintain standing water during early stages of growth.",
        "5. Apply nitrogen-based fertilizers as top dressing.",
        "6. Control weeds manually or using herbicides.",
        "7. Drain water when the grains start to ripen.",
        "8. Harvest when grains turn golden yellow."
    ],
    "maize": [
        "1. Plow and till the soil to make it loose and aerated.",
        "2. Sow seeds 2 inches deep with proper spacing.",
        "3. Water regularly, especially during germination.",
        "4. Apply balanced fertilizers containing NPK.",
        "5. Control weeds with manual weeding or herbicides.",
        "6. Monitor for pests like corn borers and apply pesticides if needed.",
        "7. Harvest when the kernels are hard and fully developed."
    ],
   "jute": [
        "1. Prepare loamy, well-drained soil with organic matter.",
        "2. Sow seeds directly into the soil in rows.",
        "3. Keep the field moist but avoid waterlogging.",
        "4. Apply nitrogen-rich fertilizers for better growth.",
        "5. Control weeds with hand weeding or shallow plowing.",
        "6. Harvest when the plants start flowering.",
        "7. Ret the stalks in water to separate fibers."
    ],
    "cotton": [
        "1. Prepare sandy loam soil with good drainage.",
        "2. Sow seeds in rows at a depth of 1 inch.",
        "3. Water regularly, but avoid overwatering.",
        "4. Apply fertilizers rich in potassium and phosphorus.",
        "5. Use pesticides to control bollworms and other pests.",
        "6. Monitor for diseases like leaf spot and take action.",
        "7. Harvest cotton bolls when they burst open."
    ],
    "coconut": [
        "1. Select well-drained soil in a sunny location.",
        "2. Plant young coconut seedlings in deep pits.",
        "3. Water regularly to keep the soil moist.",
        "4. Apply organic manure or fertilizers every few months.",
        "5. Protect from pests like rhinoceros beetles and mites.",
        "6. Harvest mature coconuts after 12 months from flowering."
    ],
    "papaya": [
        "1. Choose well-drained soil rich in organic matter.",
        "2. Plant papaya seeds in nursery beds for germination.",
        "3. Transplant seedlings to the main field after 1 month.",
        "4. Water regularly but avoid waterlogging.",
        "5. Apply nitrogen-rich fertilizers during the growing stage.",
        "6. Protect from pests like papaya fruit flies.",
        "7. Harvest fruits when they turn yellowish-green."
    ],
    "orange": [
        "1. Plant orange saplings in sandy loam soil with good drainage.",
        "2. Water regularly, especially during dry spells.",
        "3. Apply fertilizers containing nitrogen, phosphorus, and potassium.",
        "4. Prune dead or diseased branches annually.",
        "5. Control pests like aphids and citrus greening disease.",
        "6. Harvest oranges when they are fully ripe and bright orange."
    ],
       "apple": [
        "1. Plant apple saplings in cold climates with fertile soil.",
        "2. Water moderately, avoiding waterlogging.",
        "3. Fertilize the soil with nitrogen and phosphorus annually.",
        "4. Prune branches to maintain tree shape and health.",
        "5. Control pests like apple maggots and diseases like scab.",
        "6. Harvest when apples are firm, ripe, and colorful."
    ],
    "muskmelon": [
        "1. Prepare sandy soil with good drainage and organic manure.",
        "2. Sow seeds directly into the soil in raised beds.",
        "3. Water moderately to avoid fruit cracking.",
        "4. Apply fertilizers rich in potassium and phosphorus.",
        "5. Protect from pests like fruit flies and aphids.",
        "6. Harvest muskmelons when the skin turns yellowish."
    ],
    "watermelon": [
        "1. Plant seeds in sandy, well-drained soil with organic compost.",
        "2. Ensure adequate sunlight and regular watering.",
        "3. Apply fertilizers with potassium for fruit development.",
        "4. Protect from pests like aphids and diseases like powdery mildew.",
        "5. Harvest watermelons when the tendril near the fruit dries."
    ],
    "grapes": [
        "1. Plant grapevines in well-drained soil with full sunlight.",
        "2. Water regularly but avoid overwatering.",
        "3. Prune vines to encourage fruiting.",
        "4. Apply balanced fertilizers with potassium and phosphorus.",
        "5. Control pests like mealybugs and diseases like mildew.",
        "6. Harvest grapes when they are fully ripe and sweet."
    ],
    "mango": [
        "1. Plant mango saplings in loamy soil with good drainage.",
        "2. Water young plants regularly but sparingly for mature trees.",
        "3. Fertilize with nitrogen, phosphorus, and potassium.",
        "4. Prune branches to maintain tree health.",
        "5. Protect from pests like hoppers and diseases like anthracnose.",
        "6. Harvest mangoes when they are mature but not fully ripe."
    ],
    "banana": [
        "1. Plant banana suckers in well-drained, fertile soil.",
        "2. Water regularly to maintain moist soil.",
        "3. Apply fertilizers rich in potassium and nitrogen.",
        "4. Support plants with stakes to prevent bending.",
        "5. Protect from pests like weevils and diseases like leaf spot.",
        "6. Harvest bananas when the fruit is plump and green."
    ],
    "pomegranate": [
        "1. Plant saplings in loamy soil with good drainage.",
        "2. Water sparingly as pomegranates are drought-tolerant.",
        "3. Apply fertilizers with nitrogen and phosphorus annually.",
        "4. Prune dead or diseased branches to maintain shape.",
        "5. Protect from pests like aphids and fruit borers.",
        "6. Harvest fruits when they turn red and are slightly soft."
    ],
    "lentil": [
        "1. Plant lentil seeds in well-drained soil with moderate fertility.",
        "2. Water sparingly as lentils are drought-tolerant.",
        "3. Apply nitrogen fertilizers during early growth.",
        "4. Control weeds with manual weeding or herbicides.",
        "5. Harvest when the pods turn brown and dry."
    ],
    "coffee": [
        "1. Plant coffee saplings in fertile soil with shade.",
        "2. Water regularly to maintain moisture but avoid waterlogging.",
        "3. Apply organic manure or nitrogen-based fertilizers.",
        "4. Prune plants to maintain shape and productivity.",
        "5. Protect from pests like coffee borer beetles.",
        "6. Harvest coffee cherries when they turn bright red."
    ],
    "blackgram": [
        "1. Prepare sandy loam soil for blackgram cultivation.",
        "2. Sow seeds at a depth of 4-5 cm and ensure proper spacing.",
        "3. Apply phosphorus-rich fertilizers at the sowing stage.",
        "4. Irrigate only during dry periods, as blackgram is drought-tolerant.",
        "5. Monitor for pod borers and leaf-eating pests.",
        "6. Harvest when pods turn brown and seeds are hard."
    ],
    "mungbean": [
        "1. Use well-drained soil with moderate fertility for mungbean cultivation.",
        "2. Sow seeds at a shallow depth (3-4 cm).",
        "3. Apply balanced fertilizers rich in phosphorus.",
        "4. Irrigate during flowering and pod development stages.",
        "5. Control pests like aphids and whiteflies.",
        "6. Harvest when pods mature and dry on the plant."
    ],
    "mothbeans": [
        "1. Select sandy loam soil with good drainage for mothbean farming.",
        "2. Sow seeds at the onset of the monsoon season.",
        "3. Irrigate sparingly, as mothbeans are drought-resistant.",
        "4. Apply organic manure or compost before sowing.",
        "5. Control pests like pod borers and aphids.",
        "6. Harvest when pods dry and seeds are hard."],
    "pigeonpeas":[ 
        "1. Choose well-drained, fertile soil for pigeonpeas.",
        "2. Sow seeds 3-5 cm deep and space them adequately.",
        "3. Apply fertilizers rich in phosphorus and potassium.",
        "4. Irrigate regularly during flowering and pod development.",
        "5. Monitor for pests like pod borers and wilt disease.",
        "6. Harvest when the pods turn brown and dry."],
    "kidneybeans":[
        "1. Plant kidney bean seeds in fertile, well-drained soil.",
        "2. Sow seeds 4-5 cm deep with proper spacing.",
        "3. Apply phosphorus fertilizers before sowing.",
        "4. Water regularly during flowering and pod formation.",
        "5. Protect from pests like aphids and beetles.",
        "6. Harvest when pods are mature and dry."],
    "chickpea":[
        "1. Use loamy soil rich in organic matter for chickpea farming.",
        "2. Sow seeds at a depth of 4-6 cm with adequate spacing.",
        "3. Apply phosphorus fertilizers at the sowing stage.",
        "4. Avoid overwatering; chickpeas prefer dry conditions.",
        "5. Monitor for pests like pod borers and aphids.",
        "6. Harvest when pods turn yellowish-brown."],
    "peas": [
        "1. Prepare the field with loamy soil for peas cultivation.",
        "2. Sow seeds 2-3 cm deep with proper spacing.",
        "3. Water sparingly, as peas do not require much irrigation.",
        "4. Apply balanced fertilizers at the sowing stage.",
        "5. Monitor for pests like aphids and cutworms.",
        "6. Harvest when pods are green and fully developed."],
    "cowpeas":[
        "1. Plant cowpea seeds in well-drained, sandy soil.",
        "2. Sow seeds at a depth of 2-3 cm with adequate spacing.",
        "3. Irrigate sparingly, as cowpeas are drought-tolerant.",
        "4. Apply fertilizers rich in phosphorus at sowing.",
        "5. Control pests like aphids and pod borers.",
        "6. Harvest when pods are mature and dry."],
    "groundnuts": [
        "1. Use sandy or loamy soil with good drainage for groundnuts.",
        "2. Sow seeds 5-7 cm deep with proper spacing.",
        "3. Apply phosphorus-rich fertilizers at sowing.",
        "4. Water sparingly but avoid prolonged dry spells.",
        "5. Monitor for pests like leaf miners and aphids.",
        "6. Harvest when the plant turns yellow and pods mature."
    ],
    "beans": [
        "1. Choose fertile, well-drained soil for beans cultivation.",
        "2. Sow seeds 3-4 cm deep with proper spacing.",
        "3. Water regularly but avoid overwatering.",
        "4. Apply fertilizers rich in potassium and phosphorus.",
        "5. Protect from pests like aphids and leafhoppers.",
        "6. Harvest when pods are green and tender."
    ],
    "Soybeans": [
        "1. Select well-drained soil rich in organic matter for soybeans.",
        "2. Sow seeds 4-5 cm deep with proper spacing.",
        "3. Apply nitrogen-fixing inoculants to seeds before planting.",
        "4. Irrigate during flowering and pod formation stages.",
        "5. Control pests like aphids and soybean loopers.",
        "6. Harvest when pods turn brown and dry."
    ],
    "wheat": [
        "1. Use loamy soil with high fertility for wheat cultivation.",
        "2. Sow seeds at a depth of 4-5 cm and ensure proper spacing.",
        "3. Apply nitrogen, phosphorus, and potassium fertilizers.",
        "4. Irrigate regularly, especially during tillering and flowering.",
        "5. Control weeds and pests like wheat rust and aphids.",
        "6. Harvest when the grains are hard and the plant turns golden."
    ],
    "tobacco": [
        "1. Prepare well-drained soil for tobacco farming.",
        "2. Sow seeds in nursery beds and transplant when seedlings are 6-8 weeks old.",
        "3. Irrigate regularly but avoid waterlogging.",
        "4. Apply balanced fertilizers rich in potassium.",
        "5. Monitor for pests like aphids and whiteflies.",
        "6. Harvest when the leaves turn yellow and mature."
    ]
}

# Defining functions for each page 

def home():
    st.image("logo.png", width=600, use_container_width=False)
    
    # Styling Welcome Text
    st.markdown(
        """
        <div style="text-align: top; margin-top: 8px;">
            <h1 style="color: #4CAF50;">Welcome To The Crop Guide</h1>
            <p style="font-size: 20px; color: #555;">CropGuide: your smart farming companion! Get personalized crop recommendations, real-time weather updates, and expert advice to help you grow better and harvest smarter.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to encode image as base64
def get_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Loading the pre-trained models and scalers
randclf = pickle.load(open('model.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))

# Input fields to input various parameters for crop recommendation
def crop_recommendation():
    st.markdown(
    '<h1 style="color: #4CAF50;">Crop Recommendation</h1>',
    unsafe_allow_html=True
)
    
    # Input fields
    col1, col2 = st.columns(2)
    ph = col1.number_input("Enter PH value", min_value=0.0, max_value=14.0, step=0.1, value=6.50)
    col1.write(f"PH value is: {ph}")
    N = col2.number_input("Enter N value", min_value=0, max_value=200, step=1, value=90)
    col2.write(f"N value is: {N}")

    col3, col4 = st.columns(2)
    K = col3.number_input("Enter K value", min_value=0, max_value=200, step=1, value=43)
    col3.write(f"K value is: {K}")
    P = col4.number_input("Enter P value", min_value=0, max_value=200, step=1, value=42)
    col4.write(f"P value is: {P}")

    col5, col6 = st.columns(2)
    temperature = col5.number_input("Enter temperature value (°C)", min_value=0.0, max_value=50.0, step=0.1, value=20.87)
    col5.write(f"Temperature value is: {temperature}")
    humidity = col6.number_input("Enter humidity value (%)", min_value=0.0, max_value=100.0, step=0.1, value=82.00)
    col6.write(f"Humidity value is: {humidity}")

    rainfall = st.number_input("Enter rainfall value (mm)", min_value=0.0, max_value=500.0, step=0.1, value=202.93)
    st.write(f"Rainfall value is: {rainfall}")

    # creating a button for pridition of crop  
    if st.button("**Predict**"):
        try:
            # Prepare input data
            features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            mx_features = mx.transform(features)
            sc_features = sc.transform(mx_features)

            # Make prediction
            prediction = randclf.predict(sc_features)[0]

            # Crop names mapping 
            crop_names = {
                0: "rice", 1: "maize", 2: "jute", 3: "cotton", 4: "coconut",
                5: "papaya", 6: "orange", 7: "apple", 8: "muskmelon", 9: "watermelon",
                10: "grapes", 11: "mango", 12: "banana", 13: "pomegranate", 14: "lentil",
                15: "blackgram", 16: "mungbean", 17: "mothbeans", 18: "pigeonpeas",
                19: "kidneybeans", 20: "chickpea", 21: "coffee", 22: "peas",
                23: "cowpeas", 24: "groundnuts", 25: "beans", 26: "Soyabeans",
                27: "wheat", 28: "tobacco"
            }

            crop_name = crop_names[prediction]
            st.success(f"The recommended crop to grow is: {crop_name}")

            # Display a pridicted crop image
            image_path = f"Image/{crop_name}.jpg"

            # loading and encoding the image
            image_base64 = get_image_as_base64(image_path)
            if image_base64:
                st.image(f"data:image/jpeg;base64,{image_base64}", caption=crop_name.capitalize(), use_container_width=True)
            else:
                st.write("Image not available for this crop.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# function for display_weather_data 

def display_weather_data():
    st.markdown(
    '<h1 style="color: #4CAF50;">Weather Dashboard</h1>',
    unsafe_allow_html=True
)

    # Input the location using Streamlit widget
    user_api = '372c960ed77cf28656120462cddb6b25'
    location = st.text_input("Enter the city name:")

    if location:
        # Build the API link
        Api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
        api_link = requests.get(Api_link)

        if api_link.status_code == 200:  # Check if the API request is successful
            api_data = api_link.json()
            # Creating variables to store and display data
            temp_city = round(api_data['main']['temp'] - 273.15, 2)  # Convert to Celsius and round
            weather_desc = api_data['weather'][0]['description']
            hmdt = api_data['main']['humidity']
            wind_spd = api_data['wind']['speed']
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
            # Displaying the data in Streamlit
            st.markdown(
             f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h2 style="color: #4CAF50; text-align: center;">Weather Details</h2>
            <p style="font-size: 18px; color: #333;"><b>Location:</b> {location.capitalize()}</p>
            <p style="font-size: 18px; color: #333;"><b>Temperature:</b> {temp_city}°C</p>
            <p style="font-size: 18px; color: #333;"><b>Weather Description:</b> {weather_desc.capitalize()}</p>
            <p style="font-size: 18px; color: #333;"><b>Humidity:</b> {hmdt}%</p>
            <p style="font-size: 18px; color: #333;"><b>Wind Speed:</b> {wind_spd} m/s</p>
            <p style="font-size: 18px; color: #333;"><b>Date & Time:</b> {date_time}</p>
            </div>
             """,
            unsafe_allow_html=True
)

# if city is not found then write error
        else:
          st.markdown(
           f"""
           <div style="color: #4CAF50; font-size: 18px; font-weight: bold; text-align: center; margin-top: 20px;">
            City not found, please check the name and try again.
            </div>
              """,
            unsafe_allow_html=True
    )

# Functin for cultivation_process
def cultivation_process():
    # Add a background image
    page_bg = """
    <style>
    .stApp {
        background-image: url('images/7.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

    # styling title
    st.markdown(
        '<h1 style="color: #4CAF50; text-align: center; margin-top: 20px;">Cultivation Process</h1>',
        unsafe_allow_html=True
    )

    # Style the selected box with rounded shape
    st.markdown(
        """
        <style>
        .stSelectbox label {
            font-size: 18px;
            color: #4CAF50;
            font-weight: bold;
        }
        .stSelectbox div[data-baseweb="select"] {
            background-color: #f9f9f9;
            border-radius: 25px;  /* Make the select box rounded */
            border: 1px solid #ddd;
            font-size: 16px;
            padding: 5px 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a select box for selecting crop
    crop = st.selectbox(
        "Select a crop",
        options=["Select"] + list(crop_steps.keys()),
        index=0
    )

    # Show the cultivation process for the selected crop
    if crop != "Select":
        st.markdown(
            f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h2 style="color: #4CAF50;">Cultivation Process for {crop.capitalize()}:</h2>
                <ul style="font-size: 18px; color: #333; line-height: 1.6;">
        """,
            unsafe_allow_html=True
        )
        for step in crop_steps[crop]:
            st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="color: #FF0000; font-size: 18px; font-weight: bold; text-align: center; margin-top: 20px;">
                Please select a crop to view its cultivation process.
            </div>
            """,
            unsafe_allow_html=True
        )

# Main app layout
st.set_page_config(layout="centered")  

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
# function for data_analysis 
def data_analysis():
    try:
        data = pd.read_csv("Crop_recommendation.csv")
    except FileNotFoundError:
        st.error("Crop_recommendation.csv not found. Please ensure it is in the working directory.")
        return

    st.markdown(
    '<h1 style="color: #4CAF50;">Crop Data Visualizations</h1>',
    unsafe_allow_html=True
)

    # Bar Graph for average nutrient levels by crop
    avg_nutrients = data.groupby('label')[['N', 'P', 'K']].mean()
    st.subheader("Average Nutrient Levels by Crop")
    fig1, ax1 = plt.subplots()
    avg_nutrients.plot(kind='bar', ax=ax1, figsize=(12, 6))
    ax1.set_title("Average Nutrient Levels (N, P, K) by Crop")
    ax1.set_xlabel("Crop")
    ax1.set_ylabel("Nutrient Levels")
    ax1.legend(title="Nutrients")
    st.pyplot(fig1)

    # Scatter Plot: Temperature vs. Humidity
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=data, x='temperature', y='humidity', hue='label', palette='tab10', legend=False, ax=ax2)
    ax2.set_title("Temperature vs. Humidity for Different Crops")
    ax2.set_xlabel("Temperature (°C)")
    ax2.set_ylabel("Humidity (%)")
    st.pyplot(fig2)

    # Box Plot for Rainfall Distribution
    st.subheader("Rainfall Distribution by Crop")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=data, x='label', y='rainfall', palette='pastel',  ax=ax3)
    ax3.set_xlabel("Crop")
    ax3.set_ylabel("Rainfall (mm)")
    ax3.tick_params(axis='x', rotation=90)
    st.pyplot(fig3)

    # Line Graph for pH Levels
    st.subheader("Line Graph: Average pH Levels by Crop")
    avg_ph = data.groupby('label')['ph'].mean().reset_index()
    fig4, ax4 = plt.subplots()
    sns.lineplot(data=avg_ph, x='label', y='ph', marker='o', ax=ax4)
    ax4.set_title("Average pH Levels by Crop")
    ax4.set_xlabel("Crop")
    ax4.set_ylabel("pH Level")
    ax4.tick_params(axis='x', rotation=90)
    st.pyplot(fig4)

    # Heatmap for Correlation Matrix
    st.subheader("Heatmap: Correlation Matrix")
    corr = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].corr()
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax5, linewidths=0.5)
    ax5.set_title("Correlation Matrix of Nutrient and Environmental Factors")
    st.pyplot(fig5)

    # Histogram for Nutrient Distribution (Nitrogen)
    st.subheader("Histogram: Distribution of Nitrogen (N) Levels")
    fig6, ax6 = plt.subplots()
    sns.histplot(data['N'], bins=20, kde=True, color='green', ax=ax6)
    ax6.set_title("Distribution of Nitrogen (N) Levels")
    ax6.set_xlabel("Nitrogen (N) Level")
    ax6.set_ylabel("Frequency")
    st.pyplot(fig6)

    # Histogram for pH Distribution
    st.subheader("Histogram: pH Level Distribution")
    fig7, ax7 = plt.subplots()
    sns.histplot(data['ph'], bins=20, kde=True, color='blue', ax=ax7)
    ax7.set_title("Distribution of pH Levels")
    ax7.set_xlabel("pH Level")
    ax7.set_ylabel("Frequency")
    st.pyplot(fig7)

    # Pie chart for Crop Labels distribution
    st.subheader("Pie Chart: Distribution of Crops")
    crop_counts = data['label'].value_counts()
    fig8, ax8 = plt.subplots(figsize=(7, 7))
    ax8.pie(crop_counts, labels=crop_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', n_colors=len(crop_counts)))
    ax8.set_title("Crop Distribution by Label")
    st.pyplot(fig8)

    st.success("Visualizations loaded successfully!")

# Slidebar navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu", 
        ["Home", "Crop Recommendation", "Weather Dashboard", "Cultivation Process", "Data Analysis & Visualization", "Financial Assistance"], 
        icons=["house", "star", "cloud-sun-rain", "tools", "graph-up", "hand-holding-usd"], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f9f9f9"},
            "icon": {"color": "#4CAF50", "font-size": "18px"},  # Icon color and size
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#eeeeee"
            },
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},  # Selected item styles
        }
    )

# Function for financial_assistance    
def financial_assistance():
    st.markdown(
    '<h1 style="color: #4CAF50;">Financial Assistance</h1>',
    unsafe_allow_html=True
)
    st.write(
        """
        Financial Support Information for Farmers in Pakistan.
        
        This section provides detailed information on available resources, subsidies, loans, grants, and NGOs working towards the welfare of farmers in Pakistan. Farmers can use these options to improve productivity, reduce costs, and adopt sustainable practices.
        """
    )

    # Government Subsidies Section
    with st.expander("1. Government Subsidies for Farmers"):
        st.subheader("Fertilizer Subsidies")
        st.write(
            """
            The government offers subsidies on fertilizers like urea and DAP to make them affordable for farmers. 
            This ensures soil fertility and enhanced crop yields at reduced costs.
            """
        )
        st.markdown(
            """
            **Contact:** Ministry of National Food Security & Research  
            **Phone:** +92 51 9204811  
            **Email:** [info@mnfsr.gov.pk](mailto:info@mnfsr.gov.pk)  
            **Website:** [Visit Website](http://www.mnfsr.gov.pk)
            """
        )

        st.subheader("Seed Subsidies")
        st.write(
            """
            Certified, high-yield seeds for crops such as wheat, rice, and cotton are provided at subsidized rates. 
            These seeds resist pests and harsh weather, leading to higher productivity.
            """
        )
        st.markdown(
            """
            **Contact:** Federal Seed Certification & Registration Department  
            **Phone:** +92 51 9260591  
            **Website:** [Visit Website](http://www.mnfsr.gov.pk/frmDetails.aspx?opt=dept&id=3)
            """
        )

    # Agricultural Loans Section
    with st.expander("2. Agricultural Loans and Grants"):
        st.subheader("State Bank of Pakistan Agricultural Credit Schemes")
        st.write(
            """
            These schemes offer loans for crop production, farm mechanization, and livestock development at low-interest rates.
            """
        )
        st.markdown(
            """
            **Phone:** +92 21 111 727 111  
            **Website:** [Visit Website](https://www.sbp.org.pk/Acme/index.htm)
            """
        )

        st.subheader("Zarai Taraqiati Bank Limited (ZTBL)")
        st.write(
            """
            ZTBL provides loans for seeds, fertilizers, machinery, irrigation, and land development, focusing on empowering rural farmers.
            """
        )
        st.markdown(
            """
            **Helpline:** 111-30-30-30  
            **Website:** [Visit Website](https://www.ztbl.com.pk)
            """
        )

    # NGOs Section
    with st.expander("3. NGOs Supporting Farmers"):
        st.subheader("Indus Earth Trust")
        st.write(
            """
            This organization promotes sustainable farming practices and water conservation to reduce reliance on erratic rainfall.
            """
        )
        st.markdown(
            """
            **Phone:** +92 21 3530 0825  
            **Website:** [Visit Website](http://www.indusearthtrust.org)
            """
        )

        st.subheader("Rural Support Programs Network (RSPN)")
        st.write(
            """
            RSPN focuses on empowering rural communities through microfinance, technical training, and resources for small-scale farmers.
            """
        )
        st.markdown(
            """
            **Phone:** +92 51 8491270-79  
            **Website:** [Visit Website](http://www.rspn.org)
            """
        )

    # International Organizations Section
    with st.expander("4. International Organizations"):
        st.subheader("Food and Agriculture Organization (FAO)")
        st.write(
            """
            FAO provides technical assistance, training, and funding for sustainable farming practices in Pakistan.
            """
        )
        st.markdown(
            """
            **Phone:** +92 51 9255490-93  
            **Website:** [Visit Website](https://www.fao.org/pakistan)
            """
        )

        st.subheader("International Fund for Agricultural Development (IFAD)")
        st.write(
            """
            IFAD aims to alleviate rural poverty through financial aid, grants, and technical expertise in agriculture.
            """
        )
        st.markdown(
            """
            **Website:** [Visit Website](https://www.ifad.org/en/web/operations/w/country/pakistan)
            """
        )
 
# Display content based on the selected menu option
if selected == "Home":
    home()

elif selected == "Crop Recommendation":
    crop_recommendation()

elif selected == "Weather Dashboard":
    display_weather_data()

elif selected == "Cultivation Process":
    cultivation_process()

elif selected == "Data Analysis & Visualization":
    data_analysis()

elif selected ==  "Financial Assistance":
    financial_assistance()

    