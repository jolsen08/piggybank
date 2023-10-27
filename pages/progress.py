import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Piggy Bank | Progress",
    page_icon='🐷',
    layout='wide'
)

st.title('Progress Toward Goal')

df = pd.read_csv("piggy_bank_table.csv")
child_list = df['first_name'].tolist()


child = st.selectbox("Please Select the Child you would like to view", child_list)

df = df[df['first_name'] == child]

row = df.iloc[0]
st.subheader(row['first_name'])
monthly_allowance = "{:.2f}".format(row['monthly_allowance'])
weekly_allowance = "{:.2f}".format(row['monthly_allowance']/4)
st.write(f"Allowance: \${monthly_allowance} per month (about \${weekly_allowance} per week)")
st.write(f"Current Balance: \${row['current_balance']}")
st.write(f"Financial Goal: \${row['goal']}")
st.write(' ')
st.write(' ')


progress_percent = (row['current_balance'] / row['goal'])
if progress_percent == 1:
    st.balloons()
    statement = f"{row['first_name']} has achieved her goal!"
elif progress_percent > 1:
    st.balloons()
    statement = f"{row['first_name']} has exceeded her goal!"
else:
    statement = ''
    st.progress(progress_percent, text=str(round((progress_percent * 100))) + '%')

st.subheader(statement)

