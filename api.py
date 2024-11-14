import base64
from openai import OpenAI
import time
import threading
import sys

client = OpenAI()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

with open("prompt.txt", "r") as file:
    prompt = file.read()

# Function to encode the image
def uploadImage(image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Stopwatch function
    def stopwatch():
        global total_time
        start_time = time.time()
        while not stop_event.is_set():
            elapsed_time = time.time() - start_time
            sys.stdout.write(f"\rStopwatch: {elapsed_time:.2f} seconds")
            sys.stdout.flush()
            time.sleep(0.1)
        # Record the total time once the stopwatch stops
        total_time = time.time() - start_time

    # Create an event to stop the stopwatch thread
    stop_event = threading.Event()
    # Start the stopwatch thread
    stopwatch_thread = threading.Thread(target=stopwatch)
    stopwatch_thread.start()

    # API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    # Stop the stopwatch thread
    stop_event.set()
    stopwatch_thread.join()

    # Clear the line and print the response
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()
    return response.choices[0].message.content


if __name__ == "__main__":
    # Initialize the total_time variable
    total_time = 0
    response = uploadImage(
        "C:\\Users\\alexa\\OneDrive\\Desktop\\Folders\\Scripts\\Python\\PokerBot\\dr8Tw0fdSm.png"
    )
    print(f"Total Time Taken: {total_time:.2f} seconds")
