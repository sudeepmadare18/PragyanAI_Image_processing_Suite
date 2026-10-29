# 🖼️ Image Processing Suite

### A Web-Based Image Processing Application Using Python, Streamlit, Pillow, NumPy & OpenCV

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![NumPy](https://img.shields.io/badge/Library-NumPy-013243.svg)](https://numpy.org/)
[![OpenCV](https://img.shields.io/badge/Library-OpenCV-5C3EE8.svg)](https://opencv.org/)
[![Pillow](https://img.shields.io/badge/Library-Pillow-3776AB.svg)](https://python-pillow.org/)

**PixelCraft Image Processing Studio** is an interactive web application developed using Python and Streamlit. It allows users to upload images, apply various image processing operations, compare original and processed images, and download the results. The application uses Pillow, NumPy, and OpenCV to provide image transformation and enhancement features through a simple, user-friendly interface.

## 🌐 Live Demo

🚀 **Try the application online:**

👉 [Launch PixelCraft Image Processing Studio](https://pragyanaiimagestudioclass-dad7mgztbfjlmvqxnemx6p.streamlit.app/)

*Replace `YOUR_STREAMLIT_APP_URL` with your actual deployed Streamlit application URL.*

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Supported Image Formats](#-supported-image-formats)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [How to Run](#-how-to-run)
- [How to Use](#-how-to-use)
- [Application Workflow](#-application-workflow)
- [Use Cases](#-use-cases)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)
- [Author](#-author)
  
## 📖 Overview

Image processing is widely used in digital photography, computer vision, image enhancement, and visual computing. However, performing different image processing operations may require programming knowledge or multiple editing tools.

PixelCraft Image Processing Studio addresses this challenge by providing a single web-based interface for performing common image processing tasks. Users can upload images, select an operation, preview the results, and download processed images without writing image processing code themselves.

The project is designed for students, beginners, and developers who want to learn and experiment with practical image processing techniques using Python.

## ✨ Features

### 🖼️ Image Upload and Preview
- Upload images in supported formats.
- Preview original images before processing.
- Compare original and processed images side by side.

### 🎨 Image Transformation
- Convert color images to grayscale.
- Convert images to black and white using thresholding.
- Apply pencil sketch effects.
- Blend multiple images.
- Resize images to selected dimensions.
- Create pixelated image effects.

### 🔍 Image Enhancement
- Apply sharpening filters.
- Apply Gaussian blur.
- Add noise to images.
- Perform image addition and subtraction.

### 🗂️ Multiple Image Processing
- Display multiple images in a gallery.
- Apply multiple image processing operations.
- Download processed images.
- Package multiple outputs into a ZIP archive where supported.

### ⚙️ Interactive Interface
- Select operations using sidebar navigation.
- Adjust available processing parameters.
- View processed results directly in the browser.
- Download processed images in PNG format.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application interface |
| Pillow (PIL) | Image loading, conversion, resizing, and saving |
| NumPy | Array manipulation and pixel-level calculations |
| OpenCV | Image filtering, thresholding, and image arithmetic |
| `io` | In-memory image processing and download buffers |
| `zipfile` | Creating ZIP archives for multiple outputs |

## 🗃️ Supported Image Formats

The application is configured to support these input formats:

- PNG
- JPG
- JPEG
- WEBP
- BMP

Processed images can be downloaded in PNG format.

## 📂 Project Structure

```text
PixelCraft-Image-Processing-Studio/
│
├── app.py
├── requirements.txt
└── README.md


    
```

**File descriptions:**

- `app.py` — Main Streamlit application containing the interface and image processing logic.
- `requirements.txt` — Python dependencies required to run the project.
- `README.md` — Project documentation.



## 🚀 Installation and Setup

### Prerequisites

Install the following software before running the project:

- Python 3.10 or a compatible version.
- Git.
- A modern web browser.
- Visual Studio Code or another code editor (optional).

### Step 1: Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd PixelCraft-Image-Processing-Studio
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```text
streamlit
pillow
numpy
opencv-python-headless
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

Open this address in your browser to use PixelCraft Image Processing Studio.

## 🧑‍💻 How to Use

1. Open the application.
2. Upload an image using the image upload control.
3. Select an image processing operation from the sidebar.
4. Adjust the available settings, if applicable.
5. View the original and processed images.
6. Download the processed image or generated output when the relevant option is available.

## 🔄 Application Workflow

```text
       Upload Image
            |
            v
      Select Operation
            |
            v
     Process the Image
   (Pillow / NumPy / OpenCV)
            |
            v
      Display the Result
            |
            v
     Compare and Download
```

The application uses Pillow for image handling, NumPy for array operations, OpenCV for image processing, and Streamlit for the interactive interface.

## 🎯 Use Cases

- Learning fundamental image processing concepts.
- Demonstrating image transformations in academic projects.
- Experimenting with grayscale conversion and thresholding.
- Exploring image enhancement and filtering.
- Comparing original and processed images.
- Understanding practical applications of Python image processing libraries.

## 🔮 Future Enhancements

- AI-powered background removal.
- Edge detection using Sobel and Laplacian filters.
- Advanced noise reduction and image restoration.
- Batch image processing with ZIP downloads.
- Additional image resizing interpolation methods.
- More output formats and adjustable image quality.
- Improved input validation and error handling.
- Online deployment for wider access.

## 🐛 Troubleshooting

### Streamlit command not found

Install Streamlit in the active Python environment:

```bash
python -m pip install streamlit
```

### ModuleNotFoundError

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

### Application does not start

Ensure you are in the project directory and that `app.py` exists. Then run:

```bash
python -m streamlit run app.py
```

### Image upload or processing error

Check that the image uses a supported format and is a valid image file. If the issue persists, try another image.

## 👨‍💻 Author

**Sudeep S**

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) — Web application framework.
- [Pillow](https://python-pillow.org/) — Image handling and manipulation.
- [NumPy](https://numpy.org/) — Numerical computing.
- [OpenCV](https://opencv.org/) — Computer vision and image processing.

---

⭐ If you find this project useful, consider starring the repository on GitHub.
