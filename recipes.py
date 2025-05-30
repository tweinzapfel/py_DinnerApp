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

# Add tabs for different recipe modes
tab1, tab2 = st.tabs(["Recipe by Cuisine", "Recipe by Fridge Items"])

with tab1:
    st.header("Find Recipe by Cuisine & Preferences")
    
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
    if st.button("Suggest Recipe", key="cuisine_recipe"):
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

with tab2:
    st.header("Find Recipe by What's in Your Fridge")
    
    # Fridge items input
    st.subheader("What ingredients do you have?")
    fridge_items = st.text_area(
        "List the ingredients you have available (separate with commas):",
        placeholder="e.g., chicken, rice, onions, bell peppers, garlic, tomatoes",
        height=100
    )
    
    # Additional preferences for fridge mode
    col1, col2 = st.columns(2)
    
    with col1:
        fridge_complexity = st.selectbox(
            "Cooking complexity:",
            ["Easy", "Medium", "Hard"],
            key="fridge_complexity"
        )
    
    with col2:
        fridge_vegetarian = st.checkbox("Vegetarian only?", key="fridge_vegetarian")
    
    # Cooking time preference
    cooking_time = st.selectbox(
        "How much time do you have?",
        ["Quick (under 30 min)", "Medium (30-60 min)", "I have time (60+ min)"]
    )
    
    # Additional ingredients option
    allow_additional = st.checkbox(
        "Allow recipes that need a few additional common ingredients?",
        value=True,
        help="If checked, recipes may include common pantry items you might not have listed"
    )
    
    # Special dietary restrictions or preferences
    fridge_instructions = st.text_input(
        "Any dietary restrictions or special requests?",
        key="fridge_instructions"
    )

    # Submit button for fridge mode
    if st.button("Find Recipe with My Ingredients", key="fridge_recipe"):
        if not fridge_items.strip():
            st.warning("Please enter at least some ingredients from your fridge!")
        else:
            # Build prompt for fridge-based recipe
            time_mapping = {
                "Quick (under 30 min)": "quick and easy, taking less than 30 minutes",
                "Medium (30-60 min)": "moderate cooking time, around 30-60 minutes", 
                "I have time (60+ min)": "can take longer to prepare, 60+ minutes"
            }
            
            prompt = f"I have these ingredients available: {fridge_items}. "
            prompt += f"Please suggest a {fridge_complexity.lower()} dinner recipe that is {time_mapping[cooking_time]}"
            
            if fridge_vegetarian:
                prompt += " and vegetarian"
            
            if allow_additional:
                prompt += ". You can suggest recipes that use most of these ingredients and may require a few common pantry staples (like oil, salt, pepper, basic spices) that most people have."
            else:
                prompt += ". Please try to use primarily the ingredients I've listed."
            
            if fridge_instructions:
                prompt += f" Also consider: {fridge_instructions}"
            
            prompt += " Include a complete ingredient list (highlighting what I already have vs. what I might need to get) and step-by-step cooking instructions."

            # Make request to OpenAI
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful chef assistant who specializes in creating recipes based on available ingredients. Always clearly indicate which ingredients the user already has vs. which they might need to purchase."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.markdown("### Recipe Based on Your Ingredients")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
