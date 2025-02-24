import streamlit as st
import pandas as pd
import numpy as np

def calculate_pricing(team_size, burden_rate, gpm):
    hours_per_week = team_size * 37.5
    hours_per_month = hours_per_week * 4
    total_monthly_cost = hours_per_month * burden_rate
    required_revenue = total_monthly_cost / (1 - gpm)
    charge_rate_per_hour = required_revenue / hours_per_month
    return total_monthly_cost, required_revenue, charge_rate_per_hour

# Streamlit UI
st.title("IT Support Coverage Model Calculator")

# User Inputs
team_size = st.slider("Number of Team Members", 9, 12, 11)
burden_rate = st.number_input("Burden Cost Rate per Hour ($)", min_value=50, max_value=200, value=100)
gpm = st.slider("Target Gross Profit Margin (%)", 20, 60, 45) / 100

# Calculate results
total_monthly_cost, required_revenue, charge_rate_per_hour = calculate_pricing(team_size, burden_rate, gpm)

# Display results
st.subheader("Results")
st.write(f"**Total Monthly Cost:** ${total_monthly_cost:,.2f}")
st.write(f"**Required Monthly Revenue:** ${required_revenue:,.2f}")
st.write(f"**Charge Rate per Hour:** ${charge_rate_per_hour:,.2f}")

# Shift Coverage Table
st.subheader("Updated Shift Coverage (Anchored in Eastern Time)")
shift_data = {
    "Shift (ET)": ["12:30 AM - 4:30 AM", "2 AM - 6 AM", "5 AM - 9 AM", "8 AM - 12 PM", "10 AM - 2 PM", "2 PM - 11:30 PM"],
    "Resources Needed": [3, 2, 2, 3, 2, 1],
    "Assigned Locations": ["India + Mauritius", "Mauritius + India", "Mauritius + Canada", "Canada (Eastern & Central)", "Canada (Eastern, Central)", "Mauritius"]
}
shift_df = pd.DataFrame(shift_data)
st.dataframe(shift_df)
