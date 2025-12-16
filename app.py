import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

# --- Page Config ---
st.set_page_config(page_title="Advanced Shipping Calculator", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar ---
st.sidebar.title("Settings")
theme = st.sidebar.radio("Theme", ["Light Mode", "Dark Mode"])
currency_default = st.sidebar.selectbox("Default Currency", ["USD", "PKR"])
st.sidebar.markdown("---")
st.sidebar.header("Bulk Upload")
bulk_file = st.sidebar.file_uploader("Upload CSV for bulk calculations", type=["csv"])

# --- Theme Styling ---
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: white; }
        .stButton>button { color:white; background-color:#4CAF50; }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Cost Data ---
cost_mapping = {
    "Small Box": {"USD": 5.0, "PKR": 500},
    "Medium Box": {"USD": 10.0, "PKR": 1000},
    "Large Box": {"USD": 20.0, "PKR": 5000},
}

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Packages", "Box Type", "Currency", "Cost"])

# --- Input Section ---
st.title("🚚 Advanced Shipping Cost Calculator")

col1, col2, col3 = st.columns(3)
with col1:
    num_packages = st.number_input("Number of packages", min_value=1, value=1)
with col2:
    box_type = st.selectbox("Select Box Type", list(cost_mapping.keys()))
with col3:
    currency = st.selectbox("Currency", ["USD", "PKR"], index=["USD", "PKR"].index(currency_default))

# --- Currency Conversion ---
exchange_rate = 280  # Example: 1 USD = 280 PKR
if currency == "PKR":
    cost = num_packages * cost_mapping[box_type]["PKR"]
else:
    cost = num_packages * cost_mapping[box_type]["USD"]

# --- Display Result ---
st.subheader("💰 Total Shipping Cost")
st.metric(label=f"{num_packages} x {box_type}", value=f"{cost} {currency}")

# --- Save to History ---
if st.button("Add to History"):
    new_row = {"Packages": num_packages, "Box Type": box_type, "Currency": currency, "Cost": cost}
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)
    st.success("✅ Added to history!")

# --- Reset Inputs ---
if st.button("Reset Inputs"):
    st.experimental_rerun()

# --- Bulk CSV Upload ---
if bulk_file:
    df_bulk = pd.read_csv(bulk_file)
    df_bulk['Cost'] = df_bulk.apply(lambda x: x['Packages'] * cost_mapping[x['Box Type']][x['Currency']], axis=1)
    st.subheader("📁 Bulk Calculation Results")
    st.dataframe(df_bulk)
    if st.button("Add Bulk to History"):
        st.session_state.history = pd.concat([st.session_state.history, df_bulk], ignore_index=True)
        st.success("✅ Bulk added to history!")

# --- History & Export ---
if not st.session_state.history.empty:
    st.header("📊 Calculation History")
    st.dataframe(st.session_state.history, use_container_width=True)

    # Export CSV
    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button("Export History as CSV", csv, "shipping_history.csv", "text/csv")

    # Export PDF
    if st.button("Export History as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Shipping Cost History", ln=True, align="C")
        for i, row in st.session_state.history.iterrows():
            pdf.cell(200, 10, txt=f"{row['Packages']}x {row['Box Type']} = {row['Cost']} {row['Currency']}", ln=True)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        st.download_button("Download PDF", pdf_output, "shipping_history.pdf", "application/pdf")

    # Charts
    st.subheader("📈 Cost Visualization")
    fig, ax = plt.subplots()
    st.session_state.history.groupby("Box Type")["Cost"].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# --- Copy to Clipboard ---
if not st.session_state.history.empty:
    st.subheader("📋 Copy Last Result")
    last_result = st.session_state.history.iloc[-1].to_dict()
    st.code(str(last_result))
