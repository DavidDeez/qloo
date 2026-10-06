import streamlit as st
import requests
import os

# --- Configuration ---
st.set_page_config(page_title="ClientVibe | B2B Intelligence", page_icon="🍷", layout="wide")

QLOO_API_URL = "https://hackathon.api.qloo.com"
# For a real app, load this from st.secrets or env variables
# But for the hackathon prototype, we will just use it directly or let the user input it.
QLOO_API_KEY = "hack_73913cf282adf18cb8c9efd647b5aa88d0138b97"

def fetch_qloo_insights(query):
    """
    Mock function to represent hitting the Qloo API.
    In a real implementation, you would query /search or /entities 
    and map the correlations.
    """
    # Try the real API first
    headers = {
        "x-api-key": QLOO_API_KEY,
        "Accept": "application/json"
    }
    try:
        # Example using the search endpoint
        res = requests.get(f"{QLOO_API_URL}/search", headers=headers, params={"query": query}, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        pass
    
    # Fallback mock data for demo purposes if the API is slow/unavailable
    return {
        "correlations": {
            "dining": ["Farm-to-table", "Natural Wine Bars", "Omakase"],
            "gifts": ["Aesop Skincare", "Mid-century architecture books", "Artisanal Matcha"],
            "travel": ["Tulum", "Kyoto", "Copenhagen"]
        }
    }

# --- UI ---
st.title("🏆 ClientVibe")
st.subheader("Turn small talk into high-end, hyper-personalized client relationships.")

with st.sidebar:
    st.header("Client Profile")
    st.write("Enter details you learned from your client.")
    client_name = st.text_input("Client Name", "Alex (VP of Sales)")
    target_city = st.text_input("Target City", "New York")
    
    st.write("### Cultural Markers")
    st.caption("What did they mention?")
    music_taste = st.text_input("Music", "The National, Radiohead")
    fashion_taste = st.text_input("Fashion/Brands", "A.P.C, Patagonia")
    travel_taste = st.text_input("Travel", "Tulum, Mexico")
    
    analyze_btn = st.button("Generate Intelligence Report", type="primary")

if analyze_btn:
    st.divider()
    with st.spinner(f"Analyzing {client_name}'s cultural profile with Qloo..."):
        # We pass a combined string to our mock/real function
        combined_query = f"{music_taste} {fashion_taste} {travel_taste}"
        insights = fetch_qloo_insights(combined_query)
        
        st.success("Analysis Complete!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 🍽️ Dining Recommendations in {target_city}")
            st.write(f"Based on {client_name}'s preference for {music_taste}, they heavily index for:")
            for item in insights.get("correlations", {}).get("dining", ["Farm-to-table"]):
                st.write(f"- **{item}**")
            
            st.info("💡 **Agent Suggestion:** Avoid standard steakhouses. Book a table at *Le Crocodile* or *Rhodora Wine Bar*.")

        with col2:
            st.markdown("### 🎁 Closing Gift Ideas")
            st.write("Instead of generic wine or a mug, Qloo's taste graph suggests:")
            for item in insights.get("correlations", {}).get("gifts", ["Aesop Skincare"]):
                st.write(f"- **{item}**")
            
            st.info("💡 **Agent Suggestion:** Send a *Phaidon Architecture Book* with a handwritten note referencing their recent trip.")

        st.divider()
        st.write("### 📝 Drafted Email")
        draft = f"""
        Hi {client_name},
        
        Great speaking with you today! I remember you mentioning you were a fan of {music_taste.split(',')[0]} and had a great time in {travel_taste.split(',')[0]}. 
        
        If you're free next week in {target_city}, I'd love to grab dinner. I know a great natural wine spot that I think fits exactly your vibe. 
        
        Best,
        Your Name
        """
        st.code(draft, language="markdown")
