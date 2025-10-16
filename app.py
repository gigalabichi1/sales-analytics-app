import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="📊 გაყიდვების ანალიტიკა", page_icon="📊", layout="wide")

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა - XLSX")

with st.sidebar:
    uploaded_file = st.file_uploader("📁 XLSX ფაილის ატვირთვა", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # ფაილის წაკითხვა
        xls = pd.ExcelFile(uploaded_file)
        st.success(f"✅ Sheet-ები: {xls.sheet_names}")
        
        # Sheet-ის არჩევა
        selected_sheet = st.selectbox("📊 აირჩიეთ Sheet:", xls.sheet_names)
        
        # მონაცემის წაკითხვა
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        st.write(f"📋 რიგი: {len(df)}, 📊 სვეტი: {len(df.columns)}")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📈 დაშბორდი", "📊 ანალიზი", "🔮 პროგნოზა"])
        
        with tab1:
            st.markdown("## 📊 დაშბორდი")
            col1, col2, col3 = st.columns(3)
            col1.metric("📋 რიგი", len(df))
            col2.metric("📊 სვეტი", len(df.columns))
            col3.metric("✅ ივსება", f"{df.notna().sum().sum()}")
            st.dataframe(df, use_container_width=True)
        
        with tab2:
            st.markdown("## 📊 ანალიზი")
            cols = st.multiselect("აირჩიეთ სვეტები:", df.columns.tolist())
            if cols:
                st.dataframe(df[cols], use_container_width=True)
        
        with tab3:
            st.markdown("## 🔮 პროგნოზა")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                metric = st.selectbox("აირჩიეთ მეტრიკა:", numeric_cols)
                growth = st.slider("ზრდის ტემპი (%):", -100, 200, 10)
                current = df[metric].sum()
                forecast = current * (1 + growth/100)
                st.metric("ამჟამი", f"{current:,.0f}")
                st.metric("პროგნოზა", f"{forecast:,.0f}", f"{forecast-current:+,.0f}")
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")

else:
    st.markdown("## 📁 XLSX ფაილი ატვირთეთ დასაწყებად")
