
import streamlit as st
import pandas as pd
import plotly.express as px

# fetch data from google sheet to pd
sheet_id = "1HcIFrQxr1rZ4_5m9Of8VbgC0U94FbeETaYamc5_Ro8Y"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    if {'Submission Id', '1st aff country: 1st author'}.issubset(df.columns):
        df_map = df[['Submission Id', '1st aff country: 1st author']].copy()
        df_map.dropna(subset=['1st aff country: 1st author'], inplace=True)

        country_counts = df_map.groupby('1st aff country: 1st author')['Submission Id'].count().reset_index()
        country_counts.rename(columns={
            'Submission Id': '1st author base',
            'Submission Count': 'Total Abstracts Received'
        }, inplace=True)
        
        country_counts.sort_values(by='Total Abstracts Received', ascending=False, inplace=True)

        fig = px.choropleth(
            country_counts,
            locations='1st author base',
            locationmode='country names',
            color='No of abstracts received',
            hover_name='This is where the institute of the primary author is located',
            color_continuous_scale='Viridis',
            title='Number of Abstract Submissions by Country'
        )

        st.title('2024 OGHB Conference Submission Dashboard')
        st.plotly_chart(fig)

        st.subheader('Country-wise Submission Counts')
        st.dataframe(country_counts)
    else:
        st.error("Col not found. Check col names on sheet")
except Exception as e:
    st.error(f"Error loading data: {e}")
