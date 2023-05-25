import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def main():
    """return the data and a plotly express chart"""
    df = pd.read_csv('data/sba_pool_data.csv')

    df['Issue Date'] = pd.to_datetime(df['Issue Date'])
    df['Issuer'] = df['Issuer'].str.lower()

    vals = df['Mortgage Loan Margin'].value_counts().index.to_list()
    vals_1 = []
    for v in vals:
        try:
            test_val = float(v)
            vals_1.append(v)
        except:
            continue
    df = df[df['Mortgage Loan Margin'].isin(vals_1)]
    df['Mortgage Loan Margin'] = df['Mortgage Loan Margin'].astype(float)
    df.loc[(~df['Issuer'].str.contains('/'))&(df['Issuer'].str.contains('brean')), 'Issuer'] = 'brean capital'
    df.loc[(~df['Issuer'].str.contains('/'))&(df['Issuer'].str.contains('fhn')), 'Issuer'] = 'fhn financial'
    df.loc[(~df['Issuer'].str.contains('/'))&(df['Issuer'].str.contains('raym')), 'Issuer'] = 'raymond james bank'
    df.loc[(~df['Issuer'].str.contains('/'))&(df['Issuer'].str.contains('bmo')), 'Issuer'] = 'BMO'
    df.loc[(~df['Issuer'].str.contains('/'))&(df['Issuer'].str.contains('bank of america')), 'Issuer'] = 'Bank of America'
    df['Issuer'] = df['Issuer'].str.upper()
    fig = px.scatter(data_frame=df, x='Issue Date', y='Mortgage Loan Margin', color='Issuer',size='Mtge Orig Amt', title='Historical SBA Pool Creation',
                     hover_data={'Mortgage Loan Margin':':.2f', 'Mtge Orig Amt': ':,.2f'})
    return df , fig


st.title('SBA Pool Tracker')


df, fig = main()

st.plotly_chart(fig, theme=None, use_container_width=True)