import argparse
import csv
from datetime import datetime
from openfilter.filter_runtime.filter import Filter
from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.filter_runtime.filters.webvis import Webvis
from filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition

import logging
import time
import psutil
import os
import sys
from multiprocessing import Process

def run_pipeline(config_videoin):
    Filter.run_multi([
        (VideoIn, config_videoin),
        (FilterOpticalCharacterRecognition, dict(
            id="OCRFilter",
            sources=f"tcp://localhost:{config_videoin['outputs'][0].split(':')[-1]}",
            outputs=f"tcp://*:{5552}",
            ocr_engine='easyocr',
            forward_ocr_texts=True,
        )),
        (Webvis, dict(
            id="Webvis",
            sources=f"tcp://localhost:{5552}"
        ))
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OpenFilter benchmark script.")
    parser.add_argument("--loop", action="store_true", help="Loop the video playback")
    parser.add_argument("--video", type=str, default="example_video.mp4", help="Path to the video file")
    parser.add_argument("--loop_duration", type=int, default=60,
                        help="Duration in seconds to run the pipeline when --loop is enabled. "
                             "Pipeline will terminate automatically after this duration to save metrics.")
    parser.add_argument("--port_in", type=int, default=5550, help="IN (VideoIn -> OCRFilter)")
    parser.add_argument("--port_out", type=int, default=5552, help="OUT (OCRFilter -> Webvis)")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"Vnot found: {args.video}")
        sys.exit(1)

    video_start_time = time.time()

    config_videoin = {
        "id": "VideoIn",
        "outputs": [f"tcp://*:{args.port_in}"],
        "sources": [
            {
                "source": f"file://{args.video}",
                "topic": "main",
                "options": {"loop": args.loop}
            }
        ]
    }

    logging.basicConfig(
        filename="execution_metrics.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    process = psutil.Process(os.getpid())
    start_time = time.time()
    cpu_start = process.cpu_times()
    mem_start = process.memory_info().rss

    logging.info("Pipeline starting.")
    logging.info(f"Initial CPU times: {cpu_start}")
    logging.info(f"Initial Memory Usage: {mem_start / (1024 ** 2):.2f} MB")

    proc = Process(target=run_pipeline, args=(config_videoin,))
    
    try:
        proc.start()
        if args.loop:
            logging.info(f"Pipeline running in loop mode for {args.loop_duration} seconds.")
            proc.join(timeout=args.loop_duration)
        else:
            logging.info("Pipeline running in single-pass mode.")
            proc.join()
    except KeyboardInterrupt:
        logging.info("Pipeline interrupted by user (Ctrl+C). Attempting to save metrics.")
    finally:
        if proc.is_alive():
            logging.info("Terminating pipeline process.")
            proc.terminate()
            proc.join(timeout=10) 
            if proc.is_alive():
                logging.warning("Pipeline process did not terminate gracefully. Killing it.")
                proc.kill()
                proc.join() 

    video_end_time = time.time()
    duration_s = video_end_time - video_start_time

    frame_count = 0
    if frame_count == 0:
        logging.warning("Frame count is zero. can be an error? explore more in the future.")
        fps = None
    else:
        fps = frame_count / duration_s if duration_s > 0 else 0

    end_time = time.time()
    cpu_end = process.cpu_times()
    mem_end = process.memory_info().rss

    logging.info("Pipeline ended.")
    logging.info(f"Execution Time: {end_time - start_time:.2f} seconds")
    logging.info(f"Final CPU times: {cpu_end}")
    logging.info(f"Final Memory Usage: {mem_end / (1024 ** 2):.2f} MB")
    logging.info(f"Total Memory Delta: {(mem_end - mem_start) / (1024 ** 2):.2f} MB")

    csv_file = "benchmark_results.csv"
    file_exists = os.path.isfile(csv_file)

    csv_headers = [
        "timestamp", "execution_time_s",
        "cpu_user_start", "cpu_system_start",
        "cpu_user_end", "cpu_system_end",
        "mem_start_mb", "mem_end_mb", "mem_delta_mb",
        "video_name", "loop_enabled",
        "frame_count", "duration_s", "fps"
    ]

    csv_row = [
        datetime.now().isoformat(),
        f"{end_time - start_time:.2f}",
        cpu_start.user, cpu_start.system,
        cpu_end.user, cpu_end.system,
        f"{mem_start / (1024 ** 2):.2f}",
        f"{mem_end / (1024 ** 2):.2f}",
        f"{(mem_end - mem_start) / (1024 ** 2):.2f}",
        args.video, args.loop,
        frame_count, duration_s, fps
    ]

    try:
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(csv_headers)
            writer.writerow(csv_row)
            file.flush()
            os.fsync(file.fileno())
        print("saved metrics on benchmark_results.csv e execution_metrics.log")
    except Exception as e:
        print(f"Error: {e}")