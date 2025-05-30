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

    # Meal type and cooking preferences
    col1, col2 = st.columns(2)
    
    with col1:
        meal_type = st.selectbox(
            "What type of meal?",
            ["Dinner", "Lunch", "Breakfast/Brunch", "Appetizer", "Snack", "Dessert", "Side Dish"]
        )
        
        complexity = st.selectbox(
            "Select cooking complexity:",
            ["Easy", "Medium", "Hard"]
        )
    
    with col2:
        cooking_method = st.selectbox(
            "Preferred cooking method:",
            ["Any method", "One-pot/One-pan", "Slow cooker", "Air fryer", "Instant Pot/Pressure cooker", 
             "Oven/Baking", "Stovetop", "Grilling", "No-cook/Raw", "Microwave"]
        )
        
        portion_size = st.selectbox(
            "How many servings?",
            ["1 person", "2 people", "3-4 people (family)", "5-6 people", "Large group (8+ people)"]
        )

    # Dietary restrictions
    st.subheader("Dietary Preferences")
    col1, col2 = st.columns(2)
    
    with col1:
        vegetarian = st.checkbox("Vegetarian")
        vegan = st.checkbox("Vegan")
        gluten_free = st.checkbox("Gluten-free")
        dairy_free = st.checkbox("Dairy-free")
    
    with col2:
        keto = st.checkbox("Keto")
        paleo = st.checkbox("Paleo")
        low_carb = st.checkbox("Low-carb")
        low_sodium = st.checkbox("Low-sodium")
    
    # Allergy restrictions
    allergies = st.multiselect(
        "Any food allergies to avoid?",
        ["Nuts", "Shellfish", "Eggs", "Soy", "Fish", "Sesame", "Other"]
    )
    


    # Special instructions
    instructions = st.text_input("Any other special instructions or preferences?")

    # Submit button
    if st.button("Suggest Recipe", key="cuisine_recipe"):
        # Build dietary restrictions list
        dietary_restrictions = []
        if vegetarian: dietary_restrictions.append("vegetarian")
        if vegan: dietary_restrictions.append("vegan")
        if gluten_free: dietary_restrictions.append("gluten-free")
        if dairy_free: dietary_restrictions.append("dairy-free")
        if keto: dietary_restrictions.append("keto")
        if paleo: dietary_restrictions.append("paleo")
        if low_carb: dietary_restrictions.append("low-carb")
        if low_sodium: dietary_restrictions.append("low-sodium")
        
        prompt = f"Suggest a {complexity.lower()} {cuisine.lower()} {meal_type.lower()} recipe for {portion_size}"
        
        if cooking_method != "Any method":
            method_mapping = {
                "One-pot/One-pan": "one-pot or one-pan",
                "Slow cooker": "slow cooker",
                "Air fryer": "air fryer",
                "Instant Pot/Pressure cooker": "Instant Pot or pressure cooker",
                "Oven/Baking": "oven-baked",
                "Stovetop": "stovetop",
                "Grilling": "grilled",
                "No-cook/Raw": "no-cook",
                "Microwave": "microwave"
            }
            prompt += f" using {method_mapping[cooking_method]}"
        
        if dietary_restrictions:
            prompt += f" that is {', '.join(dietary_restrictions)}"
        
        if allergies:
            allergy_list = ', '.join([allergy.lower() for allergy in allergies])
            prompt += f". Avoid these allergens: {allergy_list}"
        
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
    st.subheader("Preferences")
    # Meal type and cooking preferences for fridge mode
    col1, col2 = st.columns(2)
    
    with col1:
        fridge_meal_type = st.selectbox(
            "What type of meal?",
            ["Dinner", "Lunch", "Breakfast/Brunch", "Appetizer", "Snack", "Dessert", "Side Dish"],
            key="fridge_meal_type"
        )
        
        fridge_complexity = st.selectbox(
            "Cooking complexity:",
            ["Easy", "Medium", "Hard"],
            key="fridge_complexity"
        )
    
    with col2:
        fridge_cooking_method = st.selectbox(
            "Preferred cooking method:",
            ["Any method", "One-pot/One-pan", "Slow cooker", "Air fryer", "Instant Pot/Pressure cooker", 
             "Oven/Baking", "Stovetop", "Grilling", "No-cook/Raw", "Microwave"],
            key="fridge_cooking_method"
        )
        
        fridge_portion_size = st.selectbox(
            "How many servings?",
            ["1 person", "2 people", "3-4 people (family)", "5-6 people", "Large group (8+ people)"],
            key="fridge_portion_size"
        )
    # Time and ingredient preferences
    col3, col4 = st.columns(2)
    
    with col3:
        cooking_time = st.selectbox(
            "How much time do you have?",
            ["Quick (under 30 min)", "Medium (30-60 min)", "I have time (60+ min)"]
        )
    
    with col4:
        allow_additional = st.checkbox(
            "Allow recipes that need a few additional common ingredients?",
            value=True,
            help="If checked, recipes may include common pantry items you might not have listed"
        )
    
    # Dietary restrictions for fridge mode
    st.subheader("Dietary Preferences")
    col3, col4 = st.columns(2)
    
    with col3:
        fridge_vegetarian = st.checkbox("Vegetarian", key="fridge_vegetarian")
        fridge_vegan = st.checkbox("Vegan", key="fridge_vegan")
        fridge_gluten_free = st.checkbox("Gluten-free", key="fridge_gluten_free")
        fridge_dairy_free = st.checkbox("Dairy-free", key="fridge_dairy_free")
    
    with col4:
        fridge_keto = st.checkbox("Keto", key="fridge_keto")
        fridge_paleo = st.checkbox("Paleo", key="fridge_paleo")
        fridge_low_carb = st.checkbox("Low-carb", key="fridge_low_carb")
        fridge_low_sodium = st.checkbox("Low-sodium", key="fridge_low_sodium")
    
    # Allergy restrictions for fridge mode
    fridge_allergies = st.multiselect(
        "Any food allergies to avoid?",
        ["Nuts", "Shellfish", "Eggs", "Soy", "Fish", "Sesame", "Other"],
        key="fridge_allergies"
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
            
            # Build dietary restrictions list for fridge mode
            fridge_dietary_restrictions = []
            if fridge_vegetarian: fridge_dietary_restrictions.append("vegetarian")
            if fridge_vegan: fridge_dietary_restrictions.append("vegan")
            if fridge_gluten_free: fridge_dietary_restrictions.append("gluten-free")
            if fridge_dairy_free: fridge_dietary_restrictions.append("dairy-free")
            if fridge_keto: fridge_dietary_restrictions.append("keto")
            if fridge_paleo: fridge_dietary_restrictions.append("paleo")
            if fridge_low_carb: fridge_dietary_restrictions.append("low-carb")
            if fridge_low_sodium: fridge_dietary_restrictions.append("low-sodium")
            
            prompt = f"I have these ingredients available: {fridge_items}. "
            prompt += f"Please suggest a {fridge_complexity.lower()} {fridge_meal_type.lower()} recipe for {fridge_portion_size} that is {time_mapping[cooking_time]}"
            
            if fridge_cooking_method != "Any method":
                method_mapping = {
                    "One-pot/One-pan": "one-pot or one-pan",
                    "Slow cooker": "slow cooker",
                    "Air fryer": "air fryer",
                    "Instant Pot/Pressure cooker": "Instant Pot or pressure cooker",
                    "Oven/Baking": "oven-baked",
                    "Stovetop": "stovetop",
                    "Grilling": "grilled",
                    "No-cook/Raw": "no-cook",
                    "Microwave": "microwave"
                }
                prompt += f" using {method_mapping[fridge_cooking_method]}"
            
            if fridge_dietary_restrictions:
                prompt += f" and {', '.join(fridge_dietary_restrictions)}"
            
            if fridge_allergies:
                fridge_allergy_list = ', '.join([allergy.lower() for allergy in fridge_allergies])
                prompt += f". Avoid these allergens: {fridge_allergy_list}"
            
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
