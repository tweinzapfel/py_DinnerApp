import streamlit as st
from openai import OpenAI
import os

headers = {
    "authorization": st.secrets["api_key"],
    "content-type": "application/json"
}

# Set your OpenAI API key (make sure it's in your environment variables or you can paste it here for testing)
client = OpenAI(api_key=st.secrets["api_key"])

# Streamlit UI
st.title("Dinner Recipe Maker")

# Cuisine dropdown
cuisine = st.selectbox(
    "Select a cuisine type:",
    [
    "American",
    "Barbecue",
    "Chinese",
    "French",
    "Greek",
    "Indian",
    "Italian",
    "Japanese",
    "Korean",
    "Latin American",
    "Mediterranean",
    "Mexican",
    "Middle Eastern",
    "Seafood",
    "Southern/Soul Food",
    "Tex-Mex",
    "Thai",
    "Vegan/Vegetarian",
    "Vietnamese",
    "Other"
]
)

# Complexity dropdown
complexity = st.selectbox(
    "Select cooking complexity:",
    ["Easy", "Medium", "Hard"]
)

# Vegetarian checkbox
vegetarian = st.checkbox("Should it be vegetarian?")

# Special instructions
instructions = st.text_input("Any special instructions or preferences?")

# Submit button
if st.button("Suggest Recipe"):
    prompt = f"Suggest a {complexity.lower()} {cuisine.lower()} dinner recipe"
    if vegetarian:
        prompt += " that is vegetarian"
    if instructions:
        prompt += f". Also, consider this: {instructions}"
    prompt += ". Include ingredients and step-by-step instructions."

    # Make request to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chef assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        st.markdown("### Suggested Recipe")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occurred: {e}")
