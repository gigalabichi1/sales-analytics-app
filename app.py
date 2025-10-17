import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 გაყიდვების ანალიტიკა", layout="wide")

st.title("📊 გაყიდვების ანალიტიკის სისტემა")

uploaded_file = st.file_uploader("📁 XLSX ფაილის ატვირთვა", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        # სვეტების სახელების ნაჩვენებ
        st.write("### 📋 Excel ფაილის სვეტები:")
        st.write(df.columns.tolist())
        
        st.success("✅ წარმატებით ჩატვირთა!")
        st.write(f"📋 რიგი: {len(df)} | 📊 სვეტი: {len(df.columns)}")
        
        # სვეტების ავტომატური დანიშვა
        columns = df.columns.tolist()
        
        # სვეტების შერჩევა
        st.markdown("---")
        st.markdown("### ⚙️ სვეტების კონფიგურაცია")
        
        col1, col2 = st.columns(2)
        
        with col1:
            country_col = st.selectbox("🌍 ქვეყნის სვეტი:", columns, index=0)
            month_col = st.selectbox("📅 თვის სვეტი:", columns, index=1 if len(columns) > 1 else 0)
        
        with col2:
            weight_col = st.selectbox("📦 წონის სვეტი:", columns, index=2 if len(columns) > 2 else 0)
            amount_col = st.selectbox("💰 თანხის სვეტი:", columns, index=3 if len(columns) > 3 else 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            profit_col = st.selectbox("📈 მოგების სვეტი:", columns, index=4 if len(columns) > 4 else 0)
        
        with col2:
            profit_pct_col = st.selectbox("📊 მოგების % სვეტი:", columns, index=5 if len(columns) > 5 else 0)
        
        st.markdown("---")
        
        # რიცხვითი სვეტების კონვერტაცია
        for col in [weight_col, amount_col, profit_col, profit_pct_col]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 დაშბორდი", "📅 თვეები", "🌍 ქვეყნები", "🔮 2026 გეგმა", "📊 გენერირებული"])
        
        # ============ TAB 1: დაშბორდი ============
        with tab1:
            st.subheader("📊 დაშბორდი - 2025 წელი")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📋 რიგი", len(df))
            col2.metric("📦 ჯამი წონა", f"{df[weight_col].sum():,.0f} კგ")
            col3.metric("💰 ჯამი თანხა", f"₾{df[amount_col].sum():,.0f}")
            col4.metric("📈 ჯამი მოგება", f"₾{df[profit_col].sum():,.0f}")
            
            st.markdown("---")
            st.subheader("📋 მთელი მონაცემი")
            st.dataframe(df, use_container_width=True, height=400)
        
        # ============ TAB 2: თვეების ანალიზი ============
        with tab2:
            st.subheader("📅 თვეების მიხედვით ანალიზი (2025)")
            
            month_data = df.groupby(month_col).agg({
                weight_col: 'sum',
                amount_col: 'sum',
                profit_col: 'sum',
                profit_pct_col: 'mean'
            }).round(2)
            
            st.dataframe(month_data, use_container_width=True)
            
            st.markdown("---")
            st.line_chart(month_data[profit_col])
        
        # ============ TAB 3: ქვეყნების ანალიზი ============
        with tab3:
            st.subheader("🌍 ქვეყნების მიხედვით ანალიზი (2025)")
            
            country_data = df.groupby(country_col).agg({
                weight_col: 'sum',
                amount_col: 'sum',
                profit_col: 'sum',
                profit_pct_col: 'mean'
            }).round(2).sort_values(profit_col, ascending=False)
            
            st.dataframe(country_data, use_container_width=True)
            st.bar_chart(country_data[profit_col])
        
        # ============ TAB 4: 2026 გეგმა ============
        with tab4:
            st.subheader("🔮 2026 წელი - პროგნოზა სეტინგი")
            
            growth_rate = st.slider("ზრდის ტემპი (%) - 2026:", -100, 300, 15, step=5)
            
            current_total = df[profit_col].sum()
            forecast_2026_total = current_total * (1 + growth_rate / 100)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("2025 ჯამი", f"₾{current_total:,.0f}")
            col2.metric("2026 ჯამი", f"₾{forecast_2026_total:,.0f}", f"₾{forecast_2026_total - current_total:+,.0f}")
            col3.metric("ზრდის ტემპი", f"{growth_rate}%")
            col4.metric("საშუო თვე", f"₾{forecast_2026_total/12:,.0f}")
            
            st.markdown("---")
            st.subheader("🌍 ქვეყნების მიხედვით 2026 პროგნოზა")
            
            country_2026 = df.groupby(country_col)[profit_col].sum()
            country_2026_forecast = (country_2026 * (1 + growth_rate / 100)).round(0)
            
            country_forecast_df = pd.DataFrame({
                '2025': country_2026.round(0),
                '2026': country_2026_forecast,
                'ზრდა': country_2026_forecast - country_2026.round(0)
            }).sort_values('2026', ascending=False)
            
            st.dataframe(country_forecast_df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📅 თვეების მიხედვით 2026 პროგნოზა")
            
            month_2026 = df.groupby(month_col)[profit_col].sum()
            month_2026_forecast = (month_2026 * (1 + growth_rate / 100)).round(0)
            
            month_forecast_df = pd.DataFrame({
                '2025': month_2026.round(0),
                '2026': month_2026_forecast
            })
            
            st.dataframe(month_forecast_df, use_container_width=True)
            st.line_chart(month_forecast_df)
        
        # ============ TAB 5: გენერირებული 2026 მონაცემი ============
        with tab5:
            st.subheader("📊 2026 წელი - გენერირებული მონაცემი")
            
            growth_rate_gen = st.slider("ზრდის ტემპი (%) - გენერირებული:", -100, 300, 15, step=5, key="growth_gen")
            
            # 2026 მონაცემი
            df_2026 = df.copy()
            
            for col in [weight_col, amount_col, profit_col]:
                df_2026[col] = (df_2026[col] * (1 + growth_rate_gen / 100)).round(0)
            
            # ყველა თვის პოპულაცია
            all_months = ['იანვარი', 'თებერვალი', 'მარტი', 'აპრილი', 'მაისი', 'ივ](#)*

