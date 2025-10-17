import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 გაყიდვების ანალიტიკა", layout="wide")

st.title("📊 გაყიდვების ანალიტიკის სისტემა")

uploaded_file = st.file_uploader("📁 XLSX ფაილის ატვირთვა", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.success("✅ წარმატებით ჩატვირთა!")
    st.write(f"📋 რიგი: {len(df)} | 📊 სვეტი: {len(df.columns)}")
    
    tab1, tab2, tab3 = st.tabs(["📈 დაშბორდი", "📅 თვეები", "🔮 2026"])
    
    with tab1:
        st.subheader("📊 დაშბორდი")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 რიგი", len(df))
        col2.metric("📦 წონა", f"{pd.to_numeric(df['წონა კგ'], errors='coerce').sum():,.0f} კგ")
        col3.metric("💰 თანხა", f"₾{pd.to_numeric(df['თანხა'], errors='coerce').sum():,.0f}")
        col4.metric("📈 მოგება", f"₾{pd.to_numeric(df['მოგება'], errors='coerce').sum():,.0f}")
        
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("📅 თვეების ანალიზი")
        
        month_data = df.groupby('თვე').agg({
            'წონა კგ': lambda x: pd.to_numeric(x, errors='coerce').sum(),
            'თანხა': lambda x: pd.to_numeric(x, errors='coerce').sum(),
            'მოგება': lambda x: pd.to_numeric(x, errors='coerce').sum()
        }).round(0)
        
        st.dataframe(month_data, use_container_width=True)
        
        st.line_chart(month_data)
    
    with tab3:
        st.subheader("🔮 2026 პროგნოზა")
        
        growth = st.slider("ზრდის ტემპი (%):", -100, 300, 15)
        
        current_profit = pd.to_numeric(df['მოგება'], errors='coerce').sum()
        forecast_profit = current_profit * (1 + growth / 100)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("2025", f"₾{current_profit:,.0f}")
        col2.metric("2026", f"₾{forecast_profit:,.0f}", f"₾{forecast_profit - current_profit:+,.0f}")
        col3.metric("ზრდა", f"{growth}%")
        
        country_forecast = df.groupby('Номенклатура.ქვეყანა')['მოგება'].apply(
            lambda x: pd.to_numeric(x, errors='coerce').sum()
        )
        country_forecast_2026 = (country_forecast * (1 + growth / 100)).round(0)
        
        forecast_table = pd.DataFrame({
            '2025': country_forecast.round(0),
            '2026': country_forecast_2026,
            'ზრდა': country_forecast_2026 - country_forecast.round(0)
        }).sort_values('2026', ascending=False)
        
        st.dataframe(forecast_table, use_container_width=True)
        st.bar_chart(forecast_table['2025'])
        st.bar_chart(forecast_table['2026'])

else:
    st.info("📁 XLSX ფაილი ატვირთეთ დასაწყებად")
