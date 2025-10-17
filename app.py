import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="📊 გაყიდვების ანალიტიკა",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 გაყიდვების ანალიტიკის სისტემა")
st.markdown("📈 დიაგრამებით სავსე - ქვეყნა × თვე პროგნოზა")

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
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 დაშბორდი", "📅 თვეები", "🌍 ქვეყნები", "🔮 2026", "📋 მონაცემი"])
        
        # ============ TAB 1: დაშბორდი ============
        with tab1:
            st.markdown("## 📊 დაშბორდი")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📋 რიგი", len(df))
            col2.metric("📦 წონა", f"{df['წონა კგ'].sum():,.0f} კგ")
            col3.metric("💰 თანხა", f"₾{df['თანხა'].sum():,.0f}")
            col4.metric("📈 მოგება", f"₾{df['მოგება'].sum():,.0f}")
            
            st.markdown("---")
            
            # დიაგრამა 1: მოგება × თანხა
            fig = px.scatter(df, x='თანხა', y='მოგება', 
                           color='Номенклатура.ქვეყანა',
                           size='წონა კგ',
                           title="მოგება vs თანხა")
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 2: წონა Pie
            weight_by_country = df.groupby('Номენклатура.ქვეყანა')['წონა კგ'].sum()
            fig = go.Figure(data=[go.Pie(labels=weight_by_country.index, values=weight_by_country.values)])
            fig.update_layout(title="წონის განაწილება")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True, height=300)
        
        # ============ TAB 2: თვეები ============
        with tab2:
            st.markdown("## 📅 თვეების ანალიზი")
            
            month_analysis = df.groupby('თვე').agg({
                'წონა კგ': 'sum',
                'თანხა': 'sum',
                'მოგება': 'sum',
                'მოგების პროცენტი': 'mean'
            }).round(2)
            
            month_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
            st.dataframe(month_analysis, use_container_width=True)
            
            st.markdown("---")
            
            # Line chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=month_analysis.index, y=month_analysis['თანხა ₾'],
                                    mode='lines+markers', name='თანხა'))
            fig.add_trace(go.Scatter(x=month_analysis.index, y=month_analysis['მოგება ₾'],
                                    mode='lines+markers', name='მოგება'))
            st.plotly_chart(fig, use_container_width=True)
            
            # Heatmap
            pivot = df.pivot_table(values='მოგება', index='თვე', columns='Номენклатура.ქვეყანა', aggfunc='sum')
            fig = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index))
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 3: ქვეყნები ============
        with tab3:
            st.markdown("## 🌍 ქვეყნების ანალიზი")
            
            country_analysis = df.groupby('Номенклатура.ქვეყანა').agg({
                'წონა კგ': 'sum',
                'თანხა': 'sum',
                'მოგება': 'sum',
                'მოგების პროცენტი': 'mean'
            }).round(2).sort_values('მოგება', ascending=False)
            
            st.dataframe(country_analysis, use_container_width=True)
            
            st.markdown("---")
            
            # Bar charts
            fig = px.bar(country_analysis.reset_index(), x='Номенклатура.ქვეყანა', y='მოგება',
                        title="მოგება ქვეყნების მიხედვით")
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 4: 2026 პროგნოზა ============
        with tab4:
            st.markdown("## 🔮 2026 პროგნოზა")
            
            metric_type = st.selectbox("აირჩიეთ მეტრიკა:", ["მოგება", "თანხა", "წონა კგ"])
            growth_rate = st.slider("ზრდის ტემპი (%):", -100, 300, 15, step=5)
            
            if metric_type == "მოგება":
                current = df['მოგება'].sum()
            elif metric_type == "თანხა":
                current = df['თანხა'].sum()
            else:
                current = df['წონა კგ'].sum()
            
            forecast = current * (1 + growth_rate / 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("2025", f"{current:,.0f}")
            col2.metric("2026", f"{forecast:,.0f}", f"{forecast-current:+,.0f}")
            col3.metric("ზრდა", f"{growth_rate}%")
            
            st.markdown("---")
            
            # ქვეყნების პროგნოზა
            if metric_type == "მოგება":
                country_current = df.groupby('Номенклатура.ქვეყანა')['მოგება'].sum()
            elif metric_type == "თანხა":
                country_current = df.groupby('Номენклатура.ქვეყანა')['თანხა'].sum()
            else:
                country_current = df.groupby('Номენклатура.ქვეყანა')['წონა კგ'].sum()
            
            country_forecast = (country_current * (1 + growth_rate / 100)).round(0)
            
            forecast_df = pd.DataFrame({
                '2025': country_current.round(0),
                '2026': country_forecast
            }).sort_values('2026', ascending=False)
            
            st.dataframe(forecast_df, use_container_width=True)
            
            # Bar comparison
            fig = go.Figure(data=[
                go.Bar(name='2025', x=forecast_df.index, y=forecast_df['2025']),
                go.Bar(name='2026', x=forecast_df.index, y=forecast_df['2026'])
            ])
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 5: მონაცემი ============
        with tab5:
            st.markdown("## 📋 მონაცემი")
            st.dataframe(df, use_container_width=True, height=500)
            
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 CSV", csv, "sales_data.csv", "text/csv")
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")

else:
    st.markdown("## 📁 XLSX ფაილი ატვირთეთ დასაწყებად")

st.markdown("---")
st.markdown("© 2025 გაყიდვების ანალიტიკა | **gigalabichi1**")
