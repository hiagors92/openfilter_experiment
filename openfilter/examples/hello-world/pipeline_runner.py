import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from openfilter.filter_runtime.filter import Filter
from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition
from openfilter.filter_runtime.filters.webvis import Webvis

if __name__ == "__main__":
    try:
        Filter.run_multi([
            (VideoIn, {
                "id": "VideoIn",
                "outputs": ["tcp://*:5550"],
                "sources": [{
                    "source": "file://example_video.mp4",
                    "topic": "main",
                    "options": {"loop": True} 
                }]
            }),
            (FilterOpticalCharacterRecognition, {
                "id": "OCRFilter",
                "sources": ["tcp://localhost:5550"],
                "outputs": ["tcp://*:5552"],
                "ocr_engine": "easyocr",
                "forward_ocr_texts": True
            }),
            (Webvis, {
                "id": "Webvis",
                "sources": ["tcp://localhost:5552"]
            })
        ])
    except Exception as e:
        print(f"[ERRO]: {e}")