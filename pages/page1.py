import streamlit as st
import datetime
from tools.patternPredictor import PatternPredictor

# 페이지 설정
st.set_page_config(page_title="Stock Price Prediction (Patterns)", page_icon="📈")

# 페이지 사이드바
st.sidebar.header("Settings")
with st.sidebar:
    with st.form("settings"):
        symbolInput = st.text_input("Symbol of the stock", value="005930")
        
        today = datetime.datetime.now()
        periodInput = st.date_input(
        "Period of the pattern to search",
        (today - datetime.timedelta(days=30), today),
        datetime.date(today.year, 1, 1),
        today,
        format="YYYY-MM-DD",
        )

        datesToPredictInput = st.slider('Dates to predict', 0, 30, 10)

        submitted = st.form_submit_button("Run")

# 페이지 본문
st.markdown("# Stock Price Prediction (by searching similar patterns)")
if submitted:
    with st.spinner('Running...'):
        pp = PatternPredictor()
        pp.getStockData(symbol=symbolInput)
        cosSimsList = pp.searchPattern(start_date=periodInput[0], end_date=periodInput[1])
        fig = pp.plotPattern(idx=cosSimsList.index[0], datesToPredict=datesToPredictInput)
        st.pyplot(fig)
        st.write(f"The similar pattern shown above has a value of {cosSimsList.iloc[0].round(4)} which is the highest value of the cosine similarity between the reference stock price. The closer the value is to 1, the more similar it is.")
    