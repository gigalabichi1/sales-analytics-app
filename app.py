import streamlit as st
import pandas as pd

# Title of the application
st.title('გაყიდვების ანალიტიკა')

# Upload data
uploaded_file = st.file_uploader('აირჩიეთ მონაცემთა ფაილი', type=['csv'])
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success('მონაცემები წარმატებით ჩაიტვირთა!')
    except Exception as e:
        st.error(f'მონაცემების ჩატვირთვის დროს მოხდა შეცდომა: {e}')

# Ensure data is loaded
if 'data' in locals():
    # Dashboard tab
    st.header('დაშბორდი')
    st.subheader('გაყიდვების მიმოხილვა')
    st.write(data.describe())

    # Analysis tab
    st.header('ანალიზი')
    selected_product = st.selectbox('აირჩიეთ პროდუქტი', data['Product'].unique())
    product_data = data[data['Product'] == selected_product]
    st.line_chart(product_data['Sales'])

    # Forecast tab
    st.header('მიმდინარე პროგნოზი')
    st.write('აქ უნდა იყოს პროგნოზირების მოდელი')

else:
    st.warning('გთხოვთ, განათავსოთ მონაცემთა ფაილი პირველ რიგში.')

# Error handling and data validation
if data.isnull().values.any():
    st.error('მონაცემებში არის დაკარგული მნიშვნელობები! გთხოვთ, შეამოწმოთ.')
