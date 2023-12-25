import streamlit as st
import datetime
from tools.patternPredictor import PatternPredictor

# 페이지 설정
st.set_page_config(page_title="Pattern Prediction", page_icon="📈")

# 페이지 사이드바
st.sidebar.header("Page 1")
with st.sidebar:
    today = datetime.datetime.now()
    this_year = today.year
    jan_1 = datetime.date(this_year, 1, 1)
    dec_31 = datetime.date(this_year, 12, 31)
    
    with st.form("pattern_predictor"):
        stockCode = st.text_input('Select the symbol of stock')
        
        d = st.date_input(
        "Select the dates of the pattern",
        (today - datetime.timedelta(days=14), today),
        jan_1,
        today,
        format="MM.DD.YYYY",
        )

        window = st.slider('Select days to predict', 0, 30, 5)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

# 페이지 본문
st.markdown("# Pattern Prediction")
if submitted:
    with st.spinner('Predicting...'):
        pp = PatternPredictor()
        pp.period = window
        pp.getStockData(symbol=stockCode)
        cosSimsList = pp.searchPattern(start_date=d[0], end_date=d[1])
        meanList = pp.stat_prediction(results=cosSimsList)
        fig = pp.plot_pattern(idx=cosSimsList.index[0])
        st.pyplot(fig)
    