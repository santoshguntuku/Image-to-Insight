🗓️ Week 2: Machine Vision (OCR)

Focus: Optical Character Recognition with EasyOCR

Goal: Extract raw string data from pixel data.

🧠 Theoretical Framework

OCR is a probabilistic pipeline consisting of Text Detection (finding where the text is) and Text Recognition (identifying the characters). We are using EasyOCR, a Deep Learning library that utilizes ResNet (for feature extraction) and LSTMs (for sequence prediction).

GPU vs CPU: You will notice that OCR is slow on a standard CPU. We will use Google Colab's T4 GPU runtime to speed this up by 10x-20x.

Confidence Scores: The model gives a probability (0.0 to 1.0) for every word it finds. We must filter out low-confidence "garbage" results.

📚 Learning Resources

Core Tutorial:(https://www.youtube.com/watch?v=RFK3NUWJT9I)

Documentation:(https://blog.roboflow.com/how-to-use-easyocr/)

Concept:(https://pyimagesearch.com/deep-learning-computer-vision-python-book/)

🧪 Weekly Schedule

Mon-Tue: Read the documentation and understand the reader.readtext() output format.

Wed-Thu: Practice running OCR on the sample images provided in the datasets folder.

Fri-Sun: Assignments.

✅ Assignments

Assignment 2.1: The Text Miner

Create a notebook ocr_extraction.ipynb.

Initialize easyocr.Reader(['en'], gpu=True).

Loop through 3 different meme images.

Print the extracted text for each image.

Assignment 2.2: The Confidence Filter

Refine your code. The OCR might pick up random noise.

Modify your loop to check the Confidence Score (the 3rd value in the tuple).

Only print the text if the confidence is greater than 0.5 (50%).

Bonus: Use PIL.ImageDraw to draw a red box around the detected text.

Submission: Upload your notebook and a text file containing the extracted output to Week_2.
