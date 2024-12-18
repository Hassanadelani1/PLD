
def format_text(text, color="white", bold=False):
    colors = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37"
    }
    bold_code = "1;" if bold else ""
    color_code = colors.get(color, "37")  # Default to white
    return f"\033[{bold_code}{color_code}m{text}\033[0m"