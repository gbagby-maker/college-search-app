import streamlit as st
import requests

# 1. Configuration & API Setup
API_KEY = "vGYj45AO3FjpMf7HreaqsMTvvoON2WIMpBkQruly"
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools.json"

st.set_page_config(page_title="College Research Assistant", page_icon="🎓")

# 2. Session State Initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 3. Helper Function for Navigation
def next_step():
    st.session_state.step += 1

# 4. User Interface Logic
st.title("🎓 College Research Assistant")
st.write("---")

if st.session_state.step == 1:
    st.subheader("Academic Profile")
    gpa = st.number_input("What is your current unweighted GPA?", min_value=0.0, max_value=4.0, value=3.5, step=0.1)
    rigor = st.selectbox("How would you describe your course rigor?", ["Standard", "Honors", "Mostly Honors/AP", "Extremely Rigorous (IB/Full AP)"])
    if st.button("Continue"):
        st.session_state.answers.update({"gpa": gpa, "rigor": rigor})
        next_step()
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("Extracurriculars")
    ec = st.text_input("What are your top 2 extracurricular priorities?")
    if st.button("Continue"):
        st.session_state.answers["ec"] = ec
        next_step()
        st.rerun()

elif st.session_state.step == 3:
    st.subheader("Academic Profile (Major)")
    certainty = st.radio("How certain are you about your intended major?", ["Undecided", "Somewhat decided", "Very certain"])
    major = st.text_input("What is your intended major?")
    if st.button("Continue"):
        st.session_state.answers.update({"certainty": certainty, "major": major})
        next_step()
        st.rerun()

elif st.session_state.step == 4:
    st.subheader("Interests & Learning Style")
    style = st.text_area("Tell me about your general interests and learning style.")
    if st.button("Continue"):
        st.session_state.answers["style"] = style
        next_step()
        st.rerun()

elif st.session_state.step == 5:
    st.subheader("Campus Size")
    size = st.multiselect("What campus size preferences do you have?", ["Small (< 2,000 students)", "Medium (2,000 - 15,000 students)", "Large (15,000+ students)"])
    if st.button("Continue"):
        st.session_state.answers["size"] = size
        next_step()
        st.rerun()

elif st.session_state.step == 6:
    st.subheader("College Experience")
    vibe = st.text_input("What are your top priorities for your college experience?")
    if st.button("Continue"):
        st.session_state.answers["vibe"] = vibe
        next_step()
        st.rerun()

elif st.session_state.step == 7:
    st.subheader("Geography")
    zip_code = st.text_input("What is your ZIP code?")
    drive_hours = st.slider("How many hours away from home are you willing to drive?", 1, 12, 4)
    if st.button("Continue"):
        st.session_state.answers.update({"zip": zip_code, "dist": drive_hours * 55})
        next_step()
        st.rerun()

elif st.session_state.step == 8:
    st.subheader("Testing")
    test_opt = st.radio("Would you like to see only test-optional schools?", ["No", "Yes"])
    sat = None
    if test_opt == "No":
        sat = st.number_input("What is your SAT/ACT score? (SAT equivalent)", min_value=400, max_value=1600, value=1200)
    
    if st.button("Continue"):
        st.session_state.answers.update({"test_optional": test_opt, "sat": sat})
        next_step()
        st.rerun()

elif st.session_state.step == 9:
    st.subheader("Financial Fit")
    income = st.selectbox("Select your family income bracket:", ["$0 - $30k", "$30k - $75k", "$75k - $150k", "$150k+"])
    if st.button("Generate My List"):
        st.session_state.answers["income"] = income
        next_step()
        st.rerun()

elif st.session_state.step == 10:
    st.subheader("Your Initial College List")
    with st.spinner("Finding your matches..."):
        params = {
            "api_key": API_KEY,
            "zip": st.session_state.answers["zip"],
            "distance": f"{st.session_state.answers['dist']}mi",
            "fields": "id,school.name,school.city,school.state,latest.admissions.admission_rate.overall,latest.admissions.sat_scores.average.overall",
            "per_page": 20
        }
        try:
            response = requests.get(BASE_URL, params=params).json()
            schools = response.get("results", [])

            if not schools:
                st.warning("No schools found in that driving range. Try starting over with a larger distance!")
            else:
                for s in schools:
                    st.write(f"### {s['school.name']}")
                    st.write(f"📍 {s['school.city']}, {s['school.state']}")
                    st.write("---")
        except Exception:
            st.error("API Connection Error. Please refresh and try again.")

    if st.button("Start Over"):
        st.session_state.step = 1
        st.rerun()
