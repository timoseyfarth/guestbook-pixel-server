import math

from better_profanity import profanity

from models import GuestbookEntry
from logger import logger

PIXEL_SIZE = 15
PIXEL_GAP = 2
PIXEL_COLUMNS = 30
FRAME_PADDING = 6

profanity.load_censor_words()

def gen_and_save_svg(users: list[GuestbookEntry], svg_output: str) -> str:
    try:
        svg = generate_svg(users)

        with open(svg_output, "w", encoding="utf-8") as f:
            f.write(svg)
        logger.info(f"SVG successfully generated and saved to {svg_output}")
        return "SVG was successfully generated! "
    except Exception as e:
        logger.error(f"Error generating SVG: {e}", exc_info=True)
        return f"Error generating SVG... Try again later. "


def generate_svg(users: list[GuestbookEntry]) -> str:
    total_users = len(users)
    rows = math.ceil(total_users / PIXEL_COLUMNS)
    rows = max(rows, 1)

    grid_width = (PIXEL_COLUMNS * (PIXEL_SIZE + PIXEL_GAP)) - PIXEL_GAP
    grid_height = (rows * (PIXEL_SIZE + PIXEL_GAP)) - PIXEL_GAP

    frame_width = grid_width + (2 * FRAME_PADDING)
    frame_height = grid_height + (2 * FRAME_PADDING)

    svg_content = f"""
    <svg width="100%" height="100%" viewBox="0 0 {frame_width} {frame_height}" 
    xmlns="http://www.w3.org/2000/svg" version="1.1">
        <rect width="{frame_width}" height="{frame_height}" fill="white" rx="8" />
        
        <rect x="2" y="2" width="{frame_width - 4}" height="{frame_height - 4}" 
              fill="none" stroke="#f0f0f0" stroke-width="1" rx="6" />

        <g transform="translate({FRAME_PADDING}, {FRAME_PADDING})">
    """
    for index, user in enumerate(users):
        col = index % PIXEL_COLUMNS
        row = index // PIXEL_COLUMNS
        x = col * (PIXEL_SIZE + PIXEL_GAP)
        y = row * (PIXEL_SIZE + PIXEL_GAP)

        username = sanitize_input(user.username)
        tooltip = get_tooltip(user)

        if user.is_anonymous:
            svg_content += f"""
                    <rect x="{x}" y="{y}" width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" 
                            fill="{user.avatar_hex}" stroke="#2e2e2e" stroke-width="0.8" rx="2">
                        <title>{tooltip}</title>
                    </rect>
                    """
        else:
            svg_content += f"""
                    <a href="https://github.com/{username}" target="_blank">
                        <rect x="{x}" y="{y}" width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" 
                              fill="{user.avatar_hex}" stroke="#2e2e2e" stroke-width="0.8" rx="2">
                            <title>{tooltip}</title>
                        </rect>
                    </a>
                    """

    svg_content += "</g> </svg>"
    return svg_content

def get_tooltip(user: GuestbookEntry) -> str:
    username = sanitize_input(user.username)
    if user.is_anonymous:
        username = "Anonymous"
    else:
        username = f"@{username}"

    if user.quote:
        quote = sanitize_input(user.quote)
        quote = profanity_filter(quote)
        return f"{username} said: {quote}"
    else:
        return f"{username}"

def sanitize_input(input_str: str) -> str:
    """
    Sanitizes input string to prevent XSS attacks.
    This is a simple implementation; consider using a library for production use.
    """
    if not input_str:
        return ""
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
        "/": "&#x2F;",
    }
    for old, new in replacements.items():
        input_str = input_str.replace(old, new)
    return input_str

def profanity_filter(input_str: str) -> str:
    if not input_str:
        return ""
    return profanity.censor(input_str)
