import streamlit as st
from multiapp import MultiApp
from apps import home # import your app modules here
import pandas as pd
import base64
from PIL import Image

st.set_page_config(page_title="SAS")
st.markdown("<h1 style='text-align: center; color: Black;'>SHOW AND SPEAK</h1>", unsafe_allow_html=True)


def home():
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('img.png')   
    
    def load_image(image_file):
    	img = Image.open(image_file)
    	return img

    
    st.markdown("<h5 style='text-align: center; color: Black;'>User interface to upload an image and get its spoken audio description.</h1>", unsafe_allow_html=True)
    
    
    
    image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    
    if image_file is not None:
        col1, col2, col3 = st.columns([1,6,1])
    
        with col1:
            st.write("")
        
        with col2:
            st.image(load_image(image_file),width=500)
        
        with col3:
            st.write("")
     
        with open(image_file.name,"wb") as f:
    	    f.write((image_file).getbuffer())
        fname=image_file.name[:-4]   
    
        path=f"C:/Users/srira/Desktop/presentation/output/audios/{fname}.wav"
        st.audio(path, format='audio/wav', start_time=0)


page_names_to_funcs = {
    "Home": home,
}

selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

# # Add all your application here
# app.add_app("Home", home.app)
# app.add_app("Evaluation", data.app)

# # The main app
# app.run()
