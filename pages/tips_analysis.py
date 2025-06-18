# 1. Импортируем библиотеки
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime as dt
import io


# 2. Приветствие
st.write('# Анализ чаевых в ресторане')


# 3. Чтение датафрейма
tips = st.sidebar.file_uploader('Загрузи CSV файл', type='csv')
if tips is not None:
    tips = pd.read_csv(tips)
    st.write('Первые 5 строк датафрейма')
    st.write(tips.head())
else:
    st.stop()


# 4. Обработка датафрейма
# создадим массив значений даты для заполнения
dates_to_choose = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D')
# создадим генератор для случайного заполнения нового столбца значениями
rng = np.random.default_rng(1)
tips['time_order'] = rng.choice(dates_to_choose, size=tips.shape[0])
tips = tips.sort_values('time_order').reset_index()


# 5. Строим графики
# 5.1. График, показывающий динамику чаевых во времени
st.write('### Динамика чаевых во времени')
data_to_draw = tips.groupby('time_order')['tip'].sum()
st.line_chart(data_to_draw, x_label='Дата', y_label='Чаевые')

# 5.2. Гистограмма total_bill
st.write('### Распределение счетов')
st.bar_chart(tips['total_bill'].value_counts(bins=5).sort_index(), x_label='Общий счет', y_label='Количество')

# 5.3. Scatterplot, связывающий total_bill, tip
st.write('### Корреляция величины чека и размера чаевых')
st.scatter_chart(tips, x='total_bill', y='tip', x_label='Общий счет', y_label='Чаевые')

# 5.4. Scatterplot, связывающий total_bill, tip, и size
fig, ax = plt.subplots()
sns.scatterplot(data=tips, x='total_bill', y='tip', size='size', ax=ax)
plt.title('Корреляция величины чека и размера чаевых')
plt.ylabel('Чаевые')
plt.xlabel('Чек')
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(fig)
st.download_button("Скачать график", buf, file_name="scatter_totalbill_tip_size.png", mime="image/png")

# 5.5. Boxplot, связывающий дни недели и размер счета
fig, ax = plt.subplots()
sns.boxplot(data=tips, x='day', y='total_bill', ax=ax)
plt.title('Cвязь между днем недели и размером счета')
plt.ylabel('Размер чека')
plt.xlabel('День')
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(fig)
st.download_button("Скачать график", buf, file_name="boxplot_day_totalbill.png", mime="image/png")

# 5.6. Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу
fig, ax = plt.subplots()
sns.scatterplot(data=tips, x='tip', y='day', hue='sex', ax=ax)
plt.title('Чаевые по дням недели с разделением по полу')
plt.ylabel('День')
plt.xlabel('Размер чека')
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(fig)
st.download_button("Скачать график", buf, file_name="scatter_tip_day_sex.png", mime="image/png")

# 5.7. Boxplot c суммой всех счетов за каждый день, разбивая по time
fig, ax = plt.subplots()
sns.boxplot(data=tips, x="day", y="total_bill", hue="time", ax=ax)
plt.title('Сумма счета по дню недели и времени')
plt.ylabel('Сумма счета')
plt.xlabel('День недели')
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(fig)
st.download_button("Скачать график", buf, file_name="boxplot_day_totalbill_time.png", mime="image/png")

# 5.8. Гистограммы чаевых на обед и ланч
g = sns.FacetGrid(tips, col="time")
g.map(sns.histplot, "tip")
g.set_titles("{col_name}")
g.set_axis_labels("Чаевые", "Количество случаев")
g.fig.suptitle("Гистограммы чаевых по Lunch и Dinner")
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
g.fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(g.fig)
st.download_button("Скачать график", buf, file_name="facetgrid_tip_time.png", mime="image/png")

# 5.9. Scatterplot связывающий размера счета и чаевых
g = (
    sns.relplot(
        data=tips, x='total_bill', y='tip', 
        hue='smoker', col='sex', kind='scatter'
    )
)
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
g.fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(g.fig)
st.download_button("Скачать график", buf, file_name="relplot_totalbill_tip.png", mime="image/png")

# 5.10. Тепловая карта зависимостей численных переменных
corr = tips[['total_bill', 'tip', 'size']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
ax.set_title("Матрица корреляций")
plt.tight_layout()
# Кнопка скачивания графика
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.pyplot(fig)
st.download_button("Скачать график", buf, file_name="heatmap_corr.png", mime="image/png")