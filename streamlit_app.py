import streamlit as st
import time
import psutil
import random
import os
import sys
from PIL import Image, ImageDraw, ImageOps
from PIL.Image import Resampling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from os.path import exists

st.set_page_config(page_title="🎈 App Screenshot")
st.title('🎈 App Screenshot')
st.warning('An app for taking screenshot of a Streamlit app.')

#@st.cache_resource
def get_driver():
    options = webdriver.ChromeOptions()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(f"--window-size={width}x{height}")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    return webdriver.Chrome(service=service, options=options)

def get_scrape_html(app_url):
    driver = get_driver()
    if app_url.endswith('streamlit.app'):
        driver.get(f"{app_url}/~/+/")
    else:
        driver.get(app_url)
            
    time.sleep(3)
            
    # Explicitly wait for an essential element to ensure content is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
    # Get scroll height and width
    #scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    #scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            
    # Set window size
    #driver.set_window_size(scroll_width, scroll_height)
            
    # Now, capture the screenshot
    # driver.save_screenshot('screenshot.png')
    return driver.page_source


# Settings
with st.sidebar:
    st.header('⚙️ Settings')

    st.subheader('Image Resolution')
        
    # Getting % usage of virtual_memory ( 3rd field)
    ram_usage = psutil.virtual_memory()[2]
    st.caption(f'RAM used (%): {ram_usage}')

# Input URL
with st.form("my_form"):
    app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').rstrip('/')
    app_name = app_url.replace('https://','').replace('.streamlit.app','')
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        if app_url:
            st.write(get_scrape_html(app_url))







file_exists = exists('screenshot.png')
if file_exists:
    with open("final.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"{app_name}.png",
            mime="image/png"
            )
        if btn:
            os.remove('screenshot.png')
            os.remove('final.png')


