import io
import zipfile

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

st.set_page_config(
    page_title="PragyanAI - Image Processing Suite",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 PragyanAI - Image Processing Suite")
st.caption(
    "Blending • Background Change • Grayscale • Sketch • Pixelation • "
    "Resize • Multiple Images • Arithmetic • Noise • Combined Operations"
)


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
        "⬇️ Download Image",
        data=buffer.getvalue(),
        file_name=filename,
        mime="image/png"
    )


def blend_images(image1, image2, alpha):
    image2 = image2.resize(image1.size, Image.Resampling.LANCZOS)

    a1 = np.array(image1).astype(np.float32)
    a2 = np.array(image2).astype(np.float32)

    result = (a1 * (1 - alpha)) + (a2 * alpha)
    result = np.clip(result, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def change_background(image, color):
    image_bgr = pil_to_cv(image)
    height, width = image_bgr.shape[:2]

    mask = np.zeros((height, width), np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    rect = (
        int(width * 0.03),
        int(height * 0.03),
        int(width * 0.94),
        int(height * 0.94)
    )

    cv2.grabCut(
        image_bgr,
        mask,
        rect,
        bg_model,
        fg_model,
        5,
        cv2.GC_INIT_WITH_RECT
    )

    fg_mask = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype(np.uint8)

    background = np.zeros_like(np.array(image))
    background[:] = color

    alpha = fg_mask[:, :, None] / 255.0

    result = (
        np.array(image) * alpha +
        background * (1 - alpha)
    ).clip(0, 255).astype(np.uint8)

    return Image.fromarray(result)


def make_grayscale(image):
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

    a1 = np.array(image1).astype(np.int16)
    a2 = np.array(image2).astype(np.int16)

    if operation == "Addition":
        result = np.clip(a1 + a2, 0, 255)
    else:
        result = np.abs(a1 - a2)

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


def remove_text_area(image, x, y, width, height):
    image_bgr = pil_to_cv(image)

    mask = np.zeros(image_bgr.shape[:2], np.uint8)
    mask[y:y + height, x:x + width] = 255

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

st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload main image",
    type=["png", "jpg", "jpeg", "bmp", "webp"]
)

if uploaded_file is None:
    st.info("👈 Upload an image using the sidebar.")
    st.stop()

original = load_image(uploaded_file)

st.sidebar.success(f"Loaded: {uploaded_file.name}")
st.sidebar.caption(f"Size: {original.width} × {original.height} pixels")

operation = st.sidebar.radio(
    "Choose operation",
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

# ==============================
# 1. IMAGE BLENDING
# ==============================

if operation == "1. Image Blending":
    st.header("1. Image Blending")

    second_file = st.file_uploader(
        "Upload second image",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if second_file:
        second_image = load_image(second_file)

        alpha = st.slider("Second image opacity", 0.0, 1.0, 0.5, 0.05)

        result = blend_images(original, second_image, alpha)

        show_result(original, result, "Blended Image")
        download_image(result, "blended_image.png")

    else:
        st.info("Upload a second image.")

# ==============================
# 2. BACKGROUND CHANGE
# ==============================

elif operation == "2. Background Change":
    st.header("2. Background Change")

    color_hex = st.color_picker("New background color", "#00AEEF")

    color = tuple(
        int(color_hex.lstrip("#")[i:i + 2], 16)
        for i in (0, 2, 4)
    )

    if st.button("Change Background"):
        with st.spinner("Processing..."):
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

    result = make_grayscale(original)

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
        "Pixel block size",
        options=[8, 16, 32, 64],
        value=16
    )

    result = pixelate_image(original, block_size)

    show_result(original, result, f"Pixelated - {block_size}px")
    download_image(result, f"pixelated_{block_size}.png")

# ==============================
# 6. SHAPE AND SIZE
# ==============================

elif operation == "6. Image Shape and Size":
    st.header("6. Image Shape and Size")

    scale = st.select_slider(
        "Image size",
        options=[8, 16, 32, 64, 100, 150, 200],
        value=100
    )

    result = resize_image(original, scale)

    st.write(f"Original: {original.width} × {original.height} pixels")
    st.write(f"New: {result.width} × {result.height} pixels")

    show_result(original, result, f"Resized - {scale}%")
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
# 8. ARITHMETIC & TEXT REMOVAL
# ==============================

elif operation == "8. Addition, Subtraction & Text Removal":
    st.header("8. Addition, Subtraction & Text Removal")

    sub_operation = st.radio(
        "Choose operation",
        ["Image Addition", "Image Subtraction", "Delete Text / Object"],
        horizontal=True
    )

    if sub_operation in ["Image Addition", "Image Subtraction"]:
        second_file = st.file_uploader(
            "Upload second image",
            type=["png", "jpg", "jpeg", "bmp", "webp"],
            key="arithmetic"
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
        st.info(
            "Enter the area where the text or object is present. "
            "The app will fill that area using surrounding pixels."
        )

        col1, col2 = st.columns(2)

        with col1:
            x = st.number_input("X position", 0, original.width - 1, 50)

        with col2:
            y = st.number_input("Y position", 0, original.height - 1, 50)

        col3, col4 = st.columns(2)

        with col3:
            width = st.number_input(
                "Area width",
                1, original.width, 200
            )

        with col4:
            height = st.number_input(
                "Area height",
                1, original.height, 60
            )

        if st.button("Remove Text / Object"):
            try:
                result = remove_text_area(
                    original,
                    int(x),
                    int(y),
                    int(width),
                    int(height)
                )

                show_result(original, result, "Text Removed")
                download_image(result, "text_removed.png")

            except Exception as error:
                st.error(f"Text removal failed: {error}")

# ==============================
# 9. ADD NOISE
# ==============================

elif operation == "9. Add Noise":
    st.header("9. Add Noise")

    noise_type = st.selectbox(
        "Noise type",
        ["Gaussian Noise", "Salt & Pepper Noise"]
    )

    strength = st.slider("Noise strength", 1, 100, 20)

    if st.button("Apply Noise"):
        result = add_noise(original, noise_type, strength)

        show_result(original, result, "Noisy Image")
        download_image(result, "noisy_image.png")

# ==============================
# 10. MULTIPLE OPERATIONS
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
        result = make_grayscale(result)

    if sketch:
        result = make_sketch(result)

    if blur:
        result = result.filter(ImageFilter.GaussianBlur(radius=2))

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
