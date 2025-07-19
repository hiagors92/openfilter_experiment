from openfilter.filter_runtime.filter import Filter
from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition
from openfilter.filter_runtime.filters.webvis import Webvis


if __name__ == '__main__':
    Filter.run_multi([
        (VideoIn, dict(
            sources=['file:///Users/hiagorodrigues/experiment/openfilter_experiment/openfilter/examples/hello-world/example_video.mp4'],
            outputs=['tcp://*:5550'],
        )),
        (FilterOpticalCharacterRecognition, dict(
            sources=['tcp://localhost:5550'],
            outputs=['tcp://*:5552'],
            ocr_engine='easyocr',
            forward_ocr_texts=True,
        )),
        (Webvis, dict(
            sources=['tcp://localhost:5552'],
        )),
    ])