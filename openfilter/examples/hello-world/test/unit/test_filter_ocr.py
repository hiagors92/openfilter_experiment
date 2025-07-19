import pytest
from unittest.mock import MagicMock
from openfilter.filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition, OCREngine

def test_ocr_filter_initialization():
    config = {
        'id': 'OCRTest',
        'sources': [],
        'outputs': [],
        'ocr_engine':'easyocr',
        'forward_ocr_texts': True
    }

    filter_instance = FilterOpticalCharacterRecognition(config)

    assert filter_instance.config['id'] == 'OCRTest'
    assert filter_instance.config['ocr_engine'] == OCREngine.EASYOCR