🗓️ Week 3: The Insight (NLP) & Mid-Sem Eval
Focus: Sentiment Analysis & Pipeline Integration
Goal: Understand the emotion behind the text.
🧠 Theoretical Framework
We use TextBlob for lexicon-based sentiment analysis. It assigns two metrics to every piece of text:
1. Polarity: [-1.0 to +1.0]. Is the text Negative (e.g., "Sad", "Bad") or Positive ("Happy", "Great")?
2. Subjectivity: [0.0 to 1.0]. Is it a Fact (0.0) or an Opinion (1.0)?
The Sarcasm Gap: You will likely notice that some memes have positive text ("Great job") but a sarcastic image. Our current tool (TextBlob) only sees the text. This is a known limitation we will discuss.
📚 Learning Resources
• Core Tutorial:(https://textblob.readthedocs.io/en/dev/quickstart.html)
• Concept:(https://www.geeksforgeeks.org/python-textblob-sentiment-method/)
• Video Guide:(https://www.youtube.com/watch?v=pkdmcsyYvb4)
🧪 Weekly Schedule
• Mon-Tue: Learn Polarity vs. Subjectivity.
• Wed: Learn to clean text (removing newlines, fixing spelling).
• Thu-Sun: Mid-Semester Project.
🚨 Mid-Semester Evaluation (Due Sunday)
Deliverable: mid_term_prototype.ipynb
You must submit a single, clean Jupyter Notebook that demonstrates the Full Linear Pipeline:
1. Input: Loads an image.
2. Step 1: Resizes the image (Pillow).
3. Step 2: Extracts Text (EasyOCR).
4. Step 3: Analyzes Sentiment (TextBlob).
5. Output: Displays the image with the extracted text and sentiment scores printed below it.
Submission: Upload the notebook to Week_3.
