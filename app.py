import streamlit as st
from utils import get_matches_next_hours, analyze_match
from config import API_KEY

st.set_page_config(page_title="Bet Insights", layout="centered")

st.title("⚽ Επόμενοι Αγώνες & Ανάλυση")

matches = get_matches_next_hours(API_KEY, hours=12)

if matches:
    st.subheader("Επόμενοι αγώνες (επόμενες 12 ώρες):")
    for match in matches:
        with st.expander(f"{match['teams']['home']} vs {match['teams']['away']} - {match['time']}"):
            st.write(f"Ημερομηνία: {match['date']}")
            st.write(f"Διοργάνωση: {match['league']}")
            if st.button(f"🔍 Ανάλυση για: {match['teams']['home']} vs {match['teams']['away']}", key=match['id']):
                with st.spinner("Γίνεται ανάλυση..."):
                    prediction = analyze_match(API_KEY, match['id'])
                    st.success("✅ Πιθανότερο στοίχημα:")
                    st.markdown(f"### 💡 {prediction}")
else:
    st.warning("Δεν βρέθηκαν αγώνες για τις επόμενες 12 ώρες.")
