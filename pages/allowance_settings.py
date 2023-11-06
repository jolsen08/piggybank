import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Piggy Bank | Allowance Settings",
    page_icon='🐷',
    layout='wide'
)

st.title('Allowance Settings')

df = pd.read_csv('piggy_bank_table.csv')

with st.form("Change Allowance Settings"):
    savings = st.slider("Savings (% of allowance)", min_value=0, max_value=100, step=1, value=round(100*df.at[0,'savings']))
    if df.at[0,'tithing'] > 0:
        tithing_value = True
    else:
        tithing_value = False
    if st.checkbox("Apply Tithing (10% of allowance)", value=tithing_value):
        tithing = .1
    else:
        tithing = 0
    other_witholdings = st.slider("Other Witholdings (% of allowance)", min_value=0, max_value=100, step=1, value=round(100*df.at[0,'other_witholdings']))

    if st.form_submit_button("Submit Changes"):
        for index, row in df.iterrows():
            df.at[index,'savings'] = savings/100
            df.at[index, 'tithing'] = tithing
            df.at[index, 'other_witholdings'] = other_witholdings/100

        df.to_csv('piggy_bank_table.csv', index=False)
        st.success("Settings adjusted successfully!")
    

