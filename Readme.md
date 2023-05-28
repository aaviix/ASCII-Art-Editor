ASCII Art Editor

This is a Python application that allows you to create ASCII art from an image using a graphical user interface (GUI). The application utilizes the Tkinter library for the GUI components and the PIL library for image processing.
1. Author: _Avanish Kumar Singh_
2. Date: 28-05-2023
3. Matriculation Number: _22200727_

Features
1. Select an image file from your local system.
2. Specify the character width, height, font size, grayscale method, and character set for generating ASCII art.
3. View the generated ASCII art in a text display area.
4. Scroll through the ASCII art using scrollbars.
5. Generate ASCII art by comparing each character image in the character set with the corresponding region in the image and selecting the character with the lowest distance.
6. Save the generated ASCII art as a text file.

Requirements
1. Python 3.x
2. Tkinter
3. PIL (Python Imaging Library)
4. numpy

How to Use
1. Ensure that you have Python installed on your system.
2. Install the necessary libraries by running the following command:
```
pip install pillow numpy
```
3. Save the provided code in a file with a .py extension, for example, ascii_art_editor.py.
4. Run the script by executing the following command:
```
python ascii_art_editor.py
```
5. The GUI window will appear.
6. Use the provided input elements to select an image, specify the desired parameters, and generate ASCII art.
7. The generated ASCII art will be displayed in the text area.
8. Use the scrollbars to navigate through the ASCII art.
9. Click the "Save Text" button to save the ASCII art as a text file.

```
Note: The application currently supports image file types including .jpg, .jpeg, .png, .gif, and .bmp.
```

Acknowledgements

This application is based on the ASCIIArtEditor class, which was developed using the Tkinter library, threading module, PIL (Python Imaging Library), and numpy library.

License

This code is licensed under the **MIT License**.
