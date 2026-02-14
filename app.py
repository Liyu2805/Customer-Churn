import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("Customer-Churn-Records.csv")  
    return df

df = load_data()

st.title("Customer Churn Dashboard")
st.markdown("""
This dashboard provides insights into customer churn trends, satisfaction, and behavior.
""")

total_customers = df['CustomerId'].nunique()
churned_customers = df['Exited'].sum()
active_customers = total_customers - churned_customers
avg_balance = df['Balance'].mean()
avg_age = df['Age'].mean()
avg_salary = df['EstimatedSalary'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned_customers)
col3.metric("Active Customers", active_customers)

col4, col5 = st.columns(2)
col4.metric("Average Balance", f"${avg_balance:,.2f}")
col5.metric("Average Salary", f"${avg_salary:,.2f}")

st.sidebar.header("Filters")
selected_geo = st.sidebar.multiselect("Select Geography", df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[(df['Geography'].isin(selected_geo)) & (df['Gender'].isin(selected_gender))]

st.subheader("Churn by Geography")
churn_geo = filtered_df.groupby('Geography')['Exited'].mean().reset_index()
churn_geo['Exited'] = churn_geo['Exited']*100
fig1 = px.bar(churn_geo, x='Geography', y='Exited', text='Exited', labels={'Exited':'Churn Rate (%)'})
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Churn by Gender")
churn_gender = filtered_df.groupby('Gender')['Exited'].mean().reset_index()
churn_gender['Exited'] = churn_gender['Exited']*100
fig2 = px.pie(churn_gender, names='Gender', values='Exited', title='Churn Rate by Gender')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Customer Satisfaction Distribution")
fig3 = px.histogram(filtered_df, x='Satisfaction Score', nbins=10, color='Exited', barmode='overlay',
                    labels={'Satisfaction Score':'Satisfaction Score', 'Exited':'Churn'})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Number of Products vs Churn")
fig4 = px.box(filtered_df, x='NumOfProducts', y='Balance', color='Exited',
              labels={'NumOfProducts':'Number of Products', 'Balance':'Balance'})
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Points Earned vs Churn")
fig5 = px.scatter(filtered_df, x='Point Earned', y='Balance', color='Exited', size='EstimatedSalary',
                  labels={'Point Earned':'Points Earned', 'Balance':'Balance'})
st.plotly_chart(fig5, use_container_width=True)
