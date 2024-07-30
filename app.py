import streamlit as st
import time
from openai import OpenAI
import pandas as pd
import plotly.express as px

# Function to get AI71 response
def get_openai_response(prompt):
    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = ""
    
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

# Function to format risks as a bulleted list
def format_risks(risks):
    risk_items = risks.split('\n')
    formatted_risks = ''.join([f"<li>{item}</li>" for item in risk_items if item.strip()])
    return f"<ul>{formatted_risks}</ul>"

# Streamlit app
st.set_page_config(page_title="Polypharmic Risk Score", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #f0f8ff;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4285f4;
        border-radius: 5px;
    }
    .stSelectbox {
        color: #000000;
    }
    h1, h2, h3, p, .stMarkdown, .stInfo {
        color: #000000 !important;
    }
    .result-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        min-height: 100px;
    }
    .info-box {
        background-color: #e7f3fe;
        border-left: 6px solid #2196F3;
        margin-bottom: 15px;
        padding: 4px 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Polypharmic Risk Score (PHRS)")
st.write("A polypharmic risk score (PHRS) assesses the cumulative risk associated with the repeated use of over-the-counter medications over time. It is determined by evaluating the compounded effects of multiple medication exposures, each contributing to the overall risk based on their potential long-term impacts. The polyPHarmic Risk Score was originally developed by Michael Stattelman and this solution was developed for submission in the AI71/lablab.ai FalconLLM hack-a-thon.")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_med' not in st.session_state:
    st.session_state.selected_med = None

if 'risks_fetched' not in st.session_state:
    st.session_state.risks_fetched = False

if 'previous_med' not in st.session_state:
    st.session_state.previous_med = None

st.header("Step 1: Select 1st OTC medication. Step 2: Select 2nd OTC medication.")
st.write("Score based on severity: 0 low, 100 highest")

col1, col2 = st.columns(2)

otc_meds = ["Acetaminophen", "Ibuprofen", "Aspirin", "Naproxen", "Diphenhydramine (Benadryl)", "Cetirizine (Zyrtec)", "Loratadine (Claritin)", "Fexofenadine (Allegra)", "Dextromethorphan (Robitussin, Delsym)","Guaifenesin (Mucinex)","Loperamide (Imodium)","Pseudoephedrine (Sudafed)","Ranitidine (Zantac)"]

with col1:
    selected_med = st.selectbox("Select OTC Medication", otc_meds, key="med1")
    
    # Check if the selection has changed
    if selected_med != st.session_state.previous_med:
        st.session_state.risks_fetched = False
        st.session_state.previous_med = selected_med
    
    st.session_state.selected_med = selected_med

    if st.button("#1 Get Risks", key="get_risks"):
        with st.spinner("Fetching risks..."):
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
            st.session_state.score = ''
            st.session_state.risks_fetched = True

with col2:
    # Filter out the selected medication from the first dropdown
    remaining_meds = [med for med in otc_meds if med != st.session_state.selected_med]
    selected_med2 = st.selectbox("Select 2nd OTC Medication", remaining_meds, key="med2")

    if st.button("#2 Get Score", key="get_score", disabled=not st.session_state.risks_fetched):
        if 'risks' in st.session_state and st.session_state.risks:
            with st.spinner("Calculating score..."):
                score_prompt = f'''Based on the following risks associated with {st.session_state.selected_med}:

{st.session_state.risks}

                What is the polypharmic risk score on a scale of 1-100 with 100 being immediate mortality, for {st.session_state.selected_med} when used with {selected_med2}? 

                Please provide:
                1. A numerical score from 1-100, where 100 represents the highest risk.
                2. A brief explanation of how you arrived at this score, considering both of the medications.
                3. Any specific concerns or interactions between the medications that significantly influence the risk score.
                4. Call out the specific Implications with use over time over time. (provide implications for each of the following time periods:
                a) 1 month .
                b) 6 months.
                c) 1 year
                d) 5 years.'''

                st.session_state.score = get_openai_response(score_prompt)
                
                # Add to history
                st.session_state.history.append({
                    "Medication": st.session_state.selected_med,
                    "Medication 2": selected_med2,
                    "Score": st.session_state.score.split('\n')[0]  # Assuming the score is the first line
                })
        else:
            st.warning("Please get the risks for the medication first by clicking 'Get Risks'.")

# Display results
col3, col4 = st.columns(2)

with col3:
    if 'risks' in st.session_state and st.session_state.risks:
        st.subheader("Risks:")
        formatted_risks = format_risks(st.session_state.risks)
        st.markdown(f'<div class="result-box">{formatted_risks}</div>', unsafe_allow_html=True)

with col4:
    if 'score' in st.session_state and st.session_state.score:
        st.subheader("Polypharmic Risk Score:")
        st.markdown(f'<div class="result-box">{st.session_state.score}</div>', unsafe_allow_html=True)

# Additional Information
st.header("Additional Information")
st.markdown("""
<div class="info-box">
<h3>Understanding Polypharmic Risk</h3>
<p>Polypharmic risk refers to the potential health hazards associated with taking multiple medications simultaneously. This risk increases with the number of medications used, especially when combining over-the-counter (OTC) drugs with prescription medications.</p>
</div>

<div class="info-box">
<h3>Tips for Minimizing Polypharmic Risk</h3>
<ul>
    <li>Always consult with your healthcare provider or pharmacist before starting a new medication, even if it's OTC.</li>
    <li>Keep an up-to-date list of all medications you're taking, including OTC drugs, supplements, and herbal remedies.</li>
    <li>Be aware of potential drug interactions and side effects.</li>
    <li>Regularly review your medications with your healthcare provider to ensure they're all still necessary.</li>
</ul>
</div>

<div class="info-box">
<h3>Disclaimer</h3>
<p>This tool provides general information and is not a substitute for professional medical advice. Always consult with a qualified healthcare provider before making decisions about your health or medication regimen.</p>
</div>
""", unsafe_allow_html=True)
