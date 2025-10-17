import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📊 გაყიდვების ანალიტიკა", layout="wide")

st.title("📊 გაყიდვების ანალიტიკის სისტემა")
st.markdown("📅 2026 წელი პროგნოზა + თვეების დაკომპლექტება")

uploaded_file = st.file_uploader("📁 XLSX ფაილის ატვირთვა", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # რიცხვითი სვეტების კონვერტაცია
    for col in ['წონა კგ', 'თანხა', 'მოგება', 'მოგების პროცენტი']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    st.success("✅ წარმატებით ჩატვირთა!")
    st.write(f"📋 რიგი: {len(df)} | 📊 სვეტი: {len(df.columns)}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 დაშბორდი", "📅 თვეები", "🌍 ქვეყნები", "🔮 2026 გეგმა", "📊 გენერირებული"])
    
    # ============ TAB 1: დაშბორდი ============
    with tab1:
        st.subheader("📊 დაშბორდი - 2025 წელი")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 რიგი", len(df))
        col2.metric("📦 ჯამი წონა", f"{df['წონა კგ'].sum():,.0f} კგ")
        col3.metric("💰 ჯამი თანხა", f"₾{df['თანხა'].sum():,.0f}")
        col4.metric("📈 ჯამი მოგება", f"₾{df['მოგება'].sum():,.0f}")
        
        st.markdown("---")
        st.subheader("📋 მთელი მონაცემი")
        st.dataframe(df, use_container_width=True, height=400)
    
    # ============ TAB 2: თვეების ანალიზი ============
    with tab2:
        st.subheader("📅 თვეების მიხედვით ანალიზი (2025)")
        
        month_data = df.groupby('თვე').agg({
            'წონა კგ': 'sum',
            'თანხა': 'sum',
            'მოგება': 'sum',
            'მოგების პროცენტი': 'mean'
        }).round(2)
        
        st.dataframe(month_data, use_container_width=True)
        
        st.markdown("---")
        st.line_chart(month_data['მოგება'])
    
    # ============ TAB 3: ქვეყნების ანალიზი ============
    with tab3:
        st.subheader("🌍 ქვეყნების მიხედვით ანალიზი (2025)")
        
        country_data = df.groupby('Номенклатура.ქვეყანა').agg({
            'წონა კგ': 'sum',
            'თანხა': 'sum',
            'მოგება': 'sum',
            'მოგების პროცენტი': 'mean'
        }).round(2).sort_values('მოგება', ascending=False)
        
        st.dataframe(country_data, use_container_width=True)
        st.bar_chart(country_data['მოგება'])
    
    # ============ TAB 4: 2026 გეგმა ============
    with tab4:
        st.subheader("🔮 2026 წელი - პროგნოზა სეტინგი")
        
        growth_rate = st.slider("ზრდის ტემპი (%) - 2026:", -100, 300, 15, step=5)
        
        # მთელი 2026 პროგნოზა
        current_total = df['მოგება'].sum()
        forecast_2026_total = current_total * (1 + growth_rate / 100)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("2025 ჯამი", f"₾{current_total:,.0f}")
        col2.metric("2026 ჯამი", f"₾{forecast_2026_total:,.0f}", f"₾{forecast_2026_total - current_total:+,.0f}")
        col3.metric("ზრდის ტემპი", f"{growth_rate}%")
        col4.metric("საშუო თვე", f"₾{forecast_2026_total/12:,.0f}")
        
        st.markdown("---")
        
        # ქვეყნების მიხედვით 2026
        st.subheader("🌍 ქვეყნების მიხედვით 2026 პროგნოზა")
        
        country_2026 = df.groupby('Номенклатура.ქვეყანა')['მოგება'].sum()
        country_2026_forecast = (country_2026 * (1 + growth_rate / 100)).round(0)
        
        country_forecast_df = pd.DataFrame({
            '2025': country_2026.round(0),
            '2026': country_2026_forecast,
            'ზრდა': country_2026_forecast - country_2026.round(0),
            'ზრდა %': ((country_2026_forecast - country_2026.round(0)) / country_2026 * 100).round(1)
        }).sort_values('2026', ascending=False)
        
        st.dataframe(country_forecast_df, use_container_width=True)
        
        st.markdown("---")
        
        # თვეების მიხედვით 2026
        st.subheader("📅 თვეების მიხედვით 2026 პროგნოზა")
        
        month_2026 = df.groupby('თვე')['მოგება'].sum()
        month_2026_forecast = (month_2026 * (1 + growth_rate / 100)).round(0)
        
        month_forecast_df = pd.DataFrame({
            '2025': month_2026.round(0),
            '2026': month_2026_forecast
        }).sort_index()
        
        st.dataframe(month_forecast_df, use_container_width=True)
        st.line_chart(month_forecast_df)
    
    # ============ TAB 5: გენერირებული 2026 მონაცემი ============
    with tab5:
        st.subheader("📊 2026 წელი - გენერირებული მონაცემი (თვეების დაკომპლექტება)")
        
        growth_rate = st.slider("ზრდის ტემპი (%) - გენერირებული:", -100, 300, 15, step=5, key="growth_generated")
        
        st.markdown("---")
        st.info("📌 თუ 2025 წელში რაიმე თვე აკლია, 2026-ში შეივსება წინა წლის ანალოგური თვეებით")
        
        # 2026 მონაცემი გენერირება
        df_2026 = df.copy()
        
        # ზრდის ფაქტორი გამოყენება
        for col in ['წონა კგ', 'თანხა', 'მოგება']:
            if col in df_2026.columns:
                df_2026[col] = (df_2026[col] * (1 + growth_rate / 100)).round(0)
        
        # ყველა თვის პополნება
        all_months = ['იანვარი', 'თებერვალი', 'მარტი', 'აპრილი', 'მაისი', 'ივნისი',
                      'ივლისი', 'აგვისტო', 'სექტემბერი', 'ოქტომბერი', 'ნოემბერი', 'დეკემბერი']
        
        existing_months = df['თვე'].unique()
        missing_months = [m for m in all_months if m not in existing_months]
        
        if missing_months:
            st.markdown(f"### აკლემი თვეები (შეივსება ანალოგით):")
            st.write(f"🟠 {', '.join(missing_months)}")
            st.markdown("---")
            
            # აკლემი თვეების დაკომპლექტება
            additional_rows = []
            
            for missing_month in missing_months:
                # წინა წლის ანალოგური თვე
                for existing_month in existing_months:
                    # თვეების რიგითი ნომერი
                    month_index = (all_months.index(missing_month) + 1)
                    existing_index = (all_months.index(existing_month) + 1)
                    
                    # თუ ეს იგივე თვეა (მესაზე, მაგალითად)
                    if all_months.index(missing_month) == all_months.index(existing_month):
                        # ამ თვის ყველა ქვეყনის მონაცემი
                        month_df = df[df['თვე'] == existing_month].copy()
                        
                        for idx, row in month_df.iterrows():
                            new_row = row.copy()
                            new_row['თვე'] = missing_month
                            # ზრდის გამოყენება
                            for col in ['წონა კგ', 'თანხა', 'მოგება']:
                                if col in new_row.index:
                                    new_row[col] = (new_row[col] * (1 + growth_rate / 100)).round(0)
                            additional_rows.append(new_row)
                        break
            
            if additional_rows:
                df_2026_complete = pd.concat([df_2026, pd.DataFrame(additional_rows)], ignore_index=True)
            else:
                df_2026_complete = df_2026
        else:
            df_2026_complete = df_2026
        
        st.subheader("✅ 2026 წელი - სრული მონაცემი (ზრდა: {growth_rate}%)")
        
        # სტატისტიკა
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 რიგი", len(df_2026_complete))
        col2.metric("📦 ჯამი წონა", f"{df_2026_complete['წონა კგ'].sum():,.0f} კგ")
        col3.metric("💰 ჯამი თანხა", f"₾{df_2026_complete['თანხა'].sum():,.0f}")
        col4.metric("📈 ჯამი მოგება", f"₾{df_2026_complete['მოგება'].sum():,.0f}")
        
        st.markdown("---")
        st.dataframe(df_2026_complete, use_container_width=True, height=500)
        
        st.markdown("---")
        st.subheader("📥 გენერირებული მონაცემი ჩამოტვირთვა")
        
        # CSV ჩამოტვირთვა
        csv = df_2026_complete.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 2026 წელი - CSV ჩამოტვირთვა",
            data=csv,
            file_name=f"sales_2026_forecast_{growth_rate}percent.csv",
            mime="text/csv"
        )
        
        # Excel ჩამოტვირთვა (თუ openpyxl აკ)
        try:
            excel_buffer = pd.ExcelWriter('/tmp/sales_2026.xlsx', engine='openpyxl')
            df_2026_complete.to_excel(excel_buffer, sheet_name='2026 პროგნოზა', index=False)
            excel_buffer.close()
            
            with open('/tmp/sales_2026.xlsx', 'rb') as f:
                excel_data = f.read()
            
            st.download_button(
                label="📊 2026 წელი - XLSX ჩამოტვირთვა",
                data=excel_data,
                file_name=f"sales_2026_forecast_{growth_rate}percent.xlsx",
                mime="application/vnd.ms-excel"
            )
        except:
            pass
        
        st.markdown("---")
        st.subheader("📊 2026 მოგება თვეების მიხედვით")
        
        month_2026_data = df_2026_complete.groupby('თვე')['მოგება'].sum().reindex(all_months)
        st.bar_chart(month_2026_data)
        
        st.markdown("---")
        st.subheader("🌍 2026 მოგება ქვეყნების მიხედვით")
        
        country_2026_data = df_2026_complete.groupby('Номенклатура.ქვეყანა')['მოგება'].sum().sort_values(ascending=False)
        st.bar_chart(country_2026_data)

else:
    st.info("📁 XLSX ფაილი ატვირთეთ დასაწყებად")

st.markdown("---")
st.markdown("© 2025 გაყიდვების ანალიტიკა | **gigalabichi1** | 2026 წელი გეგმა")
