import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Analytics", layout="wide")

st.title("📊 Sales Analytics System")

uploaded_file = st.file_uploader("Upload XLSX File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        st.write("### File Columns:")
        st.write(df.columns.tolist())
        
        st.success("✅ File loaded successfully!")
        st.write(f"Rows: {len(df)} | Columns: {len(df.columns)}")
        
        columns = df.columns.tolist()
        
        st.markdown("---")
        st.markdown("### Configure Columns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            country_col = st.selectbox("Country Column:", columns, index=0)
            month_col = st.selectbox("Month Column:", columns, index=1 if len(columns) > 1 else 0)
        
        with col2:
            weight_col = st.selectbox("Weight Column:", columns, index=2 if len(columns) > 2 else 0)
            amount_col = st.selectbox("Amount Column:", columns, index=3 if len(columns) > 3 else 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            profit_col = st.selectbox("Profit Column:", columns, index=4 if len(columns) > 4 else 0)
        
        with col2:
            profit_pct_col = st.selectbox("Profit % Column:", columns, index=5 if len(columns) > 5 else 0)
        
        st.markdown("---")
        
        for col in [weight_col, amount_col, profit_col, profit_pct_col]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Months", "Countries", "2026 Plan", "Generated"])
        
        with tab1:
            st.subheader("Dashboard - 2025")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", len(df))
            col2.metric("Total Weight", f"{df[weight_col].sum():,.0f} kg")
            col3.metric("Total Amount", f"${df[amount_col].sum():,.0f}")
            col4.metric("Total Profit", f"${df[profit_col].sum():,.0f}")
            
            st.markdown("---")
            st.subheader("Full Data")
            st.dataframe(df, use_container_width=True, height=400)
        
        with tab2:
            st.subheader("Monthly Analysis (2025)")
            
            month_data = df.groupby(month_col).agg({
                weight_col: 'sum',
                amount_col: 'sum',
                profit_col: 'sum',
                profit_pct_col: 'mean'
            }).round(2)
            
            st.dataframe(month_data, use_container_width=True)
            
            st.markdown("---")
            st.line_chart(month_data[profit_col])
        
        with tab3:
            st.subheader("Country Analysis (2025)")
            
            country_data = df.groupby(country_col).agg({
                weight_col: 'sum',
                amount_col: 'sum',
                profit_col: 'sum',
                profit_pct_col: 'mean'
            }).round(2).sort_values(profit_col, ascending=False)
            
            st.dataframe(country_data, use_container_width=True)
            st.bar_chart(country_data[profit_col])
        
        with tab4:
            st.subheader("2026 Forecast")
            
            growth_rate = st.slider("Growth Rate (%) - 2026:", -100, 300, 15, step=5)
            
            current_total = df[profit_col].sum()
            forecast_2026_total = current_total * (1 + growth_rate / 100)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("2025 Total", f"${current_total:,.0f}")
            col2.metric("2026 Total", f"${forecast_2026_total:,.0f}", f"${forecast_2026_total - current_total:+,.0f}")
            col3.metric("Growth Rate", f"{growth_rate}%")
            col4.metric("Monthly Avg", f"${forecast_2026_total/12:,.0f}")
            
            st.markdown("---")
            st.subheader("2026 Forecast by Country")
            
            country_2026 = df.groupby(country_col)[profit_col].sum()
            country_2026_forecast = (country_2026 * (1 + growth_rate / 100)).round(0)
            
            country_forecast_df = pd.DataFrame({
                '2025': country_2026.round(0),
                '2026': country_2026_forecast,
                'Growth': country_2026_forecast - country_2026.round(0)
            }).sort_values('2026', ascending=False)
            
            st.dataframe(country_forecast_df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("2026 Forecast by Month")
            
            month_2026 = df.groupby(month_col)[profit_col].sum()
            month_2026_forecast = (month_2026 * (1 + growth_rate / 100)).round(0)
            
            month_forecast_df = pd.DataFrame({
                '2025': month_2026.round(0),
                '2026': month_2026_forecast
            })
            
            st.dataframe(month_forecast_df, use_container_width=True)
            st.line_chart(month_forecast_df)
        
        with tab5:
            st.subheader("2026 Generated Data")
            
            growth_rate_gen = st.slider("Growth Rate (%) - Generated:", -100, 300, 15, step=5, key="growth_gen")
            
            df_2026 = df.copy()
            
            for col in [weight_col, amount_col, profit_col]:
                df_2026[col] = (df_2026[col] * (1 + growth_rate_gen / 100)).round(0)
            
            months_list = df[month_col].unique().tolist()
            all_months = ['January', 'February', 'March', 'April', 'May', 'June',
                         'July', 'August', 'September', 'October', 'November', 'December']
            
            existing_months = set(months_list)
            missing_months = [m for m in all_months if m not in existing_months]
            
            additional_rows = []
            
            for missing_month in missing_months:
                month_idx = all_months.index(missing_month)
                
                for existing_month in existing_months:
                    existing_idx = all_months.index(existing_month) if existing_month in all_months else -1
                    
                    if existing_idx == month_idx:
                        month_df = df[df[month_col] == existing_month].copy()
                        
                        for i, row in month_df.iterrows():
                            new_row = row.copy()
                            new_row[month_col] = missing_month
                            
                            for col in [weight_col, amount_col, profit_col]:
                                new_row[col] = (new_row[col] * (1 + growth_rate_gen / 100)).round(0)
                            
                            additional_rows.append(new_row)
                        break
            
            if additional_rows:
                df_2026_complete = pd.concat([df_2026, pd.DataFrame(additional_rows)], ignore_index=True)
            else:
                df_2026_complete = df_2026
            
            st.markdown(f"### 2026 Complete Data (Growth: {growth_rate_gen}%)")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", len(df_2026_complete))
            col2.metric("Weight", f"{df_2026_complete[weight_col].sum():,.0f} kg")
            col3.metric("Amount", f"${df_2026_complete[amount_col].sum():,.0f}")
            col4.metric("Profit", f"${df_2026_complete[profit_col].sum():,.0f}")
            
            st.markdown("---")
            st.dataframe(df_2026_complete, use_container_width=True, height=500)
            
            st.markdown("---")
            st.subheader("Download Generated Data")
            
            csv = df_2026_complete.to_csv(index=False)
            st.download_button(
                label="Download 2026 CSV",
                data=csv,
                file_name=f"sales_2026_forecast_{growth_rate_gen}percent.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Check if Excel file format is correct!")

else:
    st.info("Upload XLSX file to get started")

st.markdown("---")
st.markdown("© 2025 Sales Analytics | gigalabichi1")
