import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("customer_churn.csv")
df['SignupDate'] = pd.to_datetime(df['SignupDate'])
total_customers = df['CustomerID'].nunique()
churned_customers = (df['Churn'] == 1).sum()
active_customers = (df['Churn'] == 0).sum()
churn_rate = df['Churn'].mean() * 100
st.title("📊 Customer Churn Dashboard")
st.write("Track KPIs and trends for customer retention and churn.")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned_customers)
col3.metric("Active Customers", active_customers)
col4.metric("Churn Rate (%)", f"{churn_rate:.2f}%")
# Monthly churn rate
monthly_churn = (
    df.groupby(df['SignupDate'].dt.to_period("M"))['Churn']
      .mean()
      .reset_index()
)
monthly_churn['SignupDate'] = monthly_churn['SignupDate'].astype(str)

fig1 = px.line(
    monthly_churn,
    x='SignupDate',
    y='Churn',
    title="Monthly Churn Rate",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)
# Churn rate by plan type
plan_churn = df.groupby('PlanType')['Churn'].mean().reset_index()
plan_churn['Churn'] = plan_churn['Churn']*100

fig2 = px.bar(
    plan_churn,
    x='PlanType',
    y='Churn',
    title="Churn Rate by Plan Type",
    text='Churn'
)

st.plotly_chart(fig2, use_container_width=True)

region_churn = df.groupby('Region')['Churn'].mean().reset_index()
region_churn['Churn'] = region_churn['Churn']*100

fig3 = px.bar(
    region_churn,
    x='Region',
    y='Churn',
    title="Churn Rate by Region",
    text='Churn'
)

st.plotly_chart(fig3, use_container_width=True)

monthly_summary = df.groupby(df['SignupDate'].dt.to_period("M")).agg(
    new_customers=('CustomerID', 'count'),
    churned=('Churn', 'sum')
).reset_index()

monthly_summary['SignupDate'] = monthly_summary['SignupDate'].astype(str)

fig4 = px.bar(
    monthly_summary,
    x='SignupDate',
    y=['new_customers', 'churned'],
    title="New vs Churned Customers per Month"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("📌 Key Insights")
st.write("""
- Churn is highest in [PlanType with max churn]  
- Churn rate is trending up/down in recent months  
- Active customers are concentrated in [PlanType / Region]  
""")
