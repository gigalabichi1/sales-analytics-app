import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

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
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 დაშბორდი", "📅 თვეების ანალიზი", "🌍 ქვეყნების ანალიზი", "🔮 2026 პროგნოზა", "📋 მონაცემი"])
        
        # ============ TAB 1: დაშბორდი ============
        with tab1:
            st.markdown("## 📊 დაშბორდი - KPI მაჩვენებლები")
            
            # KPI Cards
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
            
            # დიაგრამა 1: მოგება × თანხა
            st.markdown("### 📈 მოგება vs თანხა (Scatter)")
            fig = px.scatter(df, x='თანხა', y='მოგება', 
                           color='Номенклатура.ქვეყანა',
                           size='წონა კგ',
                           hover_data=['თვე'],
                           title="მოგება vs თანხა",
                           labels={'თანხა': 'თანხა (₾)', 'მოგება': 'მოგება (₾)'})
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 2: წონა განაწილება
            st.markdown("### 📊 წონის განაწილება (Pie)")
            weight_by_country = df.groupby('Номенклатура.ქვეყანა')['წონა კგ'].sum()
            fig = go.Figure(data=[go.Pie(labels=weight_by_country.index, values=weight_by_country.values,
                                        textinfo="label+percent")])
            fig.update_layout(title="წონის განაწილება ქვეყნების მიხედვით")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📋 მთელი მონაცემთა ცხრილი")
            st.dataframe(df, use_container_width=True, height=300)
        
        # ============ TAB 2: თვეების ანალიზი ============
        with tab2:
            st.markdown("## 📅 თვეების მიხედვით ანალიზი")
            
            # თვეების ანალიზი
            month_analysis = df.groupby('თვე').agg({
                'წონა კგ': 'sum',
                'თანხა': 'sum',
                'მოგება': 'sum',
                'მოგების პროცენტი': 'mean'
            }).round(2)
            
            month_analysis.columns = ['წონა კგ', 'თანხა ₾', 'მოგება ₾', 'მოგება %']
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("საშუო თანხა", f"₾{month_analysis['თანხა ₾'].mean():,.0f}")
            col2.metric("საშუო მოგება", f"₾{month_analysis['მოგება ₾'].mean():,.0f}")
            col3.metric("მაქსი მოგება", f"₾{month_analysis['მოგება ₾'].max():,.0f}")
            col4.metric("მინი მოგება", f"₾{month_analysis['მოგება ₾'].min():,.0f}")
            
            st.markdown("---")
            st.markdown("### 📊 თვეების სტატისტიკა")
            st.dataframe(month_analysis, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 1: თანხა × თვე (Line)
            st.markdown("### 📈 თანხა თვეების მიხედვით (Line)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=month_analysis.index, y=month_analysis['თანხა ₾'],
                                    mode='lines+markers', name='თანხა', line=dict(color='blue', width=3)))
            fig.update_layout(title="თანხა თვეების მიხედვით", xaxis_title="თვე", yaxis_title="თანხა (₾)")
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 2: მოგება × თვე (Line)
            st.markdown("### 📈 მოგება თვეების მიხედვით (Line)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=month_analysis.index, y=month_analysis['მოგება ₾'],
                                    mode='lines+markers', name='მოგება', line=dict(color='green', width=3)))
            fig.update_layout(title="მოგება თვეების მიხედვით", xaxis_title="თვე", yaxis_title="მოგება (₾)")
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 3: წონა × თვე (Bar)
            st.markdown("### 📦 წონა თვეების მიხედვით (Bar)")
            fig = px.bar(month_analysis, x=month_analysis.index, y='წონა კგ',
                        title="წონა თვეების მიხედვით",
                        labels={'x': 'თვე', 'წონა კგ': 'წონა (კგ)'},
                        color_discrete_sequence=['orange'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 4: Pivot - მოგება (თვე × ქვეყნა)
            st.markdown("### 🌍📅 მოგება - თვე × ქვეყნა (Heatmap)")
            pivot_profit = df.pivot_table(values='მოგება', index='თვე', columns='Номენклатура.ქვეყანა', aggfunc='sum')
            fig = go.Figure(data=go.Heatmap(z=pivot_profit.values, x=pivot_profit.columns, y=pivot_profit.index,
                                           colorscale='Greens'))
            fig.update_layout(title="მოგება - თვე × ქვეყნა", xaxis_title="ქვეყნა", yaxis_title="თვე")
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 3: ქვეყნების ანალიზი ============
        with tab3:
            st.markdown("## 🌍 ქვეყნების მიხედვით ანალიზი")
            
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
            
            # დიაგრამა 1: მოგება × ქვეყნა (Bar)
            st.markdown("### 💰 მოგება ქვეყნების მიხედვით (Bar)")
            fig = px.bar(country_analysis.reset_index(), x='Номенклатура.ქვეყანა', y='მოგება ₾',
                        title="მოგება ქვეყნების მიხედვით",
                        color='მოგება ₾',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 2: თანხა × ქვეყნა (Bar)
            st.markdown("### 💸 თანხა ქვეყნების მიხედვით (Bar)")
            fig = px.bar(country_analysis.reset_index(), x='Номенклатура.ქვეყანა', y='თანხა ₾',
                        title="თანხა ქვეყნების მიხედვით",
                        color='თანხა ₾',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
            
            # დიაგრამა 3: წონა × ქვეყნა (Bar)
            st.markdown("### 📦 წონა ქვეყნების მიხედვით (Bar)")
            fig = px.bar(country_analysis.reset_index(), x='Номенклатура.ქვეყანა', y='წონა კგ',
                        title="წონა ქვეყნების მიხედვით",
                        color='წონა კგ',
                        color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 4: მოგების % (Bar)
            st.markdown("### 📊 მოგების % ქვეყნების მიხედვით (Bar)")
            fig = px.bar(country_analysis.reset_index(), x='Номенклатура.ქვეყანა', y='მოგება %',
                        title="მოგების % ქვეყნების მიხედვით",
                        color='მოგება %',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 4: 2026 პროგნოზა ============
        with tab4:
            st.markdown("## 🔮 2026 წელი - პროგნოზა")
            
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
            
            # საერთო პროგნოზა
            if metric_type == "მოგება":
                current_total = df['მოგება'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
                unit = "₾"
            elif metric_type == "თანხა":
                current_total = df['თანხა'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
                unit = "₾"
            else:
                current_total = df['წონა კგ'].sum()
                forecast_total = current_total * (1 + growth_rate / 100)
                diff_total = forecast_total - current_total
                unit = "კგ"
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("2025 წელი", f"{current_total:,.0f} {unit}")
            col2.metric("2026 პროგნოზა", f"{forecast_total:,.0f} {unit}", f"{diff_total:+,.0f} {unit}")
            col3.metric("ზრდის ტემპი", f"{growth_rate}%")
            col4.metric("საშუო თვე", f"{forecast_total/12:,.0f} {unit}")
            
            st.markdown("---")
            st.markdown(f"### 🌍 2026 პროგნოზა - ქვეყნების მიხედვით ({metric_type})")
            
            # ქვეყნების პროგნოზა
            if metric_type == "მოგება":
                country_current = df.groupby('Номენклатура.ქვეყანა')['მოგება'].sum()
            elif metric_type == "თანხა":
                country_current = df.groupby('Номენклатура.ქვეყანა')['თანხა'].sum()
            else:
                country_current = df.groupby('Номენклатура.ქვეყანა')['წონა კგ'].sum()
            
            country_forecast = (country_current * (1 + growth_rate / 100)).round(0)
            
            forecast_df = pd.DataFrame({
                '2025': country_current.round(0),
                '2026': country_forecast,
                'განსხვავება': (country_forecast - country_current.round(0)),
                'ზრდა %': (((country_forecast - country_current.round(0)) / country_current * 100)).round(1)
            }).sort_values('2026', ascending=False)
            
            st.dataframe(forecast_df, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 1: ქვეყნების პროგნოზა (Bar)
            st.markdown(f"### 📈 ქვეყნების პროგნოზა - 2025 vs 2026 ({metric_type})")
            fig = go.Figure(data=[
                go.Bar(name='2025', x=forecast_df.index, y=forecast_df['2025'], marker_color='lightblue'),
                go.Bar(name='2026', x=forecast_df.index, y=forecast_df['2026'], marker_color='darkblue')
            ])
            fig.update_layout(barmode='group', title=f"2025 vs 2026 - {metric_type}",
                            xaxis_title="ქვეყნა", yaxis_title=f"{metric_type}")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 2: თვეების პროგნოზა
            st.markdown(f"### 📅 თვეების მიხედვით 2026 პროგნოზა ({metric_type})")
            
            if metric_type == "მოგება":
                month_current = df.groupby('თვე')['მოგება'].sum()
            elif metric_type == "თანხა":
                month_current = df.groupby('თვე')['თანხა'].sum()
            else:
                month_current = df.groupby('თვე')['წონა კგ'].sum()
            
            month_forecast = (month_current * (1 + growth_rate / 100)).round(0)
            
            month_forecast_df = pd.DataFrame({
                '2025': month_current.round(0),
                '2026': month_forecast
            }).sort_index()
            
            fig = go.Figure(data=[
                go.Scatter(name='2025', x=month_forecast_df.index, y=month_forecast_df['2025'],
                          mode='lines+markers', line=dict(color='blue', width=3)),
                go.Scatter(name='2026', x=month_forecast_df.index, y=month_forecast_df['2026'],
                          mode='lines+markers', line=dict(color='red', width=3))
            ])
            fig.update_layout(title=f"თვეების მიხედვით - 2025 vs 2026",
                            xaxis_title="თვე", yaxis_title=f"{metric_type}")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # დიაგრამა 3: Heatmap - ქვეყნა × თვე
            st.markdown(f"### 🌍📅 ქვეყნა × თვე - 2026 პროგნოზა (Heatmap)")
            
            if metric_type == "მოგება":
                pivot_current = df.pivot_table(values='მოგება', index='Номენклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            elif metric_type == "თანხა":
                pivot_current = df.pivot_table(values='თანხა', index='Номენклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            else:
                pivot_current = df.pivot_table(values='წონა კგ', index='Номენклатура.ქვეყანა', columns='თვე', aggfunc='sum')
            
            pivot_forecast = (pivot_current * (1 + growth_rate / 100)).round(0)
            
            fig = go.Figure(data=go.Heatmap(z=pivot_forecast.values, x=pivot_forecast.columns, y=pivot_forecast.index,
                                           colorscale='RdYlGn'))
            fig.update_layout(title=f"2026 პროგნოზა - ქვეყნა × თვე ({metric_type})",
                            xaxis_title="თვე", yaxis_title="ქვეყნა")
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 5: მონაცემი ============
        with tab5:
            st.markdown("## 📋 სრული მონაცემთა ცხრილი")
            
            all_cols = st.multiselect(
                "აირჩიეთ სვეტები:",
                df.columns.tolist(),
                default=df.columns.tolist()
            )
            
            if all_cols:
                st.dataframe(df[all_cols], use_container_width=True, height=500)
                
                csv = df[all_cols].to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 CSV-ის ჩამოტვირთვა",
                    data=csv,
                    file_name="sales_data.csv",
                    mime="text/csv"
                )
    
    except Exception as e:
        st.error(f"❌ შეცდომა: {str(e)}")

else:
    st.markdown("## 📁 XLSX ფაილი ატვირთეთ დასაწყებად")

st.markdown("---")
st.markdown("© 2025 გაყიდვების ანალიტიკა | **gigalabichi1**")
