# 1. Импортируем библиотеки
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# 2. Парсим с Wikipedia список тикеров всех компаний из S&P 500
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
df = pd.read_html(url)[0]
ticker_dict = (
    {security: [symbol, sector, location] for security, symbol, sector, location in zip(df['Security'], df['Symbol'], df['GICS Sector'], df['Headquarters Location'])}
)

# 3. Виджет выбора компании
selected_ticker = st.sidebar.selectbox('Выберите компанию:', ticker_dict)

# 4. Виджет выбора периода отображения графиков
selected_period = (
    st.sidebar.date_input(
        label='Выберите период:', value=['2015-01-01', '2025-01-01'], 
        min_value='2015-01-01', max_value='2025-05-31')
)


# 5. Обработка исключений на период выбора пользователем диапазона дат
try:
    start, end = selected_period
except (ValueError, NameError):
    st.write(f'## Выберите период для отображения котировок акций {selected_ticker} ')
else:
    # 6. Построение графиков
    st.write(f'# Котировки акций компании {selected_ticker}')
    st.write(f"""
    Тикер - {ticker_dict.get(selected_ticker)[0]}\n
    Отрасль - {ticker_dict.get(selected_ticker)[1]}\n
    Штаб-квартира - {ticker_dict.get(selected_ticker)[2]}
    """)
    
    tickerSymbol = ticker_dict.get(selected_ticker)[0]
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=str(start), end=str(end))

    st.write('## Стоимость акции')
    st.line_chart(tickerDf.Close)
    st.write('## Объем торгов')
    st.line_chart(tickerDf.Volume)

