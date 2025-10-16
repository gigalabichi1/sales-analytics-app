import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="📊 გაყიდვების ანალიტიკა",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა")
st.markdown("ანალიზი თვეების მიხედვით + 2026 წელი პროგნოზა")

with st.sidebar:
    uploaded_file = st.file_uploader(
        "📁 XLSX ფაილის ატვირთვა",
        type=["xlsx", "xls"]
    )

if uploaded_file is not None:
    try:
        # მონაცემი წაკითხვა
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = df.columns.str.strip()
        
        # რიცხვითი სვეტების კონვერტაცია
        for col in ['წონა კგ', 'თანხა', 'მოგება', 'მოგების პროცენტი']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        st.success(f"✅ წარმატებით ჩატვირთა!")
        st.info(f"📋 რიგი: {len(df)} | 📊 სვეტი: {len(df.columns)}")
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 დაშბორდი", "📅 თვეების ანალიზი", "🌍 ქვეყნების ანალიზი", "🔮 2026 პროგნოზა", "📋 მონაცემი"])
        
        # ============ TAB 1: დაშბორდი ============
        with tab1:
            st.markdown("## 📊 დაშბორდი - KPI მაჩვენებლები")
            
            # KPI Cards - პირველი რიგი
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📋 სულ რიგი", len(df))
            
            with col2:
                total_weight = df['წონა კგ'].sum()
                st.metric("📦 ჯამი წონა", f"{total_weight:,.0f} კგ")
            
            with col3:
                total_amount = df['თანხა'].sum()
                st.metric("💰 ჯამი თანხა", f"₾{total_amount:,.0f}")
            
            with col4:
                total_profit = df['მოგება'].sum()
                st.metric("📈 ჯამი მოგება", f"₾{total_profit:,.0f}")
            
            # KPI Cards - მეორე რიგი
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_profit_pct = df['მოგების პროცენტი'].mean()
                st.metric("📊 საშუო მოგება %", f"{avg_profit_pct:.2f}%")
            
            with col2:
                unique_countries = df['Номенклатура.ქვეყანა'].nunique()
                st.metric("🌍 ქვეყნების რაოდ.", unique_countries)
            
            with col3:
                unique_months = df['თვე'].nunique()
                st.metric("📅 თვეების რაოდ.", unique_months)
            
            with col4:
                avg_weight = df['წონა კგ'].mean()
                st.metric("📦 საშუო წონა", f"{avg_weight:,.0f} კგ")
            
            st.markdown("---")
            st.markdown("### 📋 მთელი მონაცემთა ცხრილი")
            st.dataframe(df, use_container_width=True, height=400)
        
        # ============ TAB 2: თვეების ანალიზი ============
        with tab2:
            st.markdown("## 📅 თვეების მიხედვით დეტალური ანალიზი")
            
            # თვეების ანალიზი
            month_analysis = df.groupby('თვე').agg({
                'წონა კგ': 'sum',
                'თანხა': 'sum',
                'მოგება': 'sum',
                'მოგების პროცენტი': 'mean'
            }).round(2)
            
            month_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
            
            st.markdown("### 📊 თვეების სტატისტიკა")
            st.dataframe(month_analysis, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📈 თვეების ხელმოკიდებული ანალიზი")
            
            # თვე + ქვეყნა
            month_country_analysis = df.pivot_table(
                values='მოგება',
                index='თვე',
                columns='Номенклатура.ქვეყანა',
                aggfunc='sum'
            ).round(0).fillna(0)
            
            st.markdown(f"#### მოგება - თვე × ქვეყნა")
            st.dataframe(month_country_analysis, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🔝 საუკეთესო თვე")
            
            best_month = month_analysis['მოგება ₾'].idxmax()
            best_month_profit = month_analysis['მოგება ₾'].max()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📅 თვე", best_month)
            col2.metric("💰 მოგება", f"₾{best_month_profit:,.0f}")
            col3.metric("📊 საშუო %", f"{month_analysis.loc[best_month, 'მოგება %']:.2f}%")
        
        # ============ TAB 3: ქვეყნების ანალიზი ============
        with tab3:
            st.markdown("## 🌍 ქვეყნების მიხედვით დეტალური ანალიზი")
            
            # ქვეყნების ანალიზი
            country_analysis = df.groupby('Номенклатура.ქვეყანა').agg({
                'წონა კგ': 'sum',
                'თანხა': 'sum',
                'მოგება': 'sum',
                'მოგების პროცენტი': 'mean'
            }).round(2)
            
            country_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
            country_analysis = country_analysis.sort_values('მოგება ₾', ascending=False)
            
            st.markdown("### 📊 ქვეყნების სტატისტიკა")
            st.dataframe(country_analysis, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🏆 Top 5 ქვეყნები (მოგება)")
            
            top5 = country_analysis['მოგება ₾'].head(5)
            for i, (country, profit) in enumerate(top5.items(), 1):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if i == 1:
                        st.markdown(f"### 🥇 {i}")
                    elif i == 2:
                        st.markdown(f"### 🥈 {i}")
                    elif i == 3:
                        st.markdown(f"### 🥉 {i}")
                    else:
                        st.markdown(f"### {i}")
                with col2:
                    st.metric(country, f"₾{profit:,.0f}")
        
        # ============ TAB 4: 2026 პროგნოზა ============
        with tab4:
            st.markdown("## 🔮 2026 წელი - პროგნოზა ქვეყნების მიხედვით")
            
            col1, col2 = st.columns(2)
            
            with col1:
                metric_type = st.selectbox(
                    "აირჩიეთ მეტრიკა:",
                    ["მოგება", "თანხა", "წონა კგ"]
                )
            
            with col2:
                growth_rate = st.slider(
                    "ზრდის ტემპი (%) - 2026:",
                    min_value=-100,
                    max_value=300,
                    value=15,
                    step=5
                )
            
            st.markdown("---")
            st.markdown(f"### 📊 2026 წლის პროგნოზა - {metric_type}")
            
            # საერთო პროგნოზა
            if metric_type == "მოგება":
                current_total = df['მოგება'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
            elif metric_type == "თანხა":
                current_total = df['თანხა'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
            else:
                current_total = df['წონა კგ'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("2025 წელი (ამჟამი)", f"{current_total:,.0f}")
            col2.metric("2026 წელი (პროგნოზა)", f"{forecast_total:,.0f}", f"{diff_total:+,.0f}")
            col3.metric("ზრდის ტემპი", f"{growth_rate}%")
            col4.metric("საშუო თვე", f"{forecast_total/12:,.0f}")
            
            st.markdown("---")
            st.markdown(f"### 🌍 2026 პროგნოზა - ქვეყნების მიხედვით ({metric_type})")
            
            # ქვეყნების პროგნოზა
            if metric_type == "მოგება":
                country_current = df.groupby('Номенклатура.ქვეყანა')['მოგება'].sum()
            elif metric_type == "თანხა":
                country_current = df.groupby('Номенклатура.ქვეყანა')['თანხა'].sum()
            else:
                country_current = df.groupby('Номенклатура.ქვეყანა')['წონა კგ'].sum()
            
            country_forecast = (country_current * (1 + growth_rate / 100)).round(0)
            
            forecast_df = pd.DataFrame({
                '2025 (ამჟამი)': country_current.round(0),
                '2026 (პროგნოზა)': country_forecast,
                'განსხვავება': (country_forecast - country_current.round(0)),
                'ზრდა %': (((country_forecast - country_current.round(0)) / country_current * 100)).round(1)
            }).sort_values('2026 (პროგნოზა)', ascending=False)
            
            st.dataframe(forecast_df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📈 თვეების მიხედვით 2026 პროგნოზა")
            
            # თვეების პროგნოზა
            if metric_type == "მოგება":
                month_current = df.groupby('თვე')['მოგება'].sum()
            elif metric_type == "თანხა":
                month_current = df.groupby('თვე')['თანხა'].sum()
            else:
                month_current = df.groupby('თვე')['წონა კგ'].sum()
            
            month_forecast = (month_current * (1 + growth_rate / 100)).round(0)
            
            month_forecast_df = pd.DataFrame({
                '2025 (ამჟამი)': month_current.round(0),
                '2026 (პროგნოზა)': month_forecast,
                'განსხვავება': (month_forecast - month_current.round(0))
            }).sort_index()
            
            st.dataframe(month_forecast_df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📊 ქვეყნა × თვე (2026 პროგნოზა)")
            
            # Pivot პროგნოზა
            if metric_type == "მოგება":
                pivot_current = df.pivot_table(values='მოგება', index='Номенклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            elif metric_type == "თანხა":
                pivot_current = df.pivot_table(values='თანხა', index='Номенклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            else:
                pivot_current = df.pivot_table(values='წონა კგ', index='Номენклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            
            pivot_forecast = (pivot_current * (1 + growth_rate / 100)).round(0)
            
            st.dataframe(pivot_forecast, use_container_width=True)
        
        # ============ TAB 5: მონაცემი ============
        with tab5:
            st.markdown("## 📋 სრული მონაცემთა ცხრილი")
            
            # სვეტების არჩევა
            all_cols = st.multiselect(
                "აირჩიეთ სვეტები:",
                df.columns.tolist(),
                default=df.columns.tolist()
            )
            
            if all_cols:
                st.dataframe(df[all_cols], use_container_width=True, height=500)
                
                # CSV Download
                csv = df[all_cols].to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 CSV-ის ჩამოტვირთვა",
                    data=csv,
                    file_name="sales_data.csv",
                    mime="text/csv"
                )
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")
        st.info(f"💡 დიაგნოსტიკა: {type(e).__name__}")

else:
    st.markdown("## 📁 XLSX ფაილი ატვირთეთ დასაწყებად")
    st.markdown("""
    ### 📊 სავალდებული სვეტები:
    
    1. **Номенклатура.ქვეყანა** - ქვეყნის სახელი
    2. **თვე** - თვის სახელი
    3. **წონა კგ** - წონა კილოგრამებში
    4. **თანხა** - ფულის რაოდენობა
    5. **მოგება** - მოგების ოდენობა
    6. **მოგების პროცენტი** - მოგების პროცენტი
    
    ### 📈 აპლიკაციის ფუნქციონალი:
    - **დაშბორდი** - KPI მაჩვენებლები
    - **თვეების ანალიზი** - თვე, საუკეთესო თვე
    - **ქვეყნების ანალიზი** - Top 5 ქვეყნები
    - **2026 პროგნოზა** - ქვეყნა × თვე, ზრდის გეგმა
    - **მონაცემი** - ფილტრი + CSV ჩამოტვირთვა
    """)

st.markdown("---")
st.markdown("© 2025 გაყიდვების ანალიტიკა | **gigalabichi1**")
