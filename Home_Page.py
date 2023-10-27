import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Piggy Bank",
    page_icon='🐷',
    layout='wide'
)

page_bg = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url('https://marketplace.canva.com/EAFC908rtPY/1/0/1600w/canva-purple-and-peach-rainbow-waves-desktop-wallpaper-afsazXR5vWo.jpg');
background-size: cover;
}
</style>
'''

st.title("Welcome to Piggy Bank")

