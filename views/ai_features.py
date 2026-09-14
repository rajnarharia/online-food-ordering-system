import streamlit as st
import time
from database.db import get_foods

def get_recommendations(prompt):
    foods = get_foods()
    p = prompt.lower()
    
    # Intent extraction
    wants_veg = "veg" in p or "vegetarian" in p
    wants_nonveg = "non-veg" in p or "chicken" in p or "meat" in p or "beef" in p
    wants_protein = "protein" in p or "muscle" in p
    wants_low_cal = "calorie" in p or "diet" in p or "light" in p
    budget = None
    if "under" in p or "cheap" in p:
        budget = 300 # arbitrary low budget
        import re
        nums = re.findall(r'\d+', p)
        if nums: budget = int(nums[0])
        
    # Scoring
    def calculate_score(food):
        score = food['rating'] * 10 + food['popularity'] * 0.5
        if wants_veg and food['is_veg']: score += 50
        if wants_nonveg and not food['is_veg']: score += 50
        
        try:
            protein_val = int(''.join(filter(str.isdigit, str(food.get('nutrition_protein', '0')))))
            if wants_protein: score += protein_val * 2
        except: pass
        
        if wants_low_cal and food.get('calories', 1000) < 400: score += 50
        if budget and food['price'] <= budget: score += 50
        elif budget and food['price'] > budget: score -= 100
        
        # Word match in name/desc
        for word in p.split():
            if len(word) > 3 and (word in food['name'].lower() or word in str(food.get('category','')).lower()):
                score += 30
                
        return score
        
    scored_foods = [(f, calculate_score(f)) for f in foods]
    scored_foods.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2 positive score foods
    top_matches = [f for f, score in scored_foods if score > 0][:2]
    
    if not top_matches:
        # fallback to popular
        return "I couldn't find an exact match for that, but here are some of our most popular items!", sorted(foods, key=lambda x: x['popularity'], reverse=True)[:2]
        
    msg = "Here are my top recommendations based on your preferences:"
    if wants_protein: msg = "These are excellent high-protein choices:"
    elif wants_veg: msg = "Here are some fantastic vegetarian options:"
    elif budget: msg = f"Here are great options that fit your budget:"
    
    return msg, top_matches

def render_ai_features():
    st.markdown("<h1 class='section-title' style='margin-bottom: 8px;'>Smart Food Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='body-text' style='margin-bottom: 32px;'>Your intelligent culinary companion. Ask for recommendations, nutrition info, or meal plans based on our menu.</p>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi there! I'm your Smart Food Assistant. How can I help you find the perfect meal today?", "foods": []}]

    cq1, cq2, cq3, cq4 = st.columns(4)
    with cq1: 
        if st.button("Recommend high protein meals", use_container_width=True): st.session_state.prompt_action = "Recommend high protein meals"
    with cq2: 
        if st.button("What's popular right now?", use_container_width=True): st.session_state.prompt_action = "What's popular right now?"
    with cq3: 
        if st.button("Vegetarian dinner ideas", use_container_width=True): st.session_state.prompt_action = "Vegetarian dinner ideas"
    with cq4:
        if st.button("Meals under ₹300", use_container_width=True): st.session_state.prompt_action = "Meals under 300"
        
    st.write("<br>", unsafe_allow_html=True)

    with st.container():
        for msg_idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-end; margin-bottom: 16px;'>
                        <div style='background: #F59E0B; color: #FFF; padding: 12px 16px; border-radius: 16px 16px 4px 16px; max-width: 80%; font-size: 15px;'>
                            {msg['content']}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-start; margin-bottom: 16px;'>
                        <div style='background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #FFF; padding: 12px 16px; border-radius: 16px 16px 16px 4px; max-width: 80%; font-size: 15px; line-height: 1.5;'>
                            {msg['content']}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if msg.get("foods"):
                    cols = st.columns(len(msg["foods"]) + 1)
                    for i, food in enumerate(msg["foods"]):
                        with cols[i]:
                            with st.container():
                                st.markdown(f"<img src='{food.get('image_url', '')}' style='width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 8px;' />", unsafe_allow_html=True)
                                st.write(f"**{food['name']}**")
                                st.write(f"₹{food['price']} | {food.get('calories', 0)} kcal")
                                if st.button(f"Add to Cart", key=f"ai_add_{msg_idx}_{food['id']}", use_container_width=True):
                                    existing = next((item for item in st.session_state.cart if item['id'] == food['id']), None)
                                    if existing:
                                        existing['quantity'] += 1
                                    else:
                                        f_add = food.copy()
                                        f_add['quantity'] = 1
                                        st.session_state.cart.append(f_add)
                                    st.toast(f"Added {food['name']} to cart!")
                                    st.rerun()

    prompt = st.chat_input("Message Food Assistant...")
    
    if hasattr(st.session_state, 'prompt_action'):
        prompt = st.session_state.prompt_action
        del st.session_state.prompt_action
        
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
        
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        time.sleep(0.5)
        last_prompt = st.session_state.messages[-1]["content"]
        text_response, recommended_foods = get_recommendations(last_prompt)
        st.session_state.messages.append({"role": "assistant", "content": text_response, "foods": recommended_foods})
        st.rerun()
