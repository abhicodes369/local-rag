import streamlit as st
import requests
import matplotlib.pyplot as plt
import os
import pickle
from datetime import datetime
import re
import time
from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate

# Ensure conversations directory exists
CONVERSATIONS_DIR = "conversations"
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

# please add your usda api key for the project 
API_KEY = ""
BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Session State Initialization
if "current_conversation_id" not in st.session_state:
    st.session_state['current_conversation_id'] = None
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_food' not in st.session_state:
    st.session_state.current_food = None
if 'last_analyzed_food' not in st.session_state:
    st.session_state.last_analyzed_food = None
if 'last_food_quantity' not in st.session_state:
    st.session_state.last_food_quantity = 1

# Ollama Model Setup
# use model as per your machines requirements
llm = Ollama(model="llama3.2:1b")

# System Prompt
system_message = SystemMessagePromptTemplate.from_template("""
You are a helpful AI nutrition assistant. Provide detailed nutritional insights about food, recipes, and dietary information.
Respond comprehensively to queries about nutrition, ingredients, and health-related food topics.
""")


def fetch_food_items():
    food_groups = [
        'Fruits', 'Vegetables', 'Grains', 'Protein Foods',
        'Dairy', 'Seafood', 'Nuts', 'Seeds'
    ]
    all_foods = []

    for group in food_groups:
        endpoint = f"{BASE_URL}/foods/search"
        params = {
            "api_key": API_KEY,
            "query": group,
            "pageSize": 50
        }

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'foods' in data:
                    group_foods = [
                        food['description'] for food in data['foods']
                        if food.get('description')
                    ]
                    all_foods.extend(group_foods)
        except Exception as e:
            st.error(f"Error fetching {group}: {e}")

    return sorted(list(set(all_foods)))

# Get food nutrition
def get_food_nutrition(food_item, quantity=1):
    endpoint = f"{BASE_URL}/foods/search"
    params = {
        "api_key": API_KEY,
        "query": food_item,
        "pageSize": 1
    }

    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'foods' in data and data['foods']:
                food = data['foods'][0]
                nutrients = food.get('foodNutrients', [])

                # Process nutrients with quantity scaling
                nutrition_info = {
                    'Calories': None,
                    'Protein': None,
                    'Fat': None,
                    'Carbohydrates': None,
                    'Fiber': None,
                    'Vitamins/Minerals': []
                }

                for nutrient in nutrients:
                    name = nutrient.get('nutrientName', '')
                    value = float(nutrient.get('value', 0))
                    unit = nutrient.get('unitName', '')

                    # Scale nutrient values based on quantity
                    scaled_value = value * quantity

                    if 'Energy' in name:
                        nutrition_info['Calories'] = f"{scaled_value:.1f} {unit}"
                    elif 'Protein' in name:
                        nutrition_info['Protein'] = f"{scaled_value:.1f} {unit}"
                    elif 'Total lipid (fat)' in name:
                        nutrition_info['Fat'] = f"{scaled_value:.1f} {unit}"
                    elif 'Carbohydrate' in name:
                        nutrition_info['Carbohydrates'] = f"{scaled_value:.1f} {unit}"
                    elif 'Fiber' in name:
                        nutrition_info['Fiber'] = f"{scaled_value:.1f} {unit}"

                    if any(x in name.lower() for x in ['vitamin', 'mineral', 'calcium', 'iron', 'zinc']):
                        nutrition_info['Vitamins/Minerals'].append(f"{name}: {scaled_value:.1f} {unit}")

                # Update session state
                st.session_state.last_analyzed_food = food_item
                st.session_state.last_food_quantity = quantity

                return nutrition_info, food

        st.error("No nutrition data found.")
        return None, None

    except Exception as e:
        st.error(f"Error fetching nutrition: {e}")
        return None, None

# Generate AI Response
def generate_conversational_response(user_query):
    context = f"""Nutrition Context:
- Last Analyzed Food: {st.session_state.last_analyzed_food or 'None'}
- Last Food Quantity: {st.session_state.last_food_quantity} serving(s)

User Query: {user_query}

Guidelines:
- Provide precise, scientifically-based nutrition advice
- Include specific nutritional values when possible
- Focus on health, diet, and food insights"""

    try:
        response = llm.predict(context)
        return response
    except Exception as e:
        st.error(f"Error generating conversational response: {e}")
        return ""

# Create Nutrition Chart
def create_nutrition_chart(nutrition_info):
    data = {}
    for key in ['Calories', 'Protein', 'Fat', 'Carbohydrates', 'Fiber']:
        if nutrition_info.get(key):
            try:
                value = float(re.findall(r'[\d.]+', nutrition_info[key])[0])
                data[key] = value
            except (IndexError, ValueError):
                continue

    if data:
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(data.keys(), data.values())
        ax.set_title('Nutritional Content Overview')
        ax.set_xlabel('Nutrients')
        ax.set_ylabel('Amount')
        plt.xticks(rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

        st.pyplot(fig)

# Main Application
def run():
    st.title("🍎 FoodGO")

    st.sidebar.header("Nutrition Exploration")

    nav_option = st.sidebar.radio("Choose Mode", ["Nutrition Analysis", "Conversational Mode"])

    # Nutrition Analysis Mode with Quantity Control
    if nav_option == "Nutrition Analysis":
        analysis_type = st.sidebar.radio("Choose Analysis Type", ["Select from List", "Custom Food/Recipe"])

        # Quantity input
        quantity = st.number_input("Enter Quantity", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

        if analysis_type == "Select from List":
            food_items = fetch_food_items()
            selected_food = st.selectbox("Choose a Food Item", food_items)
            food_to_analyze = selected_food
        else:
            food_to_analyze = st.text_input("Enter Food Item or Recipe", placeholder="e.g., Grilled Salmon, Quinoa Salad")

        if st.button("Analyze Nutrition"):
            if food_to_analyze:
                st.session_state.current_food = food_to_analyze
                nutrition_info, _ = get_food_nutrition(food_to_analyze, quantity)

                if nutrition_info:
                    st.subheader(f"Nutritional Details for {food_to_analyze}")
                    create_nutrition_chart(nutrition_info)
                    st.table({
                        'Nutrient': list(nutrition_info.keys())[:5],
                        'Value': list(nutrition_info.values())[:5]
                    })

    # Conversational Mode
    elif nav_option == "Conversational Mode":
        st.subheader("Nutrition Conversation")

        # Conversation History
        for message in st.session_state.conversation_history:
            st.chat_message(message['role']).write(message['content'])

        # User Input
        user_query = st.chat_input("Ask a nutrition question")

        if user_query:
            st.session_state.conversation_history.append({
                'role': 'user',
                'content': user_query
            })
            st.chat_message("user").write(user_query)

            # Generate AI Response
            ai_response = generate_conversational_response(user_query)
            st.chat_message("assistant").write(ai_response)

            st.session_state.conversation_history.append({
                'role': 'assistant',
                'content': ai_response
            })

    # Clear Conversation Button
    if st.sidebar.button("Clear Conversation"):
        st.session_state.conversation_history.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    run()
