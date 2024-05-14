import streamlit as st
import os
import cv2
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.edge_detect.edge_detector import detect_edges
from src.edge_detect.contours_manipulator import *
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import logging
import pandas as pd

from src.utils.unscale_points import unscale_points
import numpy as np
from src.area_select.inference import get_temp_from_poly


def pil_to_cv2(pil_image):
    """
    Convert a PIL (Python Imaging Library) image to an OpenCV image.

    This function takes an image in PIL format, converts it to RGB mode, 
    then converts it to a numpy array, and finally changes the color format 
    from RGB to BGR to be compatible with OpenCV functions.

    Parameters:
    pil_image (PIL.Image.Image): The input image in PIL format.

    Returns:
    numpy.ndarray: The converted image in OpenCV (BGR) format.
    """
    # Convert PIL image to RGB format
    pil_image = pil_image.convert('RGB')

    # Convert PIL image to numpy array
    numpy_image = np.array(pil_image)

    # Convert RGB to BGR (OpenCV format)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    return opencv_image


def select_folder() -> UploadedFile | None:
    """
    Handle the file upload process using Streamlit.

    This function initializes a session state variable to store the uploaded 
    files if it doesn't exist, provides a file uploader widget for the user 
    to upload files, and stores the uploaded files in the session state.

    Returns:
    UploadedFile or None: The uploaded file(s), if any.
    """
    # Initialize session state variable for uploaded files if not already done
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = None

    # Create a file uploader widget for the user to upload files
    uploaded_files: UploadedFile | None = st.file_uploader("Upload files",
                                                           type=[
                                                               "png", "jpeg", "jpg"],
                                                           help="Supported file types: png, jpeg, jpg",
                                                           accept_multiple_files=False)

    # Store the uploaded files in the session state
    st.session_state["uploaded_files"] = uploaded_files
    print(uploaded_files)

    return st.session_state["uploaded_files"]


def display_image_and_edges(path):
    """
    Display an image and its edges (Canny) using the given file path.

    This function opens an image from the provided file path, converts it 
    to OpenCV format, and detects its edges.

    Parameters:
    path (str): The file path of the image.

    Returns:
    tuple: A tuple containing the original image in OpenCV format and the edges detected.
    """
    # Open the image from the given file path using PIL
    image = Image.open(path)

    # Convert the PIL image to OpenCV format
    image = pil_to_cv2(image)

    # Detect edges in the image
    edges = detect_edges(image)

    return image, edges


def clear_cache():
    st.session_state["outer_hist"] = []
    st.session_state["points"] = []


def display_interactive_image(image, edge, min_temp: float, max_temp: float, mode=0, width=600., height_ratio=1.15, image_path=None):
    """
    Display an interactive image with edge detection and contour highlighting.

    This function allows users to interact with an image using Streamlit. Depending on the mode,
    users can draw points on the image to form a polygon or highlight contours based on edges.

    Parameters:
    image (numpy.ndarray): The input image in OpenCV format (BGR).
    edge (numpy.ndarray): The edge-detected image.
    min_temp (float): Minimum temperature value for RGB to temperature conversion.
    max_temp (float): Maximum temperature value for RGB to temperature conversion.
    mode (int): Mode of operation. 0 for contour highlighting, 1 for polygon drawing.
    width (float): Width of the displayed image.
    height_ratio (float): Height-to-width ratio of the displayed image.
    image_path (str): Path to the image file (required for mode 1).

    Returns:
    tuple: Average RGB temperature and the number of selected points or contours.
    """
    def apply_ui(closest_outer, contours, inners, highlighted_image):
        """
        Apply UI changes based on the closest outer contour.

        This function updates the session state and highlights the selected contours.

        Parameters:
        closest_outer (int): Index of the closest outer contour.
        contours (list): List of contours.
        inners (list): List of inner contours indices.
        highlighted_image (numpy.ndarray): Image to draw contours on.
        """
        if closest_outer in st.session_state["outer_hist"]:
            st.session_state["outer_hist"].remove(closest_outer)
            cv2.drawContours(highlighted_image, [
                             contours[i] for i in inners], -1, (0, 255, 0), 1)
            cv2.drawContours(highlighted_image, [
                             contours[closest_outer]], -1, (0, 255, 0), 1)
            logging.info("No average")
        else:
            st.session_state["outer_hist"].append(closest_outer)
            cv2.drawContours(highlighted_image, [
                             contours[i] for i in inners], -1, (255, 0, 0), 1)
            cv2.drawContours(highlighted_image, [
                             contours[closest_outer]], -1, (255, 0, 0), 1)

    avg_rgb_text = 0

    if mode == 1:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            point_radius = 3

            for point in st.session_state["points"]:
                draw.ellipse((point[0] - point_radius, point[1] - point_radius,
                              point[0] + point_radius, point[1] + point_radius), fill='blue')

            if len(st.session_state["points"]) >= 3:
                logging.info(st.session_state["points"])
                avg_rgb_text = get_temp_from_poly(
                    image, st.session_state["points"], max_temp=max_temp, min_temp=min_temp)
                draw.polygon(st.session_state["points"], fill=(0, 255, 0, 128))

            value = streamlit_image_coordinates(img, key="pil")

            if value is not None:
                point = value["x"], value["y"]
                if point not in st.session_state["points"]:
                    st.session_state["points"].append(point)
                    st.rerun()

            st.write(
                f"Ave: {avg_rgb_text} N-selection: {len(st.session_state['outer_hist'])}")

    elif mode == 0:
        contours, hierarchy = cv2.findContours(
            edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        highlighted_image = image.copy()

        cv2.drawContours(highlighted_image, contours, -1, (0, 255, 0), 1)
        for point in st.session_state["points"]:
            logging.info(f"{point=}")
            x, y = unscale_points(
                point, width, (image.shape[1], image.shape[0]), height_ratio=height_ratio)
            closest_outer = find_closest_outer_contour(contours, x, y)
            inners = find_closest_inner_contour(hierarchy, closest_outer)
            logging.info(f"{point},{closest_outer},{inners}")

            apply_ui(closest_outer, contours, inners, highlighted_image)

            avg_rgb_text = aggregate_rgb_values(image.copy(
            ), contours, hierarchy, st.session_state["outer_hist"], float(min_temp), float(max_temp))
            logging.info(f"Ave: {avg_rgb_text} N-selection: {len(
                st.session_state['outer_hist'])} Outer Hist: {st.session_state['outer_hist']}")

        value = streamlit_image_coordinates(cv2.cvtColor(
            highlighted_image, cv2.COLOR_BGR2RGB), width=width, height=width * height_ratio)

        if value is not None:
            point = value["x"], value["y"]
            st.session_state["points"].append(point)
            logging.info(f"{st.session_state['points']=}")
            st.rerun()

        st.write(f"Ave: {avg_rgb_text} N-selection: {
                 len(st.session_state['points'])} Outer Hist: {st.session_state['outer_hist']}")

    return avg_rgb_text, len(st.session_state["outer_hist"])


def launch_thermo_images():
    """
    Launch the thermo image processing interface using Streamlit.

    This function provides a user interface for uploading thermal images, 
    setting temperature ranges, selecting image processing modes, and 
    displaying the original and processed images. Users can interactively 
    select regions or contours on the images.

    Returns:
    tuple: Filename, maximum temperature, minimum temperature, average temperature, 
    and count of selected regions or contours.
    """
    # Input fields for temperature range
    max_temp = st.number_input("Max Temp:", key="max_temp", value=41.6)
    min_temp = st.number_input("Min Temp:", key="min_temp", value=22.6)

    # Radio buttons for selection mode
    selection_mode = st.radio("Select the mode:",
                              ["Multi-Region", "Simple Area"],
                              key="selection_mode",
                              horizontal=True,
                              on_change=clear_cache)

    avg = count = 0

    st.write('Asset Directory:')

    # File uploader for selecting images
    filename = select_folder()

    if filename:
        # Create tabs for region selector and edge/original image display
        first_tab1, first_tab2 = st.tabs(
            ["Region Selector", "Edge and Original"])

        # Display the image and its edges
        image, edges = display_image_and_edges(filename)

        with first_tab1:
            # Display interactive image based on the selected mode
            avg, count = display_interactive_image(image, edges, min_temp=min_temp, max_temp=max_temp,
                                                   mode=(
                                                       0 if selection_mode != "Simple Area" else 1),
                                                   image_path=filename)

        with first_tab2:
            # Display original and edge-detected images side by side
            col1, col2 = st.columns(2)

            with col1:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                st.image(rgb_image, caption='Original Image',
                         use_column_width=True)

            with col2:
                st.image(edges, caption='Edge Detected Image',
                         use_column_width=True)

    # Return the results
    return (filename.name if filename else None), max_temp, min_temp, avg, count


def render_story_tab():
    if "points" not in st.session_state:
        st.session_state["points"] = []
    if "outer_hist" not in st.session_state:
        st.session_state["outer_hist"] = []
    st.write("THermOs")
    st.subheader("Home")

    filename, max_temp, min_temp, avg, count = launch_thermo_images()

    clear = st.button("Clear", key="clear")

    if clear:
        clear_cache()
    if avg > 0 and min_temp and max_temp:
        with st.form("tempr_form"):
            st.write("Write to record")
            title = st.text_input(label="title:", key="title_form",
                                  # type: ignore
                                  value=os.path.basename(filename))
            st.number_input("Selected Average:", key="ave_form",
                            format="%.5f", value=avg, step=1.)
            st.text_input("file name", key="file_form",
                          value=os.path.basename(filename,), disabled=True)
            st.number_input("Min temp:", key="min_temp_form",
                            value=min_temp, disabled=True)
            st.number_input("Max temp:", key="max_temp_form",
                            value=max_temp, disabled=True)
            st.number_input("Number of region:",
                            key="n_region_form", value=count, disabled=True)
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
                    temp_df = pd.concat(
                        [st.session_state['data'], new_row_df], ignore_index=True)

                    # Only check the last row
                    if not temp_df.duplicated().iloc[-1]:
                        st.session_state['data'] = temp_df
                        st.write("Done!!")
                    else:
                        st.error("Duplicate entry. The row was not added.")
