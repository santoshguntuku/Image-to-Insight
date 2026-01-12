"""
meme_engine.py
----------------
The backend logic class for the 'Image to Insight' Meme Analyzer project.
This module encapsulates the complexity of Computer Vision (EasyOCR) and 
Natural Language Processing (TextBlob) into a single, easy-to-use class.

Author: Image to Insight Curriculum Team
Date: January 2026
"""

import easyocr
from textblob import TextBlob
from PIL import Image
import numpy as np
import torch
import logging

# Configure logging to capture system events and errors
# This is production best practice for debugging deployments.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MemeAnalyzer:
    """
    A class to handle the end-to-end processing of meme images.
    
    Attributes:
        reader (easyocr.Reader): The loaded OCR model instance.
    """

    def __init__(self, languages=['en'], use_gpu=True):
        """
        Initialize the MemeAnalyzer.
        
        This method loads the EasyOCR model into memory. This is a heavy operation
        and should ideally be done once per session.
        
        Args:
            languages (list): List of language codes for OCR (default: ['en']).
            use_gpu (bool): Flag to enable/disable GPU acceleration.
        """
        # Robust check for CUDA availability
        self.use_gpu = use_gpu and torch.cuda.is_available()
        
        logging.info(f"Initializing MemeAnalyzer. GPU Available: {torch.cuda.is_available()}. Using GPU: {self.use_gpu}")
        
        try:
            # easyocr.Reader loads the deep learning models (CRAFT + CRNN)
            # We explicitly set the gpu flag based on availability
            self.reader = easyocr.Reader(languages, gpu=self.use_gpu)
            logging.info("EasyOCR Model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load EasyOCR model: {e}")
            # Re-raise exception so the frontend knows initialization failed
            raise e

    def _preprocess_image(self, image_input):
        """
        Convert PIL Image to a format compatible with EasyOCR (NumPy array).
        
        Args:
            image_input (PIL.Image or str): Image object or file path.
            
        Returns:
            numpy.ndarray: The image ready for OCR processing.
        """
        try:
            if isinstance(image_input, str):
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                image = image_input
            else:
                raise ValueError("Input must be a file path or a PIL Image object.")

            # Convert to RGB to ensure consistency (EasyOCR handles internal conversion, 
            # but standardizing input is best practice).
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Convert PIL image to numpy array (Height, Width, Channel)
            return np.array(image)
        except Exception as e:
            logging.error(f"Error in image preprocessing: {e}")
            raise e

    def analyze_image(self, image_input, run_spell_check=False):
        """
        Perform the full analysis pipeline: OCR -> Text Cleaning -> Sentiment Analysis.
        
        Args:
            image_input (PIL.Image or str): The meme image to analyze.
            run_spell_check (bool): Whether to run TextBlob's spell correction (slow).
            
        Returns:
            dict: A dictionary containing:
                - 'raw_text': All text detected joined into a string.
                - 'confidence': Average confidence score of the OCR.
                - 'sentiment_polarity': Float (-1.0 to 1.0).
                - 'sentiment_subjectivity': Float (0.0 to 1.0).
                - 'text_lines': List of individual detected text blocks.
                - 'status': 'success' or 'no_text_found'.
        """
        logging.info("Starting image analysis...")
        
        try:
            img_array = self._preprocess_image(image_input)
            
            # Step 1: Optical Character Recognition (OCR)
            # detail=1 returns list of (bbox, text, prob). 
            # We use detail=1 to calculate average confidence.
            ocr_results = self.reader.readtext(img_array, detail=1)
            
            # Handle the "Empty List" edge case 
            if not ocr_results:
                logging.warning("No text detected in the image.")
                return {
                    'status': 'no_text_found',
                    'raw_text': "",
                    'confidence': 0.0,
                    'sentiment_polarity': 0.0,
                    'sentiment_subjectivity': 0.0,
                    'text_lines': []
                }

            # Step 2: Extract Text and Metrics
            detected_text_list = []
            total_confidence = 0.0
            
            for (bbox, text, prob) in ocr_results:
                detected_text_list.append(text)
                total_confidence += prob
            
            # Join text for NLP context. 
            # Memes often split sentences across top/bottom text.
            full_text = " ".join(detected_text_list)
            avg_confidence = total_confidence / len(ocr_results) if ocr_results else 0.0
            
            logging.info(f"OCR Complete. Detected {len(ocr_results)} lines. Avg Conf: {avg_confidence:.2f}")

            # Step 3: Natural Language Processing (NLP)
            blob = TextBlob(full_text)
            
            # Optional: Spelling Correction
            # NOTE: TextBlob.correct() is computationally expensive and can introduce latency.
            # It uses Peter Norvig's spelling corrector.
            if run_spell_check:
                logging.info("Running spell check (this may take time)...")
                blob = blob.correct()
                full_text = str(blob) # Update full_text with corrected version

            # Sentiment Analysis
            # Polarity: -1.0 (Negative) to 1.0 (Positive)
            # Subjectivity: 0.0 (Fact) to 1.0 (Opinion)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            logging.info(f"Analysis Complete. Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}")

            return {
                'status': 'success',
                'raw_text': full_text,
                'confidence': avg_confidence,
                'sentiment_polarity': polarity,
                'sentiment_subjectivity': subjectivity,
                'text_lines': detected_text_list
            }

        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    # Quick smoke test if run directly
    print("MemeAnalyzer backend is ready. Run 'streamlit run app.py' to launch the interface.")
