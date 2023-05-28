"""
ASCII Art Editor

This program is a graphical user interface (GUI) for an ASCII art editor.
It converts an image to ASCII text using a set of characters provided by the user.
The program allows the user to specify parameters such as image path, character image width and height,
font size, grayscale conversion method, and character set.
The conversion process involves comparing the original image with the character images to select
the best matching character for each position.
The GUI provides options to generate the ASCII art and save the generated text to a file.

The program is implemented using Python and the Tkinter library for GUI,
along with the Pillow and NumPy libraries for image manipulation and processing.

Author: Avanish Kumar Singh
Date: 28*-05-2023
Matriculation Number: 22200727
"""

import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
import numpy as np


class ASCIIArtEditor:
    """
    It defines a class ASCIIArtEditor that represents the main application.
    The code initializes the GUI elements and parameters, creates input and
    output elements, and defines callback functions for button actions.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Editor")

        # Default GUI parameters
        self.image_path = tk.StringVar(value="")
        self.char_width = tk.StringVar(value="10")
        self.char_height = tk.StringVar(value="10")
        self.font_size = tk.StringVar(value="12")
        self.grayscale_method = tk.StringVar(value="L")
        self.character_set = tk.StringVar(value="#@*+.: ")

        # Create GUI elements
        self.create_input_elements()
        self.create_output_elements()
        self.create_button_elements()

    def create_input_elements(self):
        """
        The create_input_elements method creates the input elements of the GUI, including labels,
        entry fields, and buttons for selecting image, specifying character width,
        height, font size, grayscale method, and character set.
        """
        # Image path entry
        tk.Label(self.root, text="Image Path:").grid(row=0, column=0, sticky="w")
        image_entry = tk.Entry(self.root, textvariable=self.image_path, width=50)
        image_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        tk.Button(self.root, text="Select Image", command=self.select_image).grid(row=0, column=3, padx=5, pady=5)

        # Character image width entry
        tk.Label(self.root, text="Character Width:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.char_width, width=10).grid(row=1, column=1, padx=5, pady=5)

        # Character image height entry
        tk.Label(self.root, text="Character Height:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.char_height, width=10).grid(row=2, column=1, padx=5, pady=5)

        # Font size entry
        tk.Label(self.root, text="Font Size:").grid(row=3, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.font_size, width=10).grid(row=3, column=1, padx=5, pady=5)

        # Grayscale method selection
        tk.Label(self.root, text="Grayscale Method:").grid(row=4, column=0, sticky="w")
        tk.Radiobutton(self.root, text="L (Lightness)", variable=self.grayscale_method, value="L").grid(row=4, column=1, sticky="w")
        tk.Radiobutton(self.root, text="R (Red)", variable=self.grayscale_method, value="R").grid(row=4, column=2, sticky="w")
        tk.Radiobutton(self.root, text="G (Green)", variable=self.grayscale_method, value="G").grid(row=4, column=3, sticky="w")
        tk.Radiobutton(self.root, text="B (Blue)", variable=self.grayscale_method, value="B").grid(row=4, column=4, sticky="w")

        # Character set entry
        tk.Label(self.root, text="Character Set:").grid(row=5, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.character_set, width=50).grid(row=5, column=1, columnspan=2, padx=5, pady=5)

    def create_output_elements(self):
        """
        The create_output_elements method creates the output elements of the GUI,
        including a text widget to display the generated ASCII art and scrollbars for scrolling through the text.
        """
        # Generated ASCII text display
        self.ascii_text = tk.Text(self.root, width=80, height=24, font=("Courier New", 10))
        self.ascii_text.grid(row=6, column=0, columnspan=5, padx=5, pady=5)

        # Scrollbars for ASCII text display
        scrollbar_y = tk.Scrollbar(self.root, command=self.ascii_text.yview)
        scrollbar_y.grid(row=6, column=5, sticky="ns")
        self.ascii_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(self.root, command=self.ascii_text.xview, orient="horizontal")
        scrollbar_x.grid(row=7, column=0, columnspan=5, sticky="we")
        self.ascii_text.configure(xscrollcommand=scrollbar_x.set)

    def create_button_elements(self):
        """
        The create_button_elements method creates the buttons for generating ASCII art and saving the text.
        """
        # Generate button
        tk.Button(self.root, text="Generate", command=self.generate_ascii).grid(row=8, column=0, padx=5, pady=5)

        # Save Text button
        tk.Button(self.root, text="Save Text", command=self.save_text).grid(row=8, column=1, padx=5, pady=5)

    def select_image(self):
        """
        The select_image method is a callback function for the "Select Image" button.
        It opens a file dialog to choose an image file and
        sets the selected file path in the image_path variable.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        self.image_path.set(file_path)

    def generate_ascii(self):
        """
        Callback function for the "Generate" button.
        Retrieves GUI parameters, loads and converts the image to grayscale,
        resizes it based on character dimensions, and converts it to a numpy array.
        Generates ASCII art by comparing character images with corresponding regions in the image,
        selects the character with the lowest distance, and displays the generated ASCII art.
        """
        # Retrieve GUI parameters
        image_path = self.image_path.get()
        char_width = int(self.char_width.get())
        char_height = int(self.char_height.get())
        font_size = int(self.font_size.get())
        grayscale_method = self.grayscale_method.get()
        character_set = self.character_set.get()

        # Load and convert image to grayscale
        image = Image.open(image_path).convert(grayscale_method)
        image_width, image_height = image.size

        # Calculate the number of characters needed in x and y direction
        num_chars_x = image_width // char_width
        num_chars_y = image_height // char_height

        # Resize image to match the calculated number of characters
        image = image.resize((num_chars_x * char_width, num_chars_y * char_height))

        # Convert image to numpy array
        image_array = np.array(image)

        # Generate ASCII text
        ascii_text = ""
        for y in range(0, num_chars_y):
            for x in range(0, num_chars_x):
                # Crop the image to character size
                crop = image_array[y * char_height: (y + 1) * char_height, x * char_width: (x + 1) * char_width]

                # Calculate distances between the cropped image and characters in the character set
                distances = []
                for char in character_set:
                    char_image = self.generate_character_image(char, char_width, char_height, font_size)
                    distance = np.linalg.norm(char_image - crop)
                    distances.append(distance)

                # Select the character with the lowest distance
                min_distance_index = np.argmin(distances)
                selected_char = character_set[min_distance_index]
                ascii_text += selected_char

            ascii_text += "\n"

        # Display generated ASCII text
        self.ascii_text.delete("1.0", "end")
        self.ascii_text.insert("end", ascii_text)

    def generate_character_image(self, char, width, height, font_size):
        """
        Generates an image for a given character using specified width, height, and font size.
        Creates a new PIL image, draws the character using the specified font,
        and returns the image as a numpy array.
        """
        image = Image.new("L", (width, height), color=255)
        image_draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", font_size)

        text_width, text_height = image_draw.textsize(char, font=font)
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        image_draw.text((x, y), char, font=font, fill=0)

        return np.array(image)

    def save_text(self):
        """
        The start method starts the main event loop of the GUI window
        """
        text = self.ascii_text.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                file.write(text)

    def start(self):
        """
        Create the Tkinter window (root).
        Initialize an instance of ASCIIArtEditor with the window as an argument.
        Start the GUI application.
        """
        self.root.mainloop()


# Create the GUI window
root = tk.Tk()

# Create the ASCII Art Editor instance
ascii_editor = ASCIIArtEditor(root)

# Start the GUI application
ascii_editor.start()
