import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Customer-Churn-Records.csv")

total_customers = df['CustomerId'].nunique()
churned_customers = (df['Exited'] == 1).sum()
active_customers = (df['Exited'] == 0).sum()
churn_rate = df['Exited'].mean() * 100
st.title("📊 Customer Churn Dashboard")
st.write("Track KPIs and trends for customer retention and churn.")

df['TenureGroup'] = pd.cut(df['Tenure'], bins=[0,2,5,10], labels=['0-2','3-5','6-10'])

# -------Chart by Plan----------#
plan_churn = df.groupby('Card Type')['Exited'].mean().reset_index()
plan_churn['Exited'] = plan_churn['Exited']*100  # convert to percent

fig_plan = px.bar(
    plan_churn,
    x='Card Type',
    y='Exited',
    title="Churn Rate by Card Type",
    text='Exited'
)
st.plotly_chart(fig_plan, use_container_width=True)

# 2️⃣ Churn rate by Geography
geo_churn = df.groupby('Geography')['Exited'].mean().reset_index()
geo_churn['Exited'] = geo_churn['Exited']*100  # percent

fig_geo = px.bar(
    geo_churn,
    x='Geography',
    y='Exited',
    title="Churn Rate by Geography",
    text='Exited'
)
st.plotly_chart(fig_geo, use_container_width=True)

# 3️⃣ Churn rate by Tenure Group (trend substitute for monthly trend)
tenure_churn = df.groupby('TenureGroup')['Exited'].mean().reset_index()
tenure_churn['Exited'] = tenure_churn['Exited']*100

fig_tenure = px.line(
    tenure_churn,
    x='TenureGroup',
    y='Exited',
    title="Churn Rate by Tenure Group",
    markers=True
)
st.plotly_chart(fig_tenure, use_container_width=True)

# 4️⃣ New vs Churned customers per Tenure Group (stacked bar)
tenure_summary = df.groupby('TenureGroup').agg(
    total_customers=('CustomerId', 'count'),
    churned=('Exited', 'sum')
).reset_index()

tenure_summary['active'] = tenure_summary['total_customers'] - tenure_summary['churned']

fig_tenure_bar = px.bar(
    tenure_summary,
    x='TenureGroup',
    y=['active','churned'],
    title="Active vs Churned Customers by Tenure Group"
)
st.plotly_chart(fig_tenure_bar, use_container_width=True)

st.subheader("📌 Key Insights")
st.write("""
- Churn is highest in [PlanType with max churn]  
- Churn rate is trending up/down in recent months  
- Active customers are concentrated in [PlanType / Region]  
""")
