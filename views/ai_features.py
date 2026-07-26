import streamlit as st
import time
import json

def get_ai_response(prompt):
    # Simple rule-based engine parsing foods.json
    try:
        with open("data/foods.json", "r") as f:
            foods = json.load(f)
    except Exception:
        foods = []
        
    p = prompt.lower()
    
    if "vegetarian" in p or "veg" in p:
        veg_items = [f for f in foods if f.get("is_veg")]
        if veg_items:
            names = ", ".join([f['name'] for f in veg_items])
            return f"I found some great vegetarian options for you: {names}. Would you like to order any of these?"
            
    if "protein" in p:
        # Sort by protein naive parsing (assuming "Xg")
        def get_protein(f):
            try:
                return int(f.get("nutrition_info", {}).get("protein", "0").replace("g", ""))
            except:
                return 0
        high_protein = sorted(foods, key=get_protein, reverse=True)
        if high_protein:
            top = high_protein[0]
            return f"The best high-protein meal we have is the {top['name']} with {top['nutrition_info']['protein']} of protein! It's {top['calories']} calories."
            
    if "popular" in p or "trending" in p:
        popular = sorted(foods, key=lambda x: x.get("popularity", 0), reverse=True)
        if popular:
            return f"Our most popular dish right now is the {popular[0]['name']}! It has an amazing rating of {popular[0]['rating']} stars."
            
    if "ingredients" in p or "explain" in p:
        return "I can explain the ingredients of any dish on our menu. Just tell me which dish you are curious about!"
        
    # Fallback search
    matches = [f for f in foods if p in f['name'].lower() or p in f.get('category', '').lower()]
    if matches:
        return f"I found the {matches[0]['name']}. It costs ${matches[0]['price']} and is a delicious choice."
        
    return "I'm Foodie AI. I can recommend dishes based on your dietary needs, tell you what's popular, or explain ingredients. How can I help?"

def render_ai_features():
    st.markdown("<h1 class='section-title' style='margin-bottom: 8px;'>AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='body-text' style='margin-bottom: 32px;'>Your intelligent culinary companion. Ask for recommendations, nutrition info, or meal plans.</p>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi there! I'm your Foodie AI. How can I help you today?"}]

    # Quick action chips
    st.markdown(
        """
        <style>
        .ai-chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 100px;
            font-size: 14px;
            color: #9CA3AF;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 24px;
        }
        .ai-chip:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #FFF;
            border-color: rgba(255, 255, 255, 0.2);
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    cq1, cq2, cq3, cq4 = st.columns(4)
    with cq1: 
        if st.button("Recommend high protein meals", use_container_width=True): st.session_state.prompt_action = "Recommend high protein meals"
    with cq2: 
        if st.button("What's popular right now?", use_container_width=True): st.session_state.prompt_action = "What's popular right now?"
    with cq3: 
        if st.button("Vegetarian dinner ideas", use_container_width=True): st.session_state.prompt_action = "Vegetarian dinner ideas"
    with cq4:
        if st.button("Explain the ingredients", use_container_width=True): st.session_state.prompt_action = "Explain the ingredients"
        
    st.write("<br>", unsafe_allow_html=True)

    # Chat UI Container
    with st.container(border=True, height=450):
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: flex-end; margin-bottom: 16px;'>
                        <div style='background: #FF5A5F; color: #FFF; padding: 12px 16px; border-radius: 16px 16px 4px 16px; max-width: 80%; font-size: 15px;'>
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

    # Input Area
    prompt = st.chat_input("Message Foodie AI...")
    
    # Handle quick actions or input
    if hasattr(st.session_state, 'prompt_action'):
        prompt = st.session_state.prompt_action
        del st.session_state.prompt_action
        
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun() # Refresh to show user message
        
    # Execute AI Logic
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        time.sleep(0.5)
        last_prompt = st.session_state.messages[-1]["content"]
        response = get_ai_response(last_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
