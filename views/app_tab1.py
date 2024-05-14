import streamlit as st
import os
import cv2
from src.edge_detect.edge_detector import detect_edges
from src.edge_detect.contours_manipulator import *
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import logging 
import pandas as pd
from streamlit_file_browser import st_file_browser
from src.utils.unscale_points import unscale_points
import numpy as np
from src.area_select.inference import get_temp_from_poly
def pil_to_cv2(pil_image):
    # Convert PIL image to RGB format
    pil_image = pil_image.convert('RGB')
    # Convert PIL image to numpy array
    numpy_image = np.array(pil_image)
    # Convert RGB to BGR (OpenCV format)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return opencv_image


def file_selector(filenames):
    # filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    image = Image.open(selected_filename)
    st.image(Image.open(filenames[0]))
    st.image(pil_to_cv2(image))

    return selected_filename
def select_folder():
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"]=None
        
    uploaded_files = st.file_uploader("Upload files",type=["png","jpeg","jpg"],help="Supported file types:png, jpeg, jpg",accept_multiple_files=False)

    st.session_state["uploaded_files"]=uploaded_files
    # st.write(st.session_state["uploaded_files"])
    print(uploaded_files)

    return st.session_state["uploaded_files"]
    # st.file_uploader("Uploda")
def display_image_and_edges(path):
    image = Image.open(path)
    image = pil_to_cv2(image)
    edges = detect_edges(image)

    return image,edges
def clear_cache():
    st.session_state["outer_hist"]=[]
    st.session_state["points"]=[]

def display_interactive_image(image,edge,min_temp,max_temp,mode=0,width=600,height_ratio=1.15,image_path=None):
    def apply_ui(closest_outer):
        if closest_outer in st.session_state["outer_hist"]:
                st.session_state["outer_hist"].remove(closest_outer)
                cv2.drawContours(highlighted_image,[contours[i] for i in inners], -1, (0, 255, 0), 1) 
                cv2.drawContours(highlighted_image, [contours[closest_outer]], -1, (0, 255, 0), 1) 
                print("no average")
        else:
                st.session_state["outer_hist"].append(closest_outer)
                cv2.drawContours(highlighted_image,[contours[i] for i in inners], -1, (255, 0, 0), 1) 
                cv2.drawContours(highlighted_image, [contours[closest_outer]], -1, (255, 0, 0), 1) 
    avg_rgb_text=0
    if mode == 1:
            
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)

            # Draw an ellipse at each coordinate in points
            point_radius=3
            
            for point in st.session_state["points"]:
                 draw.ellipse((point[0] - point_radius, point[1] - point_radius, 
                      point[0] + point_radius, point[1] + point_radius), fill='blue')
    
            if len( st.session_state["points"]) >= 3:
                # Define a semi-transparent green (R, G, B, A)
                print(st.session_state["points"])
                avg_rgb_text = get_temp_from_poly(image,st.session_state["points"],max_temp=max_temp,min_temp=min_temp)
                draw.polygon( st.session_state["points"], fill=(0, 255, 0, 128))

            value = streamlit_image_coordinates(img, key="pil")

            if value is not None:
                point = value["x"], value["y"]

                if point not in st.session_state["points"]:
                    st.session_state["points"].append(point)
                    value=None
                    st.rerun()
            st.write(f"Ave:{avg_rgb_text} N-selection:{len( st.session_state['outer_hist'])} ")
            
            
      


    elif mode==0:
        contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        highlighted_image = image.copy()

        cv2.drawContours(highlighted_image, contours, -1, (0, 255, 0), 1) 
        for point in st.session_state["points"]:
            logging.info(f"{point=}")
            
            x,y = unscale_points(point,width,(image.shape[1],image.shape[0]),height_ratio=height_ratio)
            closest_outer=find_closest_outer_contour(contours,x,y)
            inners =find_closest_inner_contour(hierarchy,closest_outer)

            logging.info(f"{point},{closest_outer},{inners}")
            
            apply_ui(closest_outer)
            
            avg_rgb_text = aggregate_rgb_values(image.copy(),contours,hierarchy, st.session_state["outer_hist"],float(min_temp),float(max_temp))
            logging.info(f"Ave:{avg_rgb_text} N-selection:{len( st.session_state['outer_hist'])} Outer Hist:{st.session_state['outer_hist']}")
            
            # st.session_state["points"]=None

        value = streamlit_image_coordinates(
            cv2.cvtColor(highlighted_image, cv2.COLOR_BGR2RGB),
            width=width,
            height=width*height_ratio
            # key="pil",
        )
        # st.write(st.session_state["points"])
        if value is not None:
            point = value["x"], value["y"]


            # if point not in st.session_state["points"]:
            st.session_state["points"].append(point)
            logging.info(f"{st.session_state['points']=}")
            st.rerun()
        st.write(f"Ave:{avg_rgb_text} N-selection:{len( st.session_state['points'])} Outer Hist:{st.session_state['outer_hist']}")
                
    
    return avg_rgb_text,len( st.session_state["outer_hist"])
def launch_thermo_images():
    max_temp = st.number_input("Max Temp: \n\n",key="max_temp",value=41.6)
    min_temp = st.number_input("Min Temp: \n\n",key="min_temp",value=22.6)
    selection_mode = st.radio("Select the lmode \n\n",["Multi-Region", "Simple Area"],key="selection_mode",horizontal=True,on_change=clear_cache)
    avg=count =0

    st.write('Asset Directory:')
    # clicked = st.button('Dir Picker')
    # if clicked:
        # dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
    # dirname = st.text_input('Selected folder:')
    # folder_select_button = st.button("Select Folder")
    filename = None
    # if folder_select_button:
    filename = select_folder()
    # st.write(selected_folder_path)
    if filename:
        
        # filename = file_selector(slected_files)
        first_tab1, first_tab2 = st.tabs(["Region Selector", "Edge and Original"])
        image,edges = display_image_and_edges(filename)

        with first_tab1:
            avg,count = display_interactive_image(image,edges,min_temp=min_temp,max_temp=max_temp,mode=(0 if selection_mode!="Simple Area" else 1),
                                                  image_path=filename)
        with first_tab2:
            col1, col2 = st.columns(2)

            with col1:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                st.image(rgb_image, caption='Original Image', use_column_width=True)
            with col2:
                st.image(edges, caption='Edge Detected Image', use_column_width=True)
    return (filename.name if filename else None), max_temp,min_temp,avg,count 
                



# function to render the story tab, and call the model, and display the model prompt and response.
def render_story_tab ():
    if "points" not in st.session_state:
        st.session_state["points"] = []
    if "outer_hist" not in st.session_state:
        st.session_state["outer_hist"]=[]
    st.write("THermOs")
    st.subheader("Home")

    filename, max_temp,min_temp,avg,count =launch_thermo_images()


    clear = st.button("Clear", key="clear")

    if clear:
        clear_cache()
    if avg>0 and min_temp and max_temp:
        with st.form("tempr_form"):
            st.write("Write to record")
            title = st.text_input("title:",key="title_form",value=os.path.basename(filename))
            st.number_input("Selected Average:",key="ave_form",format="%.5f",value=avg,step=1.)
            st.text_input("file name",key="file_form",value=os.path.basename(filename,),disabled=True)
            st.number_input("Min temp:",key="min_temp_form",value=min_temp,disabled=True)
            st.number_input("Max temp:",key="max_temp_form",value=max_temp,disabled=True)
            st.number_input("Number of region:",key="n_region_form",value=count,disabled=True)
            submitted = st.form_submit_button("Add Record")
            if submitted:
                if title.strip() == "":  # Check if the title is empty or only contains whitespace
                    st.error("The title field is required.")
                else:
                    new_row = {
                        "title": title,
                        "max_temp": float(max_temp),
                        "min_temp": float(min_temp),
                        "selected_average": float(avg),
                        "n_regions": int(count),
                        "filename": os.path.basename(filename)
                    }
                    new_row_df = pd.DataFrame([new_row])
                    # Append the new row to the existing DataFrame using pd.concat
                    temp_df = pd.concat([st.session_state['data'], new_row_df], ignore_index=True)
            
                    if not temp_df.duplicated().iloc[-1]:  # Only check the last row
                        st.session_state['data'] = temp_df
                        st.write("Done!!")
                    else:
                        st.error("Duplicate entry. The row was not added.")


