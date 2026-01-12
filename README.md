# Image to Insight: The Meme Analyzer

**Phase II Final Submission | Gold Standard Reference**

## Project Overview

The **Meme Analyzer** is a multimodal AI application that reverse-engineers internet memes. By combining **Computer Vision (CV)** and **Natural Language Processing (NLP)**, the system extracts text from raw pixels and analyzes the emotional sentiment behind the message.

This project represents the culmination of the "Image to Insight" curriculum, integrating:

- **Pillow**: Image preprocessing and manipulation
- **EasyOCR**: Deep learning-based Optical Character Recognition
- **TextBlob**: Sentiment analysis and natural language processing
- **Streamlit**: Interactive web application deployment

## Features

- **Robust OCR**: Uses a CRAFT + CRNN pipeline to detect text on complex backgrounds
- **Sentiment Metrics**: Calculates Polarity (Positive/Negative) and Subjectivity (Fact/Opinion)
- **GPU Acceleration**: Automatically detects and utilizes CUDA if available for faster inference
- **Reactive UI**: Built with Streamlit for real-time analysis and visualization
- **Caching**: Implements efficient model loading patterns to ensure high performance

## Installation & Setup

### Prerequisites

- Python 3.9+
- (Optional) NVIDIA GPU with CUDA drivers for accelerated OCR


### Quickstart (Windows)

1. **Open a terminal in the project folder:**
  ```powershell
  cd "c:\Users\santo\Downloads\meme-analyzer-main\meme-analyzer-main"
  ```
2. **Create and activate a virtual environment:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  If activation is blocked, run:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```
3. **Install dependencies:**
  ```powershell
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
4. **Download TextBlob corpora:**
  ```powershell
  python -m textblob.download_corpora
  ```
5. **Run the app:**
  ```powershell
  streamlit run app.py
  ```
  The app will open at http://localhost:8501

## Usage Guide

1. **Upload**: Click "Browse files" to select a meme (JPG/PNG)
2. **View**: The app will display the raw image side-by-side with the analysis panel
3. **Analyze**: Click the "Analyze Meme" button
   - Note: The first run may take a few seconds as the AI models initialize. Subsequent runs will be faster due to caching.
4. **Interpret**: Review the extracted text, confidence score, and sentiment label

### Understanding Sentiment Scores

The analyzer provides two key metrics:

#### 1. **Sentiment Polarity** (Range: -1.0 to +1.0)

- **POSITIVE (0.1 to 1.0)** 😊
  - Text contains happy, uplifting, or favorable words
  - Examples: "love", "awesome", "beautiful", "happy", "great"
  - **Meme Goal**: TO MAKE YOU SMILE (Wholesome/Funny)

- **NEGATIVE (-1.0 to -0.1)** 😔
  - Text contains sad, critical, or unfavorable words
  - Examples: "hate", "terrible", "failure", "empty", "bad"
  - **Meme Goal**: TO VENT/COMPLAIN (Relatable Frustration)

- **NEUTRAL (-0.1 to 0.1)** 😐
  - Text is factual or has no strong emotional words
  - Examples: "The cat is sitting", "Click here", "Today is Monday"
  - **Meme Goal**: TO STATE FACTS (Informational)

#### 2. **Subjectivity** (Range: 0.0 to 1.0)

- **High Subjectivity (0.6 - 1.0)**: Opinion/Humor - expresses personal feelings
- **Medium Subjectivity (0.3 - 0.6)**: Mixed - combination of fact and opinion
- **Low Subjectivity (0.0 - 0.3)**: Factual/Objective - presents information as fact

#### Examples:

| Text | Polarity | Sentiment | Meme Purpose |
|------|----------|-----------|-------------|
| "I love this meme!" | +0.5 | POSITIVE 😊 | TO MAKE YOU SMILE |
| "This is terrible and I hate it" | -0.8 | NEGATIVE 😔 | TO VENT/COMPLAIN |
| "The image shows a cat" | 0.0 | NEUTRAL 😐 | TO STATE FACTS |
| "brother may i have some loops" | 0.0 | NEUTRAL 😐 | TO ENTERTAIN (General) |
| "empty existence full of failure" | -0.15 | NEGATIVE 😔 | TO VENT/COMPLAIN |

## Technical Architecture

### Backend: `meme_engine.py`

The backend logic encapsulates the `MemeAnalyzer` class, handling:
- Initialization of the EasyOCR reader (heavy resource)
- The processing pipeline (Image → OCR → NLP)
- GPU context management
- Error handling for edge cases (empty images, corrupted files)

### Frontend: `app.py`

The frontend UI utilizes:
- `@st.cache_resource` to load the MemeAnalyzer once, ensuring efficient memory usage
- Reactive event loop for user interactions
- Data visualization with metrics and color-coded sentiment

### Key Design Patterns

- **Singleton Pattern**: The MemeAnalyzer is loaded once and reused across all requests
- **Separation of Concerns**: Backend logic is completely decoupled from the UI
- **Graceful Degradation**: CPU fallback if GPU is not available


## Project Structure

```
meme-analyzer-main/
├── app.py                # Streamlit frontend
├── meme_engine.py        # Backend analysis engine
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── iter1.ipynb           # Experimental notebook
```

## Troubleshooting

### GPU Not Detected

If you have a CUDA-compatible GPU but it's not being used:
1. Verify CUDA installation: `python -c "import torch; print(torch.cuda.is_available())"`
2. Ensure you have the correct PyTorch version: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

### Slow Processing

If OCR is taking a long time:
- **Without GPU**: 2-10 seconds per image is normal
- **With GPU**: Should be under 1 second
- Consider disabling spell-check (adds 1-3 seconds)


### Module Import Errors

If you get import errors:
```powershell
pip install --upgrade -r requirements.txt
```

## Credits

- **EasyOCR** by JaidedAI for the text extraction model
- **TextBlob** by sloria for the NLTK wrapper
- **Streamlit** for the rapid application framework

## License

This project is for educational purposes as part of the "Image to Insight" curriculum.

---

**Built with ❤️ for the Image to Insight Curriculum Team | January 2026**
