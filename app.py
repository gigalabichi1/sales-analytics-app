import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="📊 გაყიდვების ანალიტიკა", page_icon="📊", layout="wide")

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა - XLSX")

with st.sidebar:
    uploaded_file = st.file_uploader("📁 XLSX ფაილის ატვირთვა", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        st.success("✅ XLSX ფაილი წარმატებით ჩატვირთა!")
        
        tab1, tab2, tab3 = st.tabs(["📈 დაშბორდი", "📊 ანალიზი", "🔮 პროგნოზა"])
        
        with tab1:
            st.markdown("## 📊 დაশბორდი")
            col1, col2, col3 = st.columns(3)
            col1.metric("📋 რიგი", len(df))
            col2.metric("📊 სვეტი", len(df.columns))
            col3.metric("✅ მონაცემი", df.notna().sum().sum())
            st.dataframe(df, use_container_width=True)
        
        with tab2:
            st.markdown("## 📊 ანალიზი")
            selected_cols = st.multiselect("აირჩიეთ სვეტები", df.columns.tolist())
            if selected_cols:
                st.dataframe(df[selected_cols], use_container_width=True)
        
        with tab3:
            st.markdown("## 🔮 პროგნოზა")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                metric = st.selectbox("აირჩიეთ მეტრიკა", numeric_cols)
                growth = st.slider("ზრდის ტემპი (%)", 0, 100, 10)
                forecast = df[metric].sum() * (1 + growth/100)
                st.metric("პროგნოზა", f"{forecast:,.0f}")
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")
else:
    st.markdown("## 📁 XLSX ფაილის ატვირთვა")
