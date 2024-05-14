
# ThermoImageProcessor

## Overview

ThermoImageProcessor is a Streamlit-based application designed to calculate the temperature of areas of interest in thermal images. Users can upload thermal images, set temperature ranges, select regions, and save their analysis. The application provides two modes for region selection: "Multi-Region" and "Simple Area."

## Features

- **Image Upload**: Users can upload images in PNG, JPEG, and JPG formats.
- **Temperature Range**: Users can set minimum and maximum temperatures for the analysis.
- **Mode Selection**: Users can choose between "Multi-Region" and "Simple Area" modes for region selection.
  - **Multi-Region**: Utilizes edge detection combined with dilation for enhanced edge visibility, allowing users to select multiple regions.
  - **Simple Area**: Allows users to draw polygons to select areas and estimate the temperature.
- **Color Palette**: The temperature color palette is computed using minimum and maximum temperatures and a list of hex colors defined in `color_pallet.py`.
- **Record Management**: Users can save records of their analysis to the session, modify and delete records, and download them as CSV files.
- **Future Versions**: Custom color palettes and Google Drive linkage are planned for future releases.

## Installation

To run the ThermoImageProcessor, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/u6747075/thermo-calc-web.git
   cd thermo-calc-web.
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```sh
   streamlit run app.py      \
     --browser.serverAddress=localhost \
     --server.enableCORS=false \
     --server.enableXsrfProtection=false \
     --server.port 8080
   ```

## Usage

### Upload Image

- Upload an image in PNG, JPEG, or JPG format using the file uploader.

### Set Temperature Range

- Set the minimum and maximum temperatures using the input fields.

### Select Mode

- Choose one of the two modes:
  - **Multi-Region**: Select regions based on edge detection.
  - **Simple Area**: Draw a polygon to select the area.

### Save Record

- After analysis, save the record to the session. Manage records in the Records tab, where you can modify, delete, and download them as CSV files.

## Edge Detection Algorithm

The edge detection algorithm uses Canny edge detection combined with dilation to enhance edge visibility.

### Canny Edge Detection

The Canny edge detection algorithm is a multi-stage process to detect a wide range of edges in images. It involves the following steps:

1. **Noise Reduction**: The image is first smoothed using a Gaussian filter to reduce noise. This step helps in minimizing false edges caused by noise.

    ```python
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    ```

2. **Gradient Calculation**: The gradient intensity and direction are calculated using Sobel operators. This step helps in identifying areas of rapid intensity change which correspond to edges.

3. **Non-Maximum Suppression**: This step removes spurious responses to edge detection by preserving all local maxima in the gradient image while discarding everything else. This process results in thin edges.

4. **Double Thresholding**: This step classifies edges into strong, weak, and non-relevant pixels using two thresholds. Strong edges are edges that are definitely edges, weak edges are edges that are possibly edges, and non-relevant pixels are discarded.

5. **Edge Tracking by Hysteresis**: Weak edges are included in the final edge image if and only if they are connected to strong edges. This step helps in suppressing noise while preserving true edges.

    ```python
    edges = cv2.Canny(blurred, 55, 100)
    ```

6. **Dilation**: After detecting edges using the Canny algorithm, dilation is applied to enhance the edges, making them more prominent and easier to work with for region selection.

    ```python
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    ```

### Complete Edge Detection Code

```python
def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 55, 100)
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    return dilated_edges
```

### Research Papers

- **Canny Edge Detection**:
  - Canny, J. (1986). A computational approach to edge detection. IEEE Transactions on Pattern Analysis and Machine Intelligence, 8(6), 679-698. [Link](https://ieeexplore.ieee.org/document/4767851)
- **Dilation for Edge Enhancement**:
  - Serra, J. (1982). Image Analysis and Mathematical Morphology. Academic Press, Inc. [Link](https://www.sciencedirect.com/book/9780126372400/image-analysis-and-mathematical-morphology)

## Future Versions

- **Custom Color Palettes**: Ability to define and use custom color palettes for temperature visualization.
- **Google Drive Linkage**: Integration with Google Drive for saving and retrieving records.

## Contributing

We welcome contributions to improve ThermoImageProcessor! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
