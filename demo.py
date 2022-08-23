import streamlit as st
from src.unit_api import UnitAPI

unit_api = UnitAPI()
st.title("Debugging Platform")
unit_code = st.text_input("Enter a unit code")

if st.button("Get Data"):
    
    st.json(unit_api.get_unit(unit_code)[-1])
