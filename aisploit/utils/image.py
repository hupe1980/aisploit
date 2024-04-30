import base64
import imghdr
import io

import cv2
import numpy as np
from PIL import Image


def display_base64_image_in_notebook(base64_image):
    from IPython.display import display

    base64_bytes = base64_image.encode("ascii")
    image_bytes = base64.b64decode(base64_bytes)
    image = Image.open(io.BytesIO(image_bytes))
    display(image)


def detect_image_mimetype(image_data: str | bytes) -> str | None:
    if isinstance(image_data, str):
        # Decode base64 string into bytes
        image_data = base64.b64decode(image_data)

    # Detect the image type from bytes
    image_type = imghdr.what(None, h=image_data)

    # Map image type to MIME type
    mime_types = {
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
    }

    # Get the corresponding MIME type
    mime_type = None
    if image_type:
        mime_type = mime_types.get(image_type)

    return mime_type


def image_to_data_url(image_data: str | bytes) -> str:
    if isinstance(image_data, bytes):
        image_data = base64.b64encode(image_data).decode('utf-8')

    mime_type = detect_image_mimetype(image_data)

    return f"data:{mime_type};base64,{image_data}"


def to_cv2_image(image_data: str | bytes) -> cv2.typing.MatLike:
    if isinstance(image_data, str):
        # Decode base64 string into bytes
        image_data = base64.b64decode(image_data)

    # Convert bytes to numpy array
    np_array = np.frombuffer(image_data, np.uint8)

    # Decode numpy array into image
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)


def embed_prompt_in_image(image_data: str | bytes, prompt: str, return_base64: bool = False) -> str | bytes:
    # Load the image
    image = to_cv2_image(image_data)

    # Define the font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    # Split the text into multiple lines
    lines = prompt.split('\n')

    # Calculate the size of the text for positioning
    text_size = cv2.getTextSize(prompt, font, font_scale, font_thickness)[0]

    # Calculate the starting y-coordinate for the text
    text_y = (image.shape[0] + text_size[1] * len(lines)) // 2

    # Draw each line of text on the image
    for i, line in enumerate(lines):
        text_x = (image.shape[1] - cv2.getTextSize(line, font, font_scale, font_thickness)[0][0]) // 2
        cv2.putText(image, line, (text_x, text_y + i * text_size[1]), font, font_scale, (255, 255, 255), font_thickness)

    success, encoded_image = cv2.imencode('.png', image)

    # Check if encoding was successful
    if not success:
        raise Exception("Failed to encode image to bytes")

    # Return the modified image
    image_bytes = encoded_image.tobytes()

    if return_base64:
        return base64.b64encode(image_bytes).decode('utf-8')

    return image_bytes
