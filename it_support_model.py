import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_pricing(team_size, burden_rate, gpm):
    hours_per_week = team_size * 37.5
    hours_per_month = hours_per_week * 4
    total_monthly_cost = hours_per_month * burden_rate
    required_revenue = total_monthly_cost / (1 - gpm)
    charge_rate_per_hour = required_revenue / hours_per_month
    return total_monthly_cost, required_revenue, charge_rate_per_hour

def calculate_core_hours_coverage(shift_df, core_start, core_end):
    filtered_shifts = shift_df[(shift_df["Shift Start"] >= core_start) & (shift_df["Shift End"] <= core_end)]
    return filtered_shifts["Resources Needed"].sum()

# Streamlit UI
st.set_page_config(page_title="IT Support Auto-Updating Calculator", layout="wide")
st.title("IT Support Auto-Updating Calculator")

# Sidebar for user inputs
st.sidebar.header("Input Variables")
team_size = int(st.sidebar.text_input("Number of Team Members", value="11"))
burden_rate = float(st.sidebar.text_input("Burden Cost Rate per Hour ($)", value="100"))
gpm = float(st.sidebar.text_input("Target Gross Profit Margin (%)", value="45")) / 100

# Core Support Hours Interactive Input
st.sidebar.header("Core Support Hours")
core_start = st.sidebar.number_input("Core Support Start Hour (ET)", min_value=0, max_value=23, value=10, step=1)
core_end = st.sidebar.number_input("Core Support End Hour (ET)", min_value=0, max_value=23, value=14, step=1)

# Auto-update calculations
total_monthly_cost, required_revenue, charge_rate_per_hour = calculate_pricing(team_size, burden_rate, gpm)

# Display results
st.subheader("Results (Auto-Updated)")
st.write(f"**Total Monthly Cost:** ${total_monthly_cost:,.2f}")
st.write(f"**Required Monthly Revenue:** ${required_revenue:,.2f}")
st.write(f"**Charge Rate per Hour:** ${charge_rate_per_hour:,.2f}")

# Shift Coverage Table
st.subheader("Updated Shift Coverage (Anchored in Eastern Time)")
shift_data = {
    "Shift (ET)": ["12:30 AM - 4:30 AM", "2 AM - 6 AM", "5 AM - 9 AM", "8 AM - 12 PM", "10 AM - 2 PM", "2 PM - 11:30 PM"],
    "Shift Start": [0.5, 2, 5, 8, 10, 14],
    "Shift End": [4.5, 6, 9, 12, 14, 23.5],
    "Resources Needed": [3, 2, 2, 3, 2, 1],
    "Assigned Locations": ["India + Mauritius", "Mauritius + India", "Mauritius + Canada", "Canada (Eastern & Central)", "Canada (Eastern, Central)", "Mauritius"]
}
shift_df = pd.DataFrame(shift_data)
st.dataframe(shift_df)

# Calculate core hours coverage based on user input
total_core_hours_coverage = calculate_core_hours_coverage(shift_df, core_start, core_end)
st.write(f"**Total Resources Required During Core Support Hours ({core_start}:00 - {core_end}:00 ET):** {total_core_hours_coverage}")

# Visual Representation of Shift Coverage
st.subheader("Shift Coverage Visualization")
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(shift_df["Shift (ET)"], shift_df["Resources Needed"], color='skyblue')
ax.set_xlabel("Number of People Working")
ax.set_ylabel("Shift Time (ET)")
ax.set_title("Number of People Working at Any Given Time")
st.pyplot(fig)
