import streamlit as st
import pandas as pd
import altair as alt
import numpy as np


df = pd.read_csv('saisyuu3.csv', header=0)
df.columns = df.columns.str.strip() 

st.title('日本の都道府県別人口推移を読み取る')
st.write('このアプリは、日本の各都道府県の人口推移データを視覚化します。')
st.write('使い方：')
st.write('サイドバーで表示したい都道府県と年齢層を選択してください。各タブで男性、女性、男女合計の人口データを確認できます。')


age_cols = df.columns[5:]
df[age_cols] = (
    df[age_cols]
    .astype(str) # 文字列型に
    .apply(lambda s: s.str.replace(',', '', regex=False)) # カンマを削除
    .astype(int) # 整数型に
)


tab1, tab2, tab3 = st.tabs(['男性人口データ', '女性人口データ', '男女合計人口データ'])
with st.sidebar:
    st.header('オプション選択')
    st.write('表示する都道府県を選択してください。')
    prefectures_grops = df['全国・都道府県'].unique().tolist()
    selected_prefectures = st.multiselect('都道府県を選択', prefectures_grops)
    age = st.selectbox('年齢層を選択', age_cols)
    


with tab1:
    st.header('男性人口データの表示')
    df_filtered = df[(df['gender'] == '男') & (df['全国・都道府県'].isin(selected_prefectures))]
    fig = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('全国・都道府県:N', title='都道府県'),
        y=alt.Y(age, title='人口(千人)'),
        color=alt.Color('全国・都道府県:N', legend=None)
    )
    st.altair_chart(fig, use_container_width=True)
    st.info(f'このグラフは、{selected_prefectures}における、{age}歳の男性人口を示しています。')


with tab2:
    st.header('女性人口データの表示')
    df_filtered = df[(df['gender'] == '女') & (df['全国・都道府県'].isin(selected_prefectures))]
    fig = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('全国・都道府県:N', title='都道府県'),
        y=alt.Y(age, title='人口(千人)'),
        color=alt.Color('全国・都道府県:N', legend=None)
    )
    st.altair_chart(fig, use_container_width=True)
    st.info(f'このグラフは、{selected_prefectures}における、{age}歳の女性人口を示しています。')

with tab3:
    st.header('男女合計人口データの表示')
    df_filtered = df[(df['gender'] == '男女計') & (df['全国・都道府県'].isin(selected_prefectures))]
    fig = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('全国・都道府県:N', title='都道府県'),
        y=alt.Y(age, title='人口(千人)'),
        color=alt.Color('全国・都道府県:N', legend=None)
    )
    st.altair_chart(fig, use_container_width=True)
    st.info(f'このグラフは、{selected_prefectures}における、{age}歳の男女合計人口を示しています。')

st.download_button(
        label='データをCSVでダウンロード',
        data=df.to_csv(index=False).encode('utf-8-sig'),
        file_name='saisyuu3.csv',
        mime='text/csv'
    )
st.write('データソース: 総務省統計局「国勢調査」')

