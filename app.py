import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="📊 გაყიდვების ანალიტიკა",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა")
st.markdown("ჰორიზონტალური მონაცემი - Excel დაფა")

with st.sidebar:
    uploaded_file = st.file_uploader(
        "📁 XLSX ფაილის ატვირთვა",
        type=["xlsx", "xls"]
    )

if uploaded_file is not None:
    try:
        # მონაცემი წაკითხვა
        df = pd.read_excel(uploaded_file, sheet_name=0)
        
        # სვეტების სახელების გასწორება
        df.columns = df.columns.str.strip()
        
        st.success(f"✅ წარმატებით ჩატვირთა!")
        st.info(f"📋 რიგი: {len(df)} | 📊 სვეტი: {len(df.columns)}")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📈 დაშბორდი", "📊 ანალიზი", "🔮 პროგნოზა", "📋 მონაცემი"])
        
        # ============ TAB 1: დაშბორდი ============
        with tab1:
            st.markdown("## 📊 დაშბორდი - KPI მაჩვენებლები")
            
            # KPI Cards - პირველი რიგი
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📋 სულ რიგი", len(df))
            
            with col2:
                if 'წონა კგ' in df.columns:
                    total_weight = pd.to_numeric(df['წონა კგ'], errors='coerce').sum()
                    st.metric("📦 ჯამი წონა", f"{total_weight:,.0f} კგ")
                else:
                    st.metric("📦 წონა", "N/A")
            
            with col3:
                if 'თანხა' in df.columns:
                    total_amount = pd.to_numeric(df['თანხა'], errors='coerce').sum()
                    st.metric("💰 ჯამი თანხა", f"₾{total_amount:,.0f}")
                else:
                    st.metric("💰 თანხა", "N/A")
            
            with col4:
                if 'მოგება' in df.columns:
                    total_profit = pd.to_numeric(df['მოგება'], errors='coerce').sum()
                    st.metric("📈 ჯამი მოგება", f"₾{total_profit:,.0f}")
                else:
                    st.metric("📈 მოგება", "N/A")
            
            # KPI Cards - მეორე რიგი
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if 'მოგების პროცენტი' in df.columns:
                    avg_profit_pct = pd.to_numeric(df['მოგების პროცენტი'], errors='coerce').mean()
                    st.metric("📊 საშუო მოგება %", f"{avg_profit_pct:.2f}%")
                else:
                    st.metric("📊 მოგება %", "N/A")
            
            with col2:
                if 'Номенклатура.ქვეყანა' in df.columns:
                    unique_countries = df['Номенклатура.ქვეყანა'].nunique()
                    st.metric("🌍 ქვეყნების რაოდ.", unique_countries)
                else:
                    st.metric("🌍 ქვეყნები", "N/A")
            
            with col3:
                if 'თვე' in df.columns:
                    unique_months = df['თვე'].nunique()
                    st.metric("📅 თვეების რაოდ.", unique_months)
                else:
                    st.metric("📅 თვეები", "N/A")
            
            with col4:
                if 'წონა კგ' in df.columns:
                    avg_weight = pd.to_numeric(df['წონა კგ'], errors='coerce').mean()
                    st.metric("📦 საშუო წონა", f"{avg_weight:,.0f} კგ")
                else:
                    st.metric("📦 საშუო", "N/A")
            
            st.markdown("---")
            st.markdown("### 📋 მთელი მონაცემთა ცხრილი (ჰორიზონტალური)")
            st.dataframe(df, use_container_width=True, height=400)
        
        # ============ TAB 2: ანალიზი ============
        with tab2:
            st.markdown("## 📊 დეტალური ანალიზი")
            
            # ქვეყნების ანალიზი
            if 'Номенклатура.ქვეყანა' in df.columns:
                st.markdown("### 🌍 ქვეყნების მიხედვით ანალიზი")
                
                country_analysis = df.groupby('Номенклатура.ქვეყანა').agg({
                    'წონა კგ': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'თანხა': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'მოგება': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'მოგების პროცენტი': lambda x: pd.to_numeric(x, errors='coerce').mean()
                }).round(2)
                
                country_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
                country_analysis = country_analysis.sort_values('მოგება ₾', ascending=False)
                st.dataframe(country_analysis, use_container_width=True)
            
            # თვის მიხედვით ანალიზი
            if 'თვე' in df.columns:
                st.markdown("### 📅 თვის მიხედვით ანალიზი")
                
                month_analysis = df.groupby('თვე').agg({
                    'წონა კგ': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'თანხა': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'მოგება': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'მოგების პროცენტი': lambda x: pd.to_numeric(x, errors='coerce').mean()
                }).round(2)
                
                month_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
                st.dataframe(month_analysis, use_container_width=True)
            
            # Pivot ცხრილი: ქვეყნა × თვე
            if 'Номенклатура.ქვეყანა' in df.columns and 'თვე' in df.columns:
                st.markdown("### 🌍📅 ქვეყნა × თვე (მოგება)")
                
                pivot_table = df.pivot_table(
                    values='მოგება',
                    index='Номенклатура.ქვეყანა',
                    columns='თვე',
                    aggfunc=lambda x: pd.to_numeric(x, errors='coerce').sum()
                ).round(0)
                
                st.dataframe(pivot_table, use_container_width=True)
            
            # Top 5 ქვეყნები
            if 'Номенклатура.ქვეყანა' in df.columns and 'მოგება' in df.columns:
                st.markdown("### 🏆 Top 5 ქვეყნები (მოგება)")
                
                top_countries = df.groupby('Номенклатура.ქვეყანა')['მოგება'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce').sum()
                ).sort_values(ascending=False).head(5)
                
                for i, (country, profit) in enumerate(top_countries.items(), 1):
                    st.write(f"{i}. **{country}**: ₾{profit:,.0f}")
        
        # ============ TAB 3: პროგნოზა ============
        with tab3:
            st.markdown("## 🔮 პროგნოზა და წინასწარი")
            
            col1, col2 = st.columns(2)
            
            with col1:
                metric_type = st.selectbox(
                    "აირჩიეთ მეტრიკა:",
                    ["თანხა", "მოგება", "წონა კგ"]
                )
            
            with col2:
                growth_rate = st.slider(
                    "ზრდის ტემპი (%):",
                    min_value=-100,
                    max_value=300,
                    value=10,
                    step=5
                )
            
            st.markdown("---")
            st.markdown(f"### {metric_type} - წინასწარი პროგნოზა")
            
            if metric_type == "თანხა" and 'თანხა' in df.columns:
                current = pd.to_numeric(df['თანხა'], errors='coerce').sum()
                forecast = current * (1 + growth_rate / 100)
                diff = forecast - current
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("ამჟამი ჯამი", f"₾{current:,.0f}")
                col2.metric("წინასწარი ჯამი", f"₾{forecast:,.0f}", f"₾{diff:+,.0f}")
                col3.metric("ზრდის ტემპი", f"{growth_rate}%")
                col4.metric("განსხვავება %", f"{(diff/current*100):+.1f}%" if current != 0 else "N/A")
            
            elif metric_type == "მოგება" and 'მოგება' in df.columns:
                current = pd.to_numeric(df['მოგება'], errors='coerce').sum()
                forecast = current * (1 + growth_rate / 100)
                diff = forecast - current
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("ამჟამი ჯამი", f"₾{current:,.0f}")
                col2.metric("წინასწარი ჯამი", f"₾{forecast:,.0f}", f"₾{diff:+,.0f}")
                col3.metric("ზრდის ტემპი", f"{growth_rate}%")
                col4.metric("განსხვავება %", f"{(diff/current*100):+.1f}%" if current != 0 else "N/A")
            
            elif metric_type == "წონა კგ" and 'წონა კგ' in df.columns:
                current = pd.to_numeric(df['წონა კგ'], errors='coerce').sum()
                forecast = current * (1 + growth_rate / 100)
                diff = forecast - current
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("ამჟამი ჯამი", f"{current:,.0f} კგ")
                col2.metric("წინასწარი ჯამი", f"{forecast:,.0f} კგ", f"{diff:+,.0f} კგ")
                col3.metric("ზრდის ტემპი", f"{growth_rate}%")
                col4.metric("განსხვავება %", f"{(diff/current*100):+.1f}%" if current != 0 else "N/A")
            
            st.markdown("---")
            st.markdown("### 📊 ქვეყნების მიხედვით წინასწარი")
            
            if 'Номенклатура.ქვეყანა' in df.columns and metric_type == "მოგება":
                country_forecast = df.groupby('Номенклатура.ქვეყანა')['მოგება'].apply(
                    lambda x: pd.to_numeric(x, errors='coerce').sum()
                )
                country_forecast_new = (country_forecast * (1 + growth_rate / 100)).round(0)
                
                forecast_df = pd.DataFrame({
                    'ამჟამი': country_forecast,
                    'წინასწარი': country_forecast_new,
                    'განსხვავება': country_forecast_new - country_forecast
                }).sort_values('წინასწარი', ascending=False)
                
                st.dataframe(forecast_df, use_container_width=True)
        
        # ============ TAB 4: მონაცემი ============
        with tab4:
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
                csv = df[all_cols].to_csv(index=False)
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
    ### 📊 სავალდებული სვეტები (ჰორიზონტალური):
    
    | სვეტი | სახელი | აღწერა |
    |------|--------|--------|
    | 1 | Номенклатура.ქვეყანა | ქვეყნის სახელი |
    | 2 | თვე | თვის სახელი |
    | 3 | წონა კგ | წონა კილოგრამებში |
    | 4 | თანხა | ფულის რაოდენობა |
    | 5 | მოგება | მოგების ოდენობა |
    | 6 | მოგების პროცენტი | მოგების პროცენტი |
    
    ### 📈 აპლიკაციის ფუნქციონალი:
    - **დაშბორდი** - KPI მაჩვენებლები
    - **ანალიზი** - ქვეყნა, თვე, Pivot ცხრილი
    - **პროგნოზა** - ზრდის წინასწარი
    - **მონაცემი** - ფილტრი და CSV ჩამოტვირთვა
    """)

st.markdown("---")
st.markdown("© 2025 გაყიდვების ანალიტიკა | **gigalabichi1**")
