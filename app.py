import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="📊 გაყიდვების ანალიტიკა",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა - XLSX")

with st.sidebar:
    uploaded_file = st.file_uploader(
        "📁 XLSX ფაილის ატვირთვა",
        type=["xlsx", "xls"]
    )

if uploaded_file is not None:
    try:
        # ფაილის წაკითხვა
        xls = pd.ExcelFile(uploaded_file)
        
        st.success(f"✅ წარმატებით ჩატვირთა! Sheet-ები: {xls.sheet_names}")
        
        # Sheet არჩევა
        selected_sheet = st.selectbox("📊 აირჩიეთ Sheet:", xls.sheet_names)
        
        # მონაცემი
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📈 დაშბორდი", "📊 ანალიზი", "🔮 პროგნოზა"])
        
        # Tab 1: დაშბორდი
        with tab1:
            st.markdown("## 📊 დაშბორდი")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📋 რიგი", len(df))
            col2.metric("📊 სვეტი", len(df.columns))
            col3.metric("✅ მონაცემი", df.notna().sum().sum())
            
            st.markdown("---")
            st.dataframe(df, use_container_width=True, height=400)
        
        # Tab 2: ანალიზი
        with tab2:
            st.markdown("## 📊 ანალიზი")
            
            selected_cols = st.multiselect(
                "აირჩიეთ სვეტები:",
                df.columns.tolist()
            )
            
            if selected_cols:
                st.dataframe(df[selected_cols], use_container_width=True)
        
        # Tab 3: პროგნოზა
        with tab3:
            st.markdown("## 🔮 პროგნოზა")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                metric = st.selectbox("აირჩიეთ მეტრიკა:", numeric_cols)
                growth = st.slider("ზრდის ტემპი (%):", -100, 200, 10, step=5)
                
                current = df[metric].sum()
                forecast = current * (1 + growth / 100)
                diff = forecast - current
                
                col1, col2 = st.columns(2)
                col1.metric("ამჟამი", f"{current:,.0f}")
                col2.metric("პროგნოზა", f"{forecast:,.0f}", f"{diff:+,.0f}")
            else:
                st.warning("⚠️ რიცხვითი სვეტი არ მოიძებნა")
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")

else:
    st.markdown("## 📁 XLSX ფაილი ატვირთეთ დასაწყებად")
    st.info("✅ მხარდაჭერილი: .xlsx და .xls ფორმატი")
