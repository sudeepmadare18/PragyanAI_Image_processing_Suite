import io
import zipfile

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from streamlit_drawable_canvas import st_canvas

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="PragyanAI - Image Processing Suite",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 PragyanAI - Image Processing Suite")
st.caption(
    "Blending • Background Change • Grayscale • Sketch • Pixelation • "
    "Resize • Multiple Images • Arithmetic & Text Removal • Noise • Combined Operations"
)

st.markdown(
    """
    Upload an image and choose an operation from the sidebar.  
    Apply image-processing techniques, preview the result, and download the output.
    """
)

# ==============================
# SESSION STATE
# ==============================

if "original_image" not in st.session_state:
    st.session_state.original_image = None

if "original_name" not in st.session_state:
    st.session_state.original_name = "image.png"

# ==============================
# HELPER FUNCTIONS
# ==============================

def load_image(file):
    return Image.open(file).convert("RGB")


def pil_to_cv(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def cv_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def show_result(original, result, title):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(original, use_container_width=True)

    with col2:
        st.subheader(title)
        st.image(result, use_container_width=True)


def download_image(image, filename):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    st.download_button(
        label="⬇️ Download Processed Image",
        data=buffer.getvalue(),
        file_name=filename,
        mime="image/png"
    )


def blend_images(image1, image2, alpha):
    image2 = image2.resize(image1.size, Image.Resampling.LANCZOS)

    array1 = np.array(image1).astype(np.float32)
    array2 = np.array(image2).astype(np.float32)

    blended = (array1 * (1 - alpha)) + (array2 * alpha)
    blended = np.clip(blended, 0, 255).astype(np.uint8)

    return Image.fromarray(blended)


def change_background(image, color):
    image_bgr = pil_to_cv(image)
    height, width = image_bgr.shape[:2]

    mask = np.zeros((height, width), np.uint8)

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    rectangle = (
        int(width * 0.03),
        int(height * 0.03),
        int(width * 0.94),
        int(height * 0.94)
    )

    cv2.grabCut(
        image_bgr,
        mask,
        rectangle,
        background_model,
        foreground_model,
        5,
        cv2.GC_INIT_WITH_RECT
    )

    foreground_mask = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype(np.uint8)

    background = np.zeros_like(np.array(image))
    background[:] = color

    alpha = foreground_mask[:, :, None] / 255.0

    result = (
        np.array(image) * alpha +
        background * (1 - alpha)
    ).clip(0, 255).astype(np.uint8)

    return Image.fromarray(result)


def convert_grayscale(image):
    return image.convert("L").convert("RGB")


def make_sketch(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blurred

    sketch = cv2.divide(gray, inverted_blur, scale=256)

    return Image.fromarray(sketch).convert("RGB")


def pixelate_image(image, block_size):
    width, height = image.size

    small = image.resize(
        (
            max(1, width // block_size),
            max(1, height // block_size)
        ),
        Image.Resampling.NEAREST
    )

    return small.resize(
        (width, height),
        Image.Resampling.NEAREST
    )


def resize_image(image, scale):
    new_width = max(1, int(image.width * scale / 100))
    new_height = max(1, int(image.height * scale / 100))

    return image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )


def image_arithmetic(image1, image2, operation):
    image2 = image2.resize(image1.size, Image.Resampling.LANCZOS)

    array1 = np.array(image1).astype(np.int16)
    array2 = np.array(image2).astype(np.int16)

    if operation == "Addition":
        result = np.clip(array1 + array2, 0, 255)
    else:
        result = np.abs(array1 - array2)

    return Image.fromarray(result.astype(np.uint8))


def add_noise(image, noise_type, strength):
    array = np.array(image).astype(np.float32)

    if noise_type == "Gaussian Noise":
        noise = np.random.normal(0, strength, array.shape)
        noisy = array + noise

    else:
        noisy = array.copy()
        probability = min(strength / 100, 0.5)

        random_map = np.random.random(array.shape[:2])

        noisy[random_map < probability / 2] = 0
        noisy[random_map > 1 - probability / 2] = 255

    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    return Image.fromarray(noisy)


def remove_text(image, mask):
    image_bgr = pil_to_cv(image)

    mask = cv2.dilate(
        mask,
        np.ones((3, 3), np.uint8),
        iterations=2
    )

    result_bgr = cv2.inpaint(
        image_bgr,
        mask,
        5,
        cv2.INPAINT_TELEA
    )

    return cv_to_pil(result_bgr)


# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("⚙️ Image Processing Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload main image",
    type=["png", "jpg", "jpeg", "bmp", "webp"]
)

if uploaded_file is not None:
    st.session_state.original_image = load_image(uploaded_file)
    st.session_state.original_name = uploaded_file.name

if st.session_state.original_image is None:
    st.info("👈 Upload an image using the sidebar to begin.")
    st.stop()

original = st.session_state.original_image

st.sidebar.success(f"Loaded: {st.session_state.original_name}")
st.sidebar.caption(f"Size: {original.width} × {original.height} pixels")

operation = st.sidebar.radio(
    "Choose an operation",
    [
        "1. Image Blending",
        "2. Background Change",
        "3. Grayscale Conversion",
        "4. Pencil Sketch",
        "5. Image Pixelation",
        "6. Image Shape and Size",
        "7. Multiple Images",
        "8. Addition, Subtraction & Text Removal",
        "9. Add Noise",
        "10. Multiple Image Operations"
    ]
)

st.sidebar.divider()
st.sidebar.caption("PragyanAI - Image Processing Suite")

# ==============================
# 1. IMAGE BLENDING
# ==============================

if operation == "1. Image Blending":
    st.header("1. Image Blending")

    second_file = st.file_uploader(
        "Upload second image",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
        key="blend_upload"
    )

    if second_file:
        second_image = load_image(second_file)

        alpha = st.slider(
            "Second image opacity",
            0.0, 1.0, 0.5, 0.05
        )

        result = blend_images(original, second_image, alpha)

        show_result(original, result, "Blended Image")
        download_image(result, "blended_image.png")

    else:
        st.info("Upload a second image to blend.")

# ==============================
# 2. BACKGROUND CHANGE
# ==============================

elif operation == "2. Background Change":
    st.header("2. Background Change")

    color_hex = st.color_picker(
        "Choose new background color",
        "#00AEEF"
    )

    color = tuple(
        int(color_hex.lstrip("#")[i:i + 2], 16)
        for i in (0, 2, 4)
    )

    if st.button("Change Background"):
        with st.spinner("Processing background..."):
            try:
                result = change_background(original, color)

                show_result(original, result, "New Background")
                download_image(result, "background_changed.png")

            except Exception as error:
                st.error(f"Background change failed: {error}")

# ==============================
# 3. GRAYSCALE
# ==============================

elif operation == "3. Grayscale Conversion":
    st.header("3. Color to Black & White")

    result = convert_grayscale(original)

    show_result(original, result, "Grayscale Image")
    download_image(result, "grayscale_image.png")

# ==============================
# 4. PENCIL SKETCH
# ==============================

elif operation == "4. Pencil Sketch":
    st.header("4. Color to Pencil Sketch")

    result = make_sketch(original)

    show_result(original, result, "Pencil Sketch")
    download_image(result, "pencil_sketch.png")

# ==============================
# 5. PIXELATION
# ==============================

elif operation == "5. Image Pixelation":
    st.header("5. Image Pixel Size")

    block_size = st.select_slider(
        "Select pixel block size",
        options=[8, 16, 32, 64],
        value=16
    )

    result = pixelate_image(original, block_size)

    show_result(original, result, f"Pixelated Image - {block_size}px")
    download_image(result, f"pixelated_{block_size}.png")

# ==============================
# 6. SHAPE AND SIZE
# ==============================

elif operation == "6. Image Shape and Size":
    st.header("6. Image Shape and Size")

    st.info(
        "This changes the image dimensions using a selected scale percentage."
    )

    scale = st.select_slider(
        "Select image size",
        options=[8, 16, 32, 64, 100, 150, 200],
        value=100
    )

    result = resize_image(original, scale)

    st.write(
        f"Original size: **{original.width} × {original.height}** pixels"
    )
    st.write(
        f"New size: **{result.width} × {result.height}** pixels"
    )

    show_result(original, result, f"Resized Image - {scale}%")
    download_image(result, f"resized_{scale}.png")

# ==============================
# 7. MULTIPLE IMAGES
# ==============================

elif operation == "7. Multiple Images":
    st.header("7. Multiple Images")

    files = st.file_uploader(
        "Upload multiple images",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
        accept_multiple_files=True
    )

    if files:
        st.success(f"Uploaded {len(files)} image(s).")

        columns = st.columns(3)

        for index, file in enumerate(files):
            try:
                image = load_image(file)

                with columns[index % 3]:
                    st.image(
                        image,
                        caption=file.name,
                        use_container_width=True
                    )

            except Exception:
                st.warning(f"Could not load {file.name}")

        if st.button("Prepare ZIP Download"):
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(
                zip_buffer,
                "w",
                zipfile.ZIP_DEFLATED
            ) as archive:

                for file in files:
                    try:
                        image = load_image(file)
                        buffer = io.BytesIO()
                        image.save(buffer, format="PNG")

                        name = file.name.rsplit(".", 1)[0] + ".png"
                        archive.writestr(name, buffer.getvalue())

                    except Exception:
                        pass

            st.download_button(
                "⬇️ Download All Images as ZIP",
                data=zip_buffer.getvalue(),
                file_name="multiple_images.zip",
                mime="application/zip"
            )

    else:
        st.info("Upload one or more images.")

# ==============================
# 8. ADDITION, SUBTRACTION & TEXT REMOVAL
# ==============================

elif operation == "8. Addition, Subtraction & Text Removal":
    st.header("8. Image Addition, Subtraction & Text Removal")

    sub_operation = st.radio(
        "Choose operation",
        ["Image Addition", "Image Subtraction", "Delete Text / Object"],
        horizontal=True
    )

    if sub_operation in ["Image Addition", "Image Subtraction"]:
        second_file = st.file_uploader(
            "Upload second image",
            type=["png", "jpg", "jpeg", "bmp", "webp"],
            key="arithmetic_upload"
        )

        if second_file:
            second_image = load_image(second_file)

            result = image_arithmetic(
                original,
                second_image,
                sub_operation.replace("Image ", "")
            )

            show_result(original, result, sub_operation)
            download_image(
                result,
                sub_operation.lower().replace(" ", "_") + ".png"
            )

        else:
            st.info("Upload a second image.")

    else:
        st.write(
            "Paint over the text or object you want to remove, then click remove."
        )

        max_width = 700
        max_height = 600

        scale = min(
            max_width / original.width,
            max_height / original.height,
            1.0
        )

        canvas_width = int(original.width * scale)
        canvas_height = int(original.height * scale)

        canvas_background = original.resize(
            (canvas_width, canvas_height),
            Image.Resampling.LANCZOS
        )

        brush_size = st.slider(
            "Brush size",
            3, 60, 18
        )

        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 1.0)",
            stroke_width=brush_size,
            stroke_color="#FF0000",
            background_image=canvas_background,
            update_streamlit=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode="freedraw",
            return_image_data=True,
            key="text_removal_canvas"
        )

        if st.button("Remove Marked Text / Object"):
            if canvas_result.image_data is None:
                st.error("Please paint over the text first.")

            else:
                canvas_array = np.asarray(canvas_result.image_data)

                red = canvas_array[:, :, 0].astype(np.int16)
                green = canvas_array[:, :, 1].astype(np.int16)
                blue = canvas_array[:, :, 2].astype(np.int16)

                small_mask = np.where(
                    (red > 100) &
                    (red > green * 1.25) &
                    (red > blue * 1.25),
                    255,
                    0
                ).astype(np.uint8)

                full_mask = cv2.resize(
                    small_mask,
                    (original.width, original.height),
                    interpolation=cv2.INTER_NEAREST
                )

                if cv2.countNonZero(full_mask) == 0:
                    st.error("No marked area detected. Paint again.")

                else:
                    result = remove_text(original, full_mask)

                    show_result(
                        original,
                        result,
                        "Text / Object Removed"
                    )

                    download_image(
                        result,
                        "text_removed.png"
                    )

# ==============================
# 9. ADD NOISE
# ==============================

elif operation == "9. Add Noise":
    st.header("9. Add Noise to Image")

    noise_type = st.selectbox(
        "Noise type",
        ["Gaussian Noise", "Salt & Pepper Noise"]
    )

    strength = st.slider(
        "Noise strength",
        1, 100, 20
    )

    if st.button("Apply Noise"):
        result = add_noise(original, noise_type, strength)

        show_result(original, result, "Noisy Image")
        download_image(result, "noisy_image.png")

# ==============================
# 10. MULTIPLE IMAGE OPERATIONS
# ==============================

elif operation == "10. Multiple Image Operations":
    st.header("10. Multiple Image Operations")

    grayscale = st.checkbox("Grayscale")
    sketch = st.checkbox("Pencil Sketch")
    blur = st.checkbox("Gaussian Blur")
    sharpen = st.checkbox("Sharpen")
    invert = st.checkbox("Invert Colors")
    pixelate = st.checkbox("Pixelate")

    result = original.copy()

    if grayscale:
        result = convert_grayscale(result)

    if sketch:
        result = make_sketch(result)

    if blur:
        result = result.filter(
            ImageFilter.GaussianBlur(radius=2)
        )

    if sharpen:
        result = ImageEnhance.Sharpness(result).enhance(2.0)

    if invert:
        result = Image.fromarray(
            (255 - np.array(result)).astype(np.uint8)
        )

    if pixelate:
        result = pixelate_image(result, 16)

    show_result(original, result, "Combined Output")
    download_image(result, "multiple_operations.png")
