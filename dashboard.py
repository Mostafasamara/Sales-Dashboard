import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title and settings
st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")


# Load the dataset
df = pd.read_csv('supermarkt_sales.csv')

# Convert 'Date' to a datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar Filters
st.sidebar.header("Filters")
selected_city = st.sidebar.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique())
selected_customer_type = st.sidebar.multiselect("Select Customer Type", options=df['Customer_type'].unique(), default=df['Customer_type'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Apply filters to the data
filtered_df = df[(df['City'].isin(selected_city)) &
                 (df['Customer_type'].isin(selected_customer_type)) &
                 (df['Gender'].isin(selected_gender))]

# Header
st.title("Sales Dashboard")
st.markdown("Interactive dashboard to visualize sales data.")

# KPIs
total_sales = filtered_df['Total'].sum()
average_order_value = filtered_df['Total'].mean()
num_transactions = len(filtered_df)
total_quantity = filtered_df['Quantity'].sum()

# Display KPIs
st.markdown("### Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Order Value", f"${average_order_value:,.2f}")
col3.metric("Number of Transactions", num_transactions)
col4.metric("Total Quantity Sold", total_quantity)

# Line Chart: Sales over Time
st.markdown("### Sales Trend Over Time")
timeframe_option = st.radio("View by:", ["Daily", "Monthly"], horizontal=True)

if timeframe_option == "Daily":
    sales_per_day = filtered_df.groupby(filtered_df['Date'].dt.date)['Total'].sum().reset_index()
    fig_line = px.line(sales_per_day, x='Date', y='Total', title='Daily Sales Trend', labels={'Date': 'Date', 'Total': 'Sales'})
else:
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
    sales_per_month = filtered_df.groupby('Month')['Total'].sum().reset_index()
    sales_per_month['Month'] = sales_per_month['Month'].astype(str)
    fig_line = px.line(sales_per_month, x='Month', y='Total', title='Monthly Sales Trend', labels={'Month': 'Month', 'Total': 'Sales'})

st.plotly_chart(fig_line)

# Bar Chart: Sales by Product Line
st.markdown("### Sales by Product Line")
sales_by_product_line = filtered_df.groupby('Product line')['Total'].sum().reset_index()
fig_bar = px.bar(sales_by_product_line, x='Product line', y='Total', color='Product line',
                 title='Sales by Product Line', labels={'Total': 'Sales'}, text='Total')
st.plotly_chart(fig_bar)

# Histogram: Distribution of Total Sales
st.markdown("### Distribution of Sales Amounts")
fig_hist = px.histogram(filtered_df, x='Total', nbins=20, title='Sales Distribution', labels={'Total': 'Sales Amount'})
st.plotly_chart(fig_hist)

# Pie Chart: Payment Method Distribution
st.markdown("### Sales by Payment Method")
sales_by_payment = filtered_df.groupby('Payment')['Total'].sum().reset_index()
fig_pie = px.pie(sales_by_payment, names='Payment', values='Total', title='Sales Distribution by Payment Method')
st.plotly_chart(fig_pie)

# Bar Chart: Sales by City
st.markdown("### Sales by City")
sales_by_city = filtered_df.groupby('City')['Total'].sum().reset_index()
fig_city = px.bar(sales_by_city, x='City', y='Total', color='City', title='Sales by City', labels={'Total': 'Sales'})
st.plotly_chart(fig_city)

#Dark mode Theam
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)
