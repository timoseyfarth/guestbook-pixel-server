import random
from io import BytesIO

import requests
from PIL import Image
from logger import logger

def get_dominant_color(avatar_url: str) -> str:
    """
    Downloads the avatar, resizes to 1x1 to get the average color,
    and returns a HEX string.
    """
    try:
        response = request_avatar(avatar_url)
        image = process_avatar(response)
        rgb = get_rgb_color(image)
        return convert_rgb_to_hex(rgb)
    except Exception as e:
        logger.error(f"Failed to get dominant color from {avatar_url}: {e}")
        raise ValueError(f"Failed to get dominant color: {e}")

def request_avatar(avatar_url: str) -> requests.Response:
    try:
        response = requests.get(avatar_url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise ValueError(f"Failed to download avatar image: {e}")

def process_avatar(response: requests.Response) -> Image.Image:
    try:
        img_data = BytesIO(response.content)
        avatar_image = Image.open(img_data)
        avatar_image = avatar_image.convert("RGB")

        avatar_image = avatar_image.resize((1, 1), resample=Image.Resampling.HAMMING)
        return avatar_image
    except Exception as e:
        raise ValueError(f"Failed to process avatar image: {e}")

def get_rgb_color(image: Image.Image) -> tuple[int, int, int]:
    r, g, b = image.getpixel((0, 0))
    return r, g, b

def convert_rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def get_random_hex() -> str:
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
