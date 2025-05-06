import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 
import plotly.express as px

st.set_page_config(page_title="Ski Resorts in the Pacific States", layout="wide")
st.title('Ski Resorts in the Pacific States')

st.write("This is a site to get more information about the top 50 rated ski resorts in the pacific states of the US. Data is from https://www.skiresort.info/ski-resorts/pacific-states-west-coast/" )
data = pd.read_csv('Ski_Resort_Data2.csv') 
search = st.text_input("Resort Search:")
if search: 
    try:
        filtered_data = data[data['Resort name'].str.contains(search, case=False, na=False)]
        st.write(filtered_data)
    except Exception as e:
        st.error(f"Not a valid resort: {e}")
else:
    st.write(data)
##slider for price
min_price = int(data['Ticket Price'].min())
max_price = int(data['Ticket Price'].max())
price_range = st.slider("Filter by Ticket Price ($)", min_value=min_price, max_value=max_price, value=(min_price, max_price))
data = data[(data['Ticket Price'] >= price_range[0]) & (data['Ticket Price'] <= price_range[1])]

st.dataframe(data, hide_index=True)

##graph
data = data.dropna(subset=['Resort name', 'Ski lifts', 'Ticket Price'])
data['Resort name'] = data['Resort name'].astype(str)

if data.empty:
    st.warning("No data to display.")
else:
    fig = plt.figure(figsize=(8, 3))
    plt.bar(data['Resort name'], data['Ski lifts'], color='skyblue')
    plt.xlabel('Resort Name')
    plt.ylabel('Number of ski lifts')
    plt.title('Number of ski lifts in each resort')
    plt.xticks(rotation=90)
    st.pyplot(fig)

    fig2 = plt.figure(figsize=(8, 3))
    plt.hist(data['Ticket Price'], bins=10, color='skyblue', edgecolor='black')
    plt.xlabel('Ticket Price ($)')
    plt.ylabel('Number of Resorts')
    plt.title('Distribution of Ticket Prices')
    st.pyplot(fig2)

st.subheader("Ticket Price vs Rating")

# Make sure data has the needed columns and no missing values
scatter_data = data.dropna(subset=['Resort name', 'Ticket Price', 'Test Rating', 'Ski lifts'])

if scatter_data.empty:
    st.warning("Not enough data to show the comparison.")
else:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(scatter_data['Ticket Price'], scatter_data['Test Rating'], color='pink', edgecolor='red')

    # Add labels for each point
    for i, row in scatter_data.iterrows():
        ax.annotate(row['Resort name'], (row['Ticket Price'], row['Test Rating']),
                    textcoords="offset points", xytext=(0, 5), ha='center', fontsize=4)

    ax.set_xlabel('Ticket Price ($)')
    ax.set_ylabel('Test Rating')
    ax.set_title('Comparison of Ticket Price and Rating by Resort')

    st.pyplot(fig)

fig = px.scatter(
    scatter_data,
    x='Ticket Price',
    y='Test Rating',
    color='Ski lifts',
    size='Ski lifts',
    hover_name='Resort name',       
    hover_data={
        'Ticket Price': True,
        'Test Rating': True,
        'Ski lifts': True
    },
    color_continuous_scale='viridis',
    title='Ticket Price vs Rating (Bubble Size = Lifts)',
    labels={
        'Ticket Price': 'Ticket Price ($)',
        'Test Rating': 'Rating',
        'Ski lifts': 'Number of Lifts'
    },
    height=600
)

st.plotly_chart(fig, use_container_width=True)
