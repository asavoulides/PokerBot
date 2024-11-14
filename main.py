import pyautogui
import random
import string
from PIL import Image
from screeninfo import get_monitors
import tempfile
import os
import api
import keyboard
from colorama import init, Fore, Style
import time
import threading
import sys
import platform

# Initialize colorama for colored output
init(autoreset=True)


def generate_random_filename(extension="png", length=10):
    """Generates a random filename with specified extension and length."""
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    return f"{random_string}.{extension}"


def capture_monitor_screenshot(monitor_index=1):
    # Get the list of monitors
    monitors = get_monitors()

    # Check if the specified monitor index is valid
    if monitor_index < 0 or monitor_index >= len(monitors):
        print(
            f"Invalid monitor index. Please choose between 0 and {len(monitors) - 1}."
        )
        return None

    # Get the specified monitor's dimensions
    monitor = monitors[monitor_index]
    left = monitor.x
    top = monitor.y
    width = monitor.width
    height = monitor.height

    # Capture the screenshot of the specified monitor region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Generate a randomized filename
    filename = generate_random_filename()

    # Get the temporary directory path
    temp_dir = "temp"
    file_path = os.path.join(temp_dir, filename)

    # Save the screenshot in the temporary directory
    screenshot.save(file_path)
    return file_path


def display_banner():
    """Displays the application banner."""
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
============================================
       Screenshot Capture & Upload Tool
============================================
Press 'F4' to capture and upload a screenshot.
Press 'Esc' to exit the program.
============================================
{Style.RESET_ALL}
"""
    print(banner.center(80))


def main():
    """Main function to capture a screenshot and handle the API response."""
    print(Fore.YELLOW + "Capturing screenshot...")

    screenshot_path = capture_monitor_screenshot()
    if not screenshot_path:
        print(Fore.RED + "Screenshot capture failed. Please try again.")
        return

    print(Fore.GREEN + "\nUploading screenshot...")
    try:
        # Extract decision and justification from the API response
        decisions = api.uploadImage(screenshot_path).split(";")
        decision = decisions[0].strip()
        justification = decisions[1].strip()

        # Define the width of the box
        box_width = 60

        # Generate the formatted output
        print(Fore.MAGENTA + "\n[Upload Result]")
        print(Fore.CYAN + "┌" + "─" * box_width + "┐")
        print(
            Fore.CYAN
            + f"│ {Fore.YELLOW}Decision      : {Fore.WHITE}{decision}".ljust(box_width)
            + " │"
        )
        print(Fore.CYAN + "├" + "─" * box_width + "┤")
        print(Fore.CYAN + f"│ {Fore.YELLOW}Justification :".ljust(box_width) + " │")

        # Wrap and print the justification text without extra lines
        wrapped_justification = wrap_text(justification, box_width - 2)
        for line in wrapped_justification:
            print(Fore.CYAN + f"│ {Fore.WHITE}{line}".ljust(box_width) + " │")

        print(Fore.CYAN + "├" + "─" * box_width + "┤")
        print(
            Fore.CYAN
            + f"│ {Fore.YELLOW}Time Taken    : {Fore.WHITE}{api.total_time:.2f} seconds".ljust(
                box_width
            )
            + " │"
        )
        print(Fore.CYAN + "└" + "─" * box_width + "┘\n")

    except Exception as e:
        print(Fore.RED + f"Error during upload: {str(e)}")


def wrap_text(text, width):
    """Wraps text to fit within a specified width without extra lines."""
    import textwrap

    wrapped_lines = textwrap.wrap(text, width)
    return [line.strip() for line in wrapped_lines if line.strip()]


if __name__ == "__main__":
    display_banner()
    while True:
        try:
            # Check for 'L' key press
            if keyboard.is_pressed("f4"):
                main()

            # Exit the program if 'Esc' is pressed
            if keyboard.is_pressed("esc"):
                print(Fore.RED + "Exiting... Goodbye!")
                break

        except KeyboardInterrupt:
            print(Fore.RED + "\nProgram interrupted manually.")
            break
