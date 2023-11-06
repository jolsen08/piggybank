import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Piggy Bank | Your Children",
    page_icon='🐷',
    layout='wide'
)

if 'child_data' not in st.session_state:
    st.session_state.child_data = pd.read_csv("piggy_bank_table.csv")
    st.session_state.child_data['birth_date'] = st.session_state.child_data['birth_date'].astype(str)

if 'editing_child' not in st.session_state:
    st.session_state.editing_child = None

col1, col2 = st.columns([.6, .2])

with col2:
    child_info = st.empty()

    with child_info.expander("Add a New Child"):
        with st.form("New Child Info"):
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            gender = st.selectbox("Gender", ['', 'Male', 'Female'])
            birth_date = st.date_input("Birth Date", value=None)
            monthly_allowance = st.number_input("Allowance per Month", step=1., format="%.2f")
            goal = st.number_input("Financial Goal", step=1., format="%.2f")
            submit = st.form_submit_button("Submit")
            if submit and first_name is not None and last_name is not None and first_name != '' and last_name != '':
                new_row = {'first_name': first_name, 'last_name': last_name, 'gender': gender, 'birth_date': birth_date,
                           'monthly_allowance': monthly_allowance, 'current_balance': 0, 'goal': goal}
                st.session_state.child_data = st.session_state.child_data.append(new_row, ignore_index=True)
                st.session_state.child_data.to_csv('piggy_bank_table.csv', index=False)

with col1:
    st.subheader('Your Current Children')
    st.write('---')
    for index, row in st.session_state.child_data.iterrows():
        col1, col2, col3 = st.columns(3)
        with col1:
            current_date = datetime.now()
            birth_date = datetime.strptime(row['birth_date'], '%Y-%m-%d')
            monthly_allowance = "{:.2f}".format(row['monthly_allowance'])
            weekly_allowance = "{:.2f}".format(row['monthly_allowance'] / 4)
            age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (
            birth_date.month, birth_date.day))
            st.write(f"Name: {row['first_name']}")
            st.write(f"Age: {age}")
            st.write(f"Allowance: \${monthly_allowance} per month (about \${weekly_allowance} per week)")
            st.write(f"Current Balance: \${row['current_balance']}")
            st.write(f"Financial Goal: \${row['goal']}")

            if st.button(f"Edit {row['first_name']}", key=f"{index} - edit"):
                st.session_state.editing_child = index

            if st.session_state.editing_child == index:
                new_monthly_allowance = st.number_input("Edit Allowance per Month", value=row['monthly_allowance'], step=1., format="%.2f")
                new_goal = st.number_input("Edit Financial Goal", value=row['goal'], step=1., format="%.2f")
                if st.button("Save Edit"):
                    st.session_state.child_data.at[index, 'monthly_allowance'] = new_monthly_allowance
                    st.session_state.child_data.at[index, 'goal'] = new_goal
                    st.session_state.child_data.to_csv("piggy_bank_table.csv", index=False)
                    st.session_state.editing_child = -1
                    st.rerun()

        with col2:
            if row['gender'] is not None and row['gender'] != '':
                if row['gender'].lower() == 'male':
                    st.image(
                        'https://static.vecteezy.com/system/resources/previews/024/044/218/original/kids-clipart-transparent-background-free-png.png',
                        width=150)
                elif row['gender'].lower() == 'female':
                    st.image(
                        'https://cdn.pixabay.com/photo/2013/07/13/12/38/girl-160006_1280.png',
                        width=150)
        with col3:
            monthly_payment = st.button("Pay Monthly Allowance", key=f"{index} - monthly")
            weekly_payment = st.button("Pay Weekly Allowance", key=f"{index} - weekly")
            custom_payment = st.expander("Custom")

            if custom_payment:
                custom = st.number_input("Custom Payment", step=1., format="%.2f", key=f"{index} - custom_value")
                custom_submit = st.button("Submit Payment", key=f"{index} - custom")
                if custom_submit:
                    st.session_state.child_data.at[index, 'current_balance'] += float(custom)
                    st.session_state.child_data.to_csv("piggy_bank_table.csv", index=False)
            if monthly_payment:
                st.session_state.child_data.at[index, 'current_balance'] += float(monthly_allowance)
                st.session_state.child_data.to_csv("piggy_bank_table.csv", index=False)
            if weekly_payment:
                st.session_state.child_data.at[index, 'current_balance'] += float(weekly_allowance)
                st.session_state.child_data.to_csv("piggy_bank_table.csv", index=False)

        st.write("---")
