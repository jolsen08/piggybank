import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Piggy Bank | Your Children",
    page_icon='🐷',
    layout='wide'
)

df = pd.read_csv("piggy_bank_table.csv")
df['birth_date'] = df['birth_date'].astype(str)

col1, col2 = st.columns([.6,.2])

with col2:
    child_info = st.empty()

    with child_info.expander("Add a New Child"):
        with st.form("New Child Info"):
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            gender = st.selectbox("Gender",['','Male','Female'])
            birth_date = st.date_input("Birth Date", value=None)
            monthly_allowance = st.number_input("Allowance per Month", step=1., format="%.2f")
            goal = st.number_input("Financial Goal", step=1., format="%.2f")
            submit = st.form_submit_button("Submit")
            if submit and first_name is not None and last_name is not None and first_name != '' and last_name != '':
                new_row = {'first_name': first_name, 'last_name': last_name, 'gender': gender, 'birth_date': birth_date, 'monthly_allowance': monthly_allowance, 'current_balance': 0, 'goal': goal}
                df = df.append(new_row, ignore_index=True)
                df.to_csv('piggy_bank_table.csv')

df['birth_date'] = df['birth_date'].astype(str)
with col1:
    st.subheader('Your Current Children')
    st.write('---')
    for index, row in df.iterrows():
        col1, col2, col3 = st.columns(3)
        with col1:
            current_date = datetime.now()
            birth_date = datetime.strptime(row['birth_date'], '%Y-%m-%d')
            monthly_allowance = "{:.2f}".format(row['monthly_allowance'])
            weekly_allowance = "{:.2f}".format(row['monthly_allowance']/4)
            age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            st.write(f"Name: {row['first_name']}")
            st.write(f"Age: {age}")
            st.write(f"Allowance: \${monthly_allowance} per month (about \${weekly_allowance} per week)")
            st.write(f"Current Balance: \${row['current_balance']}")
            st.write(f"Financial Goal: \${row['goal']}")
        with col2:
            if row['gender'] is not None and row['gender'] != '':
                if row['gender'].lower() == 'male':
                    st.image('https://static.vecteezy.com/system/resources/previews/024/044/218/original/kids-clipart-transparent-background-free-png.png', width=150)
                elif row['gender'].lower() == 'female':
                    st.image('https://cdn.pixabay.com/photo/2013/07/13/12/38/girl-160006_1280.png', width=150)
        with col3:
            monthly_payment = st.button("Pay Monthly Allowance", key=f"{index} - monthly")
            weekly_payment = st.button("Pay Weekly Allowance", key=f"{index} - weekly")
            custom_payment = st.expander("Custom")
            if custom_payment:
                custom = st.number_input("Custom Payment", step=1., format="%.2f", key=f"{index} - custom_value")
                custom_submit = st.button("Submit Payment",  key=f"{index} - custom")
                if custom_submit:
                    df.at[index, 'current_balance'] += float(custom)
                    df.to_csv("piggy_bank_table.csv", index=False)
                    st.rerun()
            if monthly_payment:
                df.at[index, 'current_balance'] += float(monthly_allowance)
                df.to_csv("piggy_bank_table.csv", index=False)
                st.rerun()
            if weekly_payment:
                df.at[index, 'current_balance'] += float(weekly_allowance)
                df.to_csv("piggy_bank_table.csv", index=False)
                st.rerun()

            df.to_csv("piggy_bank_table.csv", index=False)
            
        st.write("---")



