import pandas as pd
import numpy as np
import streamlit as st
import pickle
import time

df = pd.read_csv('final_dataset.csv')
df.drop(['Unnamed: 0', 'price'], axis='columns', inplace=True)
#print(len(df.columns))
title = "Home Price Prediction".upper()
st.title(title)

st.subheader('We will predict the price of your **Dream House** in BENGALURU by just entering the following details!!!')

with open('prediction_model.pickle', 'rb') as f :
    model = pickle.load(f)

def take_inputs() :
    location = [i[9:] for i in df.columns[3:]]
    location.insert(0, '')
    st.write('\n\n')
    loc = st.selectbox('Choose a location', location)
    st.write('\n')
    sqft = st.number_input('Enter the Total Square Feet Area')
    st.write('\n')
    bath = st.slider('Select the number of bathrooms', min_value=1, max_value=10)
    st.write('\n')
    bhk = st.slider('Select BHK', min_value=1, max_value=10)
    print(sqft, loc, bath, bhk)
    st.write('\n\t\t')
    pred = st.button('PREDICT')
    if pred :
        if loc and sqft > 100.0 and bath < bhk + 2 and bhk < bath + 3:
            st.write('\n')
            st.write('### Your input values :')
            d = {'Location' : loc, 'Total Square Feet Area' : sqft, 'Bathrooms' : bath, 'BHK' : bhk}
            in_df = pd.DataFrame(d, index=[0])
            st.write(in_df)
            st.write('\n')
            with st.spinner('Predicting...'):
                time.sleep(5)
                st.write('\n')
                return predict_price(loc, sqft, bath, bhk)
        else :
            if sqft <= 100.0 :
                st.error('Total Square Feet field must be greater than 100!')    
            if not loc :
                st.error('Location field is not selected. Please check!')
            if bath >= bhk + 2 or bhk >= bath + 3:
                st.error('Invalid data!!')

def predict_price(location, sqft, bath, bhk) :
    loc = 'location_' + location
    loc_index = np.where(df.columns == loc)[0][0]
    lst = np.zeros(len(df.columns))
    lst[0] = sqft
    lst[1] = bath
    lst[2] = bhk
    if loc_index > 2 :
        lst[loc_index] = 1
    print(len(lst))
    price = model.predict([lst])[0]
    st.write('\n')
    if price < 10 :
        price = 10
    st.info(f'''
        Predicted price of your **Dream House** in {location} having {sqft} sqft, {bhk} BHK and {bath} bathroom/s is 
        **{round(price, 2)} Lakh INR**
        ''')

take_inputs()
