import streamlit as st
import requests
st.set_page_config(page_title="SmartInsure", page_icon="💳", layout="centered")
st.markdown("<h1 style='text-align: center;'>SmartInsure</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Fill in the details below to estimate premium price.</p>", unsafe_allow_html=True)

FASTAPI_URL = "http://127.0.0.1:8000/predict"
col1,col2 = st.columns(2)
with col1:
    Age = st.number_input("Age",min_value=0, max_value = 100, value=30,step=1)
    Diabetes = st.selectbox("Diabetes",['No','Yes'])
    BloodPressureProblems = st.selectbox("Blood Pressure Problems",['No','Yes'])
    AnyTransplants = st.selectbox("Any Transplants",['No','Yes'])
    AnyChronicDiseases = st.selectbox("Any Chronic Diseases", ["No", "Yes"])
with col2:
    Height = st.number_input("Height",min_value=50.0, max_value = 250.0, value=170.0,step=0.1)
    Weight = st.number_input("Weight (kg)", min_value=10.0, max_value=400.0, value=70.0, step=0.1)
    KnownAllergies = st.selectbox("Known Allergies",['No','Yes'])
    HistoryOfCancerInFamily = st.selectbox("History of Cancer In Family",['No','Yes'])
    NumberOfMajorSurgeries = st.number_input("Number Of Major Surgeries", min_value=0, max_value=10, value=0, step=1)
if st.button('Predict Premium'):
    payload = {
        "Age": int(Age),
        "Diabetes":Diabetes,
        'BloodPressureProblems':BloodPressureProblems,
        'AnyTransplants':AnyTransplants,
        "AnyChronicDiseases": AnyChronicDiseases,
        "Height": float(Height),
        "Weight": float(Weight),
        "KnownAllergies": KnownAllergies,
        "HistoryOfCancerInFamily": HistoryOfCancerInFamily,
        "NumberOfMajorSurgeries": int(NumberOfMajorSurgeries)

    }

    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout = 10)
        if response.status_code == 200:
            result = response.json()
            premium = result["PredictedPremiumPrice"]
            st.metric(label="Predicted Premium Price", value=f"₹ {premium:,.2f}")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("FastAPI backend is not running. Start it first on port 8000.")
    except Exception as e:
        st.error(f"Error: {e}")



