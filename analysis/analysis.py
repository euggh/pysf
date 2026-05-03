import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.errors import EmptyDataError

# web страница
st.set_page_config(page_title="Анализ табличных данных", layout="wide")

# upload file cache
@st.cache_data
def process_data(file):
    df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8')
    
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['time', 'date', 'at']):
            if df[col].astype(str).str.strip().any():
                try:
                    df[col] = pd.to_datetime(df[col], format='mixed', errors='coerce')
                except:
                    continue
    return df

# session state
if "df" not in st.session_state:
    st.session_state.df = None

st.title("Анализ табличных данных")

# upload file
uploaded_file = st.file_uploader("Загрузите CSV-файл", type="csv")

if uploaded_file:
    try:
        data = process_data(uploaded_file)
        if data.empty:
            st.error("Файл не содержит данных.")
        else:
            st.session_state.df = data
    except EmptyDataError:
        st.error("Файл пустой")
    except Exception as e:
        st.error(f"Ошибка чтения файла: {e}")

# web страница при корректном файле
if st.session_state.df is not None:
    df = st.session_state.df
    all_columns = df.columns.tolist()

# таблица
    st.subheader("Содержимое файла")
    selected_view_cols = st.multiselect(
        "Выберите столбцы", 
        options=all_columns, 
        default=all_columns
    )
    
    if selected_view_cols:
        st.dataframe(df[selected_view_cols].head(100), width='stretch')
    else:
        st.info("Выберите столбцы")

    # статистика
    st.subheader("Статистический анализ")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        stat_col = st.selectbox("Выберите числовой столбец для анализа:", numeric_cols)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Среднее значение", f"{df[stat_col].mean():.2f}")
        m2.metric("Медиана", f"{df[stat_col].median():.2f}")
        m3.metric("Станд. отклонение", f"{df[stat_col].std():.2f}")
    else:
        st.warning("В файле нет числовых данных для анализа.")

    # график
    st.subheader("Графики")
    
    col_left, col_right = st.columns(2)
    with col_left:
        x_axis = st.selectbox("Ось X", all_columns, index=0)
    with col_right:
        y_axis = st.selectbox("Ось Y", all_columns, index=1 if len(all_columns) > 1 else 0)
        
    chart_type = st.radio("Тип графика:", ["Линейный график", "Диаграмма рассеяния"], horizontal=True)

    # первые 1000 строк
    plot_df = df.head(1000).sort_values(by=x_axis) if chart_type == "Линейный график" else df.head(1000)

    if chart_type == "Линейный график":
        fig = px.line(plot_df, x=x_axis, y=y_axis, title=f"{y_axis} от {x_axis}")
    else:
        fig = px.scatter(plot_df, x=x_axis, y=y_axis, title=f"Связь {y_axis} и {x_axis}")

    st.plotly_chart(fig, width='stretch')

else:
    st.info("Идет загрузка CSV-файла...")
