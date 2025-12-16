import streamlit as st
import pandas as pd

# Title
st.title("Shipping Cost Calculator")

# Input Section
st.header("Input Package Details")
num_packages = st.number_input("Enter the number of packages", min_value=1, value=1)
box_type = st.selectbox("Select Box Type", ["Small Box", "Medium Box", "Large Box"])
currency = st.selectbox("Select Currency", ["USD", "PKR"])

# Cost mapping
cost_mapping = {
    "Small Box": {"USD": 5.0, "PKR": 500},
    "Medium Box": {"USD": 10.0, "PKR": 1000},
    "Large Box": {"USD": 20.0, "PKR": 5000},
}

# Calculate cost
cost = num_packages * cost_mapping[box_type][currency]

# Display result
st.subheader("Total Shipping Cost")
st.write(f"{num_packages} x {box_type} = {cost} {currency}")

# Optionally: reset
if st.button("Reset Inputs"):
    st.experimental_rerun()
