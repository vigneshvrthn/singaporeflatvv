# import required packages
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import requests


#creating the function for calling the csv file and the model
def load_model_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            model = pickle.loads(response.content)
            return model
        except pickle.UnpicklingError as e:
            raise Exception(f"Error unpickling the data: {e}")
    else:
        raise Exception(f"Failed to fetch file from URL. Status code: {response.status_code}")

def predict(model):
    pred_value = model.predict(a.loc[: ,list(a.columns)[:]])
    return pred_value



#reading the csv file
url = "https://raw.githubusercontent.com/vigneshvrthn/singaporeflatvv/main/finalfalt2.csv"



# Load the CSV file into a DataFrame
df = pd.read_csv(url)


#streamling app pagelayout and background and title
st.set_page_config(layout="wide")
st.title("FLAT RESALE VALUE")



# setting the background image
page_bg_img = '''
    <style>
    [data-testid=stAppViewContainer] {
        background-image: url(https://runwalgroup.in/blog/wp-content/uploads/2023/06/new-resale-flat.jpg);
        background-size: 100% 100%; /* Cover the entire container */
        background-repeat: no-repeat; /* Ensure background image doesn't repeat */
    }
    </style>
    '''
    
st.markdown(page_bg_img, unsafe_allow_html=True)

#by using the optionmenu creating the option to view as like the page
with st.sidebar:    
    select_fun=option_menu("Menu",["Price Prediction","Contact"])
if select_fun=="Price Prediction":
    cols = st.columns([2, 2, 2, 2, 2])  # Adjust the width of each column as needed

    # First column getting the input datas
    with cols[0]:
        st.markdown("<h5><span style='color:blue'>ENTER THE SELLING YEAR</span><h5>", unsafe_allow_html=True)
        selling_year=st.number_input("",value=2000,min_value=1990,max_value=2024)
        st.markdown("<h5><span style='color:blue'>ENTER THE SELLING MONTH</span><h5>", unsafe_allow_html=True)
        selling_month=st.number_input("",value=1,min_value=1,max_value=12)
        st.markdown("<h5><span style='color:blue'>ENTER THE LEASE COMMENCE DATE</span><h5>", unsafe_allow_html=True)
        lease_commence_date=st.number_input("",min_value=1973,max_value=2021)        
        
        
    
    # First column getting the input datas
    with cols[2]:
        st.markdown("<h5><span style='color:blue'>SELECT THE TOWN</span><h5>", unsafe_allow_html=True)
        town=st.selectbox("",df.town.unique())
        st.markdown("<h5><span style='color:blue'>ENTER THE SQM OF THE FALT</span><h5>", unsafe_allow_html=True)        
        floor_area_sqm=st.number_input("",min_value=53,max_value=173) 
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("") 
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")      
        but=st.button("Predict")     #creating the button

    # First column getting the input datas
    with cols[4]:
        st.markdown("""    <h5>        <span style='color:white; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;'>
            SELECT THE FALT TYPE        </span>    </h5>""", unsafe_allow_html=True)
        flat_type=st.selectbox("",df.flat_type.unique())
        st.markdown("<h5><span style='color:blue'>SELECT THE FALT MODEL</span><h5>", unsafe_allow_html=True)
        flat_model=st.selectbox("",df.flat_model.unique())
        st.markdown("""    <h5>        <span style='color:white; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;'>
            SELECT THE STOREY RANGE        </span>    </h5>""", unsafe_allow_html=True)
        floor=st.selectbox("",df.storey_range.unique())


    # by using the threshhold create the dict for the input data to save and impute the data for suitabe format
    
    if but: # by cliking the button to collect the input data and append in it dict
        a={"floor_area_sqm":[],"lease_commence_date":[],"town_code":[],"flat_type_code":[],
           "flat_model_code":[],"storey_range_code":[],"Selling_Year":[]}
        a["floor_area_sqm"].append(floor_area_sqm)
        a["lease_commence_date"].append(lease_commence_date)
        a["Selling_Year"].append(selling_year)
        town=df[df["town"]==town]["town_code"].iloc[0]
        a["town_code"].append(town)
        model_code=df[df["flat_model"]==flat_model]["flat_model_code"].iloc[0]
        a["flat_model_code"].append(model_code)
        type_code=df[df["flat_type"]==flat_type]["flat_type_code"].iloc[0]
        a["flat_type_code"].append(type_code)
        floor=df[df.storey_range==floor]["storey_range_code"].iloc[0]
        a["storey_range_code"].append(floor)
        a=pd.DataFrame(a)      #dict to dataframe 
        url = "https://raw.githubusercontent.com/vigneshvrthn/singaporeflatvv/main/resalevv"
        model = load_model_from_url(url)
        PRE=predict(model)         #calling the function to predict
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.markdown(f"""
    <h5 style='font-size: 20px;'>
        <span style='color: blue; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000; font-size: 50px;'>
            RESALE PRICE IS THE FLAT IS
        </span>
        <span style='color: red; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000; font-size: 50px;'>
            {round(PRE[0], 0)}
        </span>
    </h5>
""", unsafe_allow_html=True)
