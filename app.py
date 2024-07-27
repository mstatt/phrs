import streamlit as st
import time
from tqdm import tqdm
from openai import OpenAI
# Function to get AI71 response

def get_openai_response(prompt):
    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = "<API_KEY>"

    client = OpenAI(
	    api_key=AI71_API_KEY,
	    base_url=AI71_BASE_URL,
	)

    response = client.chat.completions.create(
    model="tiiuae/falcon-180B-chat",
    messages=[
        {"role": "user", "content": f"`{prompt}`"},
    ],
)
    return response.choices[0].message.content.strip()
	    
    
# Function to display a simple loading animation
def display_loading_animation():
    loading_placeholder = st.empty()
    for _ in range(5):
        for dots in [".", "..", "..."]:
            loading_placeholder.text(f"Loading{dots}")
            time.sleep(0.3)
    loading_placeholder.empty()

# Streamlit app
st.set_page_config(page_title="Polypharmic Risk Score", layout="wide")
st.title("Polypharmic Risk Score (PHRS)")
txt = "A polypharmic risk score (PHRS) assesses the cumulative risk associated with the repeated use of over-the-counter medications over time. It is determined by evaluating the compounded effects of multiple medication exposures, each contributing to the overall risk based on their potential long-term impacts"

st.write(txt)


st.title("Step 1: Select the over the counter medication. Step 2 Select the Disease")
st.write("Score based on severity: 0 low, 100 highest")

col1, col2 = st.columns(2)

# Initialize session state to store risks
if 'risks' not in st.session_state:
    st.session_state.risks = ""

with col1:
    # OTC Medications dropdown
    otc_meds = ["Acetaminophen", "Ibuprofen", "Aspirin", "Naproxen", "Diphenhydramine", "Loratadine", "Ranitidine", "Famotidine", "Loperamide"]
    selected_med = st.selectbox("Select OTC Medication", otc_meds)

    # Get Risks button
    if st.button("#1 Get Risks"):
        with st.spinner("Fetching risks..."):
            display_loading_animation()
            risks_prompt = f'''You are a highly skilled clinical researcher with over 20 years of experience studying the impacts of over-the-counter medications. Your task is to provide a concise yet comprehensive list of the top 10 long-term health implications regarding the use of {selected_med}.
            For each implication, please provide:
            1. A brief title (1-5 words)
            2. A concise explanation (1-2 sentences)
            3. The severity level (Low, Moderate, High, or Severe)
            4. The estimated frequency of occurrence (Rare, Uncommon, Common, or Very Common)
            Your response should be structured as follows:
            1. [Title]: [Explanation]. Severity: [Level]. Frequency: [Occurrence rate].
            2. [Title]: [Explanation]. Severity: [Level]. Frequency: [Occurrence rate].
            ...
            Ensure that your list covers a range of body systems and potential complications, focusing on the most significant long-term effects based on current medical knowledge. Prioritize accuracy and clinical relevance in your response.'''

            st.session_state.risks = get_openai_response(risks_prompt)
            st.markdown(f"**Risks for {selected_med}:**\n\n{st.session_state.risks}")

with col2:
    # Diseases dropdown
    diseases = ["Cerebrovascular Disease", "Cardiovascular Disease", "Diabetes", "Asthma", "Kidney Disease"]
    selected_disease = st.selectbox("Select Disease", diseases)

    # Get Score button
    if st.button("#2 Get Score"):
        if st.session_state.risks:
            with st.spinner("Calculating score..."):
                display_loading_animation()
                score_prompt = f'''Based on the following risks associated with {selected_med}:

{st.session_state.risks}

                What is the polypharmic risk score for {selected_med} when used by a patient with {selected_disease}? 

                Please provide:
                1. A numerical score from 1-100, where 100 represents the highest risk.
                2. A brief explanation of how you arrived at this score, considering both the medication risks and the specific disease.
                3. Any specific concerns or interactions between the medication and the disease that significantly influence the risk score.
                4. Call out the specific Implications with use over time over time'''

                score_response = get_openai_response(score_prompt)
                st.markdown(f"**Polypharmic Risk Score for {selected_med} with {selected_disease}:**\n\n{score_response}")
        else:
            st.warning("Please get the risks for the medication first by clicking 'Get Risks'.")

# Custom CSS for blue, black, and white theme
st.markdown("""
    <style>
                .st-emotion-cache-10trblm {
            color:#000000
    }
    .stApp {
        background-color: #f0f8ff;
        color: #000000;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4285f4;
        border-radius: 5px;
    }
    .stSelectbox {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
