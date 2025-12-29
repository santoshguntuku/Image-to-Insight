🗓️ Week 4: The Web Dashboard

Focus: Streamlit & Software Architecture

Goal: Move from "Notebook Scripts" to a "Web Application."

🧠 Theoretical Framework

Code living in a notebook is hard to share. Streamlit turns Python scripts into interactive websites.

• State Management: Streamlit reruns the entire script every time you click a button. We must handle this efficienty.

• Caching: Loading the EasyOCR model takes time. We will use @st.cache_resource to load the model only once, so the app doesn't freeze on every interaction.

📚 Learning Resources

• Official Tutorial:(https://docs.streamlit.io/get-started/tutorials/create-an-app)

• Video Course:(https://www.youtube.com/watch?v=Klqn--Mu2pE)

🧪 Weekly Schedule

• Mon-Tue: "Hello World" in Streamlit. Learn st.file_uploader and st.write.

• Wed: Refactor your Week 3 code into a class MemeAnalyzer in a separate file meme_engine.py.

• Thu-Sun: Build the UI.

✅ Assignments

Assignment 4.1: The Backend (meme_engine.py)

Take your logic from the Mid-Sem notebook and clean it up. Put it into a pure Python file. It should not have any print() statements, only return statements.

Assignment 4.2: The Frontend (app.py)

Create a Streamlit app that:
1. Imports your MemeAnalyzer.
2. Allows the user to upload an image.
3. Displays the image.
4. Shows the text and sentiment in a nice layout (use st.columns).

Submission: Upload app.py, meme_engine.py, and a screenshot of your app running to Week_4.
