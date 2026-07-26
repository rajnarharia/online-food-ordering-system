import streamlit as st
import time

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
        
    # Simulate typing indicator if last message was user
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        time.sleep(0.5)
        response = f"I'm Foodie AI. I can certainly help you with: '{prompt}'. As a premium assistant, I analyze thousands of data points to give you the perfect culinary advice."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
