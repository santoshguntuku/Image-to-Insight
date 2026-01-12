"""
app.py
------
The Streamlit frontend for the 'Image to Insight' Meme Analyzer.
This script handles user interaction, image uploading, and results visualization.

Usage:
    streamlit run app.py
"""

import streamlit as st
from PIL import Image
from meme_engine import MemeAnalyzer
import time

# ------------------------------------------------------------------
# Configuration & Setup
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Meme Analyzer | Image to Insight",
    page_icon="🤖",
    layout="wide"
)

# ------------------------------------------------------------------
# Resource Caching
# ------------------------------------------------------------------
# We use @st.cache_resource because MemeAnalyzer contains the EasyOCR model,
# which is a large, non-serializable object that should persist across reruns.
# Reference: Streamlit Docs on Caching Machine Learning Models 
@st.cache_resource
def get_analyzer():
    """
    Initializes and caches the MemeAnalyzer instance.
    This prevents reloading the EasyOCR model on every interaction.
    """
    # This print statement will only appear once in the terminal logs
    print("Loading MemeAnalyzer model... (This should only happen once)")
    return MemeAnalyzer(use_gpu=True)

# Initialize the analyzer
# We wrap this in a try-block to handle cases where dependencies might be missing
try:
    with st.spinner("Loading AI Models (EasyOCR + TextBlob)..."):
        analyzer = get_analyzer()
except Exception as e:
    st.error(f"Fatal Error loading models: {e}")
    st.stop()

# ------------------------------------------------------------------
# UI Layout
# ------------------------------------------------------------------

# Sidebar Configuration
with st.sidebar:
    st.title("Image to Insight")
    st.markdown("### The Meme Analyzer Project")
    st.write("This application integrates Computer Vision and NLP to decode the hidden meanings in memes.")
    
    st.markdown("---")
    st.markdown("### Settings")
    # Toggle for the slow spelling correction feature
    enable_spellcheck = st.checkbox("Enable Auto-Correct", value=False, 
                                  help="Uses TextBlob to fix spelling. Warning: Slows down processing significantly.")
    
    st.markdown("---")
    st.info("Built with EasyOCR, TextBlob, and Streamlit.")

# Main Content Area
st.title("🤖 Meme Sentiment Analyzer")
st.markdown("""
Upload a meme to extract its text and analyze the sentiment. 
The system uses **Deep Learning OCR** to read the image and **Lexicon-based NLP** to score the text.
""")

# Expandable info section about sentiment scores
with st.expander("ℹ️ Understanding Sentiment Scores"):
    st.markdown("""
    ### Sentiment Polarity (-1.0 to +1.0)
    
    - **POSITIVE (0.1 to 1.0)** 😊: Happy, uplifting words → **Meme Goal: TO MAKE YOU SMILE**
    - **NEGATIVE (-1.0 to -0.1)** 😔: Sad, critical words → **Meme Goal: TO VENT/COMPLAIN**
    - **NEUTRAL (-0.1 to 0.1)** 😐: Factual, no emotion → **Meme Goal: TO STATE FACTS**
    
    ### Subjectivity (0.0 to 1.0)
    
    - **High (0.6-1.0)**: Opinion/Humor - expresses feelings
    - **Medium (0.3-0.6)**: Mixed - fact + opinion
    - **Low (0.0-0.3)**: Factual/Objective - just information
    
    ### Examples:
    
    | Text | Score | Sentiment | Purpose |
    |------|-------|-----------|----------|
    | "I love this!" | +0.5 | POSITIVE 😊 | Make you smile |
    | "This is terrible" | -0.8 | NEGATIVE 😔 | Vent frustration |
    | "The cat sits" | 0.0 | NEUTRAL 😐 | State facts |
    | "brother may i have some loops" | 0.0 | NEUTRAL 😐 | Entertain |
    """)

# File Uploader Widget with enhanced settings
st.markdown("---")
uploaded_file = st.file_uploader(
    "📤 Upload a meme image",
    type=["jpg", "png", "jpeg"],
    help="Click 'Browse files' or drag and drop your meme here",
    accept_multiple_files=False
)

# Add helpful tips
if uploaded_file is None:
    st.info("👆 Click **'Browse files'** above to select a meme, or drag and drop an image file into the box.")

if uploaded_file is not None:
    # Use columns to create a side-by-side layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Original Image")
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Meme', use_container_width=True)
        except Exception as e:
            st.error(f"Error reading image: {e}")
            st.stop()

    with col2:
        st.subheader("Analysis Results")
        
        # Action Button
        if st.button("Analyze Meme"):
            start_time = time.time()
            
            # Processing Spinner
            with st.spinner("Extracting text and crunching numbers..."):
                results = analyzer.analyze_image(image, run_spell_check=enable_spellcheck)
            
            end_time = time.time()
            
            # Handle Results
            if results['status'] == 'success':
                # Row 1: Key Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Processing Time", f"{end_time - start_time:.2f}s")
                m2.metric("OCR Confidence", f"{results['confidence']*100:.1f}%")
                
                # Logic to determine color and label based on polarity
                polarity = results['sentiment_polarity']
                if polarity > 0.1:
                    sent_color = "normal" # Streamlit handles positive delta (Green)
                    sent_label = "Positive 😄"
                    delta_color = "normal"
                elif polarity < -0.1:
                    sent_color = "inverse"
                    sent_label = "Negative 😠"
                    delta_color = "inverse" # Streamlit handles negative delta (Red)
                else:
                    sent_label = "Neutral 😐"
                    delta_color = "off"
                
                m3.metric("Sentiment", sent_label, f"{polarity:.2f}", delta_color=delta_color)

                st.markdown("#### Extracted Text")
                st.text_area("Raw Output", results['raw_text'], height=100)
                
                # Insight Box for Subjectivity and Meme Goal
                st.markdown("#### 💡 Insight")
                subj = results['sentiment_subjectivity']
                
                # Determine meme goal based on sentiment + subjectivity
                if polarity > 0.3 and subj > 0.5:
                    meme_goal = "🎉 TO MAKE YOU SMILE (Wholesome/Funny)"
                elif polarity < -0.3 and subj > 0.5:
                    meme_goal = "😤 TO VENT/COMPLAIN (Relatable Frustration)"
                elif polarity > 0 and subj < 0.3:
                    meme_goal = "✅ TO INFORM POSITIVELY (Motivational)"
                elif polarity < 0 and subj < 0.3:
                    meme_goal = "⚠️ TO WARN/CRITIQUE (Serious Message)"
                elif abs(polarity) < 0.1 and subj > 0.5:
                    meme_goal = "🤔 TO MAKE YOU THINK (Thought-provoking)"
                elif abs(polarity) < 0.1 and subj < 0.3:
                    meme_goal = "📰 TO STATE FACTS (Informational)"
                else:
                    meme_goal = "🎭 TO ENTERTAIN (General Humor)"
                
                if subj > 0.5:
                    subj_desc = "Opinionated/Subjective"
                    subj_msg = "This text expresses a strong personal opinion or emotion."
                else:
                    subj_desc = "Factual/Objective"
                    subj_msg = "This text presents information as fact."
                
                st.info(f"**Subjectivity**: {subj_desc} ({subj:.2f})\n\n{subj_msg}")
                st.success(f"**🎯 MEME PURPOSE**: {meme_goal}")

            elif results['status'] == 'no_text_found':
                st.warning("⚠️ No text could be detected in this image. It might be purely visual, or the text is too obscured/stylized for the OCR model.")
            
            else:
                st.error(f"An error occurred: {results.get('message')}")
