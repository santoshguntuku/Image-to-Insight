🗓️ Week 1: The Digital Canvas

Focus: Python Setup & Image Manipulation

Goal: Understand how computers "see" images as matrices and how to manipulate them using Python.

🧠 Theoretical Framework

An image is not just a picture; it is a 3-dimensional matrix of numbers (Height, Width, Color Channels). Before we can read text from a meme, we must pre-process it. Optical Character Recognition (OCR) engines struggle with noise, color artifacts, and massive file sizes.

• Grayscaling: Converts a 3-channel (RGB) image into a 1-channel image, simplifying the data.

• Resizing: Standardizes the input so our AI models run faster.

📚 Learning Resources

• Python Basics (Video):(https://learn.microsoft.com/en-us/shows/intro-to-python-development/)

• Google Colab Guide:(https://www.marqo.ai/blog/getting-started-with-google-colab-a-beginners-guide)

• Pillow (PIL) Documentation:(https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)

• Image Coordinates: GeeksForGeeks Pillow Guide

🧪 Weekly Schedule

• Mon-Tue: Watch the Python & Colab tutorials. Set up your environment.

• Wed-Thu: Experiment with PIL.Image.open(), .crop(), and .resize().

• Fri-Sun: Complete the assignments below.

✅ Assignments

Assignment 1.1: The Setup

Create a setup.py or .ipynb file. Write a script that imports PIL, loads an image from your computer, and displays it. This confirms your environment is ready.

Assignment 1.2: The Pre-processor

Write a function process_meme(image_path) that performs the following pipeline:

1. Opens an image file.
2. Prints its original dimensions (Width, Height).
3. Converts it to Grayscale (.convert('L')).
4. Resizes it to 50% of the original scale.
5. Saves the result as processed_week1.jpg.

Submission: Upload your code and the processed_week1.jpg to your repository's Week_1 folder.
