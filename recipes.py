import streamlit as st
from openai import OpenAI
import os
import requests

headers = {
    "authorization": st.secrets["api_key"],
    "content-type": "application/json"
}

# Set your OpenAI API key (make sure it's in your environment variables or you can paste it here for testing)
client = OpenAI(api_key=st.secrets["api_key"])


# ——— UI setup ———
st.set_page_config(page_title="Dinner Suggester", page_icon="🍽️")
st.title("🍽️ What's for Dinner?")

# Mode selection: Standard or Fridge Mode
mode = st.radio(
    "Choose mode:",
    ["Standard Suggestion", "What’s in My Fridge?"]
)

# Form for inputs
with st.form("dinner_form"):
    if mode == "Standard Suggestion":
        cuisine = st.selectbox(
            "Choose a cuisine:",
            ["Italian", "Mexican", "Tex-Mex", "Chinese", "Indian", "Mediterranean", "American", "Thai", "Japanese", "French"]
        )
        complexity = st.selectbox(
            "Cooking complexity:",
            ["Easy to prepare", "Medium", "Complex"]
        )
        vegetarian = st.checkbox("Vegetarian only")
        extra = st.text_input(
            "Anything else? (e.g. no nuts, kid-friendly, low-carb…)",
            placeholder="Enter any special requirements here"
        )
    else:
        ingredients = st.text_area(
            "List the ingredients you have (separated by commas):",
            placeholder="e.g., chicken, bell pepper, garlic, onion"
        )
        vegetarian = st.checkbox("Vegetarian only")
        extra = st.text_input(
            "Anything else? (e.g. no nuts, kid-friendly, low-carb…)",
            placeholder="Enter any special requirements here"
        )

    submitted = st.form_submit_button("Suggest Dinner")

# Handle submission
if submitted:
    # Build prompt based on mode
    if mode == "Standard Suggestion":
        prompt = (
            f"Suggest a {complexity.lower()} {('vegetarian ' if vegetarian else '')}"
            f"{cuisine.lower()} dinner recipe"
        )
        if extra:
            prompt += f", {extra}"
    else:
        prompt = (
            f"I have the following ingredients: {ingredients}. "
            f"Please suggest a {('vegetarian ' if vegetarian else '')}recipe I can make using these ingredients"
        )
        if extra:
            prompt += f", {extra}"
    prompt += ".\n\nPlease provide a detailed list of ingredients and step-by-step cooking instructions."

    # Optional: display headers for debugging
    st.write("Using headers:", headers)

    # Call the OpenAI API via HTTP request
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }
    with st.spinner("Asking the chef…"):
        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chef assistant."},
                {"role": "user", "content": prompt}
            ]
        )
            response.raise_for_status()
            data = response.json()
            recipe = data["choices"][0]["message"]["content"].strip()
            st.subheader("Here’s your recipe:")
            st.markdown(recipe)
        except Exception as e:
            st.error(f"Error: {e}")
