import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import base64

sns.set()



st.set_page_config(page_title="Stock Price Analyser", layout="wide", page_icon = '📈' )
st.markdown("# 📈 Stock Price Analyser")


with open('stock.css') as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html = True)




with st.sidebar:
    st.markdown("## Upload Stock CSV Data")
    uploaded_file = st.file_uploader(" ", type="csv")
    
    if uploaded_file is None:
        st.info("Please upload a CSV file containing stock data.")
    if uploaded_file:
        st.success("File uploaded successfully!")


if uploaded_file:
    tsla = pd.read_csv(uploaded_file)
    st.success("Stock data uploaded!")
else:
    tsla = pd.read_csv('TSLA.csv')
    st.warning("Sample data is being used. Upload your own stock CSV for personalized analysis. CSV file must contain (Open,High,Low and Close) columns!!!")


tsla['Date'] = pd.to_datetime(tsla['Date'])
tsla.set_index('Date', inplace=True)


min_date = tsla.index.min().date()
max_date = tsla.index.max().date()

st.markdown("## Stock Price Overview")




selected_column = st.selectbox(
    "Select a stock attribute to analyze", options=['Open', 'High', 'Low', 'Close'], index=3
)


selected_dates = st.slider(
    'Select The Period', min_value=min_date, max_value=max_date,
    value=(min_date, max_date), format="YYYY-MM-DD"
)

start_date, end_date = selected_dates
tsla_filtered = tsla[(tsla.index >= pd.to_datetime(start_date)) & (tsla.index <= pd.to_datetime(end_date))]


min_num = tsla_filtered[selected_column].min()
max_num = tsla_filtered[selected_column].max()

min_date = tsla_filtered[tsla_filtered[selected_column] == min_num].index[0].date()
max_date = tsla_filtered[tsla_filtered[selected_column] == max_num].index[0].date()



col1, col2, col3 = st.columns(3)
col1.metric(f"📉 Minimum {selected_column}", f"{min_num:.2f}", f"Date: {min_date}")
col2.metric(f"📈 Maximum {selected_column}", f"{max_num:.2f}", f"Date: {max_date}")
col3.metric(f"💸 Profit from Max and Min Price ", f"${max_num - min_num:.2f}", f" P%: {((max_num - min_num)/max_num)*100:.2f}% ")

chart_data = tsla_filtered.reset_index()[['Date', selected_column]]
chart = alt.Chart(chart_data).mark_line().encode(
    x='Date:T', y=f'{selected_column}:Q', tooltip=['Date:T', f'{selected_column}:Q']
).interactive().properties(width=800, height=400)

st.altair_chart(chart, use_container_width=True)

st.markdown("## 💵 Investment Simulation")
st.markdown("##### This is based on the period selected ")


cash_invested = st.number_input("Enter the cash amount you want to invest ($)", min_value=1, value=1000)


shares_bought = cash_invested / min_num
final_value = shares_bought * max_num
profit_loss = (final_value - cash_invested) 


if profit_loss <= cash_invested:
    st.error(f"**Remaining Amount**: ${profit_loss:.2f}")
else:
     st.success(f"**Remaining Amount**: ${profit_loss:.2f}")


roi = ((max_num - min_num) / min_num) * 100

if profit_loss <= cash_invested:
    st.error(f"**Return on Investment (ROI)**: {roi - 100:.2f}%")
else:
    st.success(f"**Return on Investment (ROI)**: {roi - 100:.2f}%")




st.markdown("## 📥 Download Results")
download_data = pd.DataFrame({
    "Date Range": [f"{start_date} to {end_date}"],
    "Initial Cash": [cash_invested],
    "Minimum Price": [min_num],
    "Maximum Price": [max_num],
    "Final Value": [final_value],
    "Profit/Loss": [profit_loss],
    "ROI (%)": [roi]
})

csv = download_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  
href = f'<a href="data:file/csv;base64,{b64}" download="stock_analysis.csv">Download CSV File</a>'
st.markdown(href, unsafe_allow_html=True)


st.markdown("---")
st.markdown("**📊 Stock Price Analyzer** helps you evaluate stock performance, visualize trends, "
            "and simulate investment returns over custom periods.")
st.markdown("Built with 💻 by Herbert.")

