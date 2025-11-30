import argparse
import cv2
import time
import os
import uuid 
import numpy as np


from detector import Detector
from tracker import Tracker
from analyser import Analyser # Analyser must be imported
from utils import save_reports # Keep save_reports

# --------------------------------------------------------------------------
# --- NEW DRAWING FUNCTION ADDED ---
def draw_boxes_green(frame, tracked_objects_with_speed, class_names, frame_number):
    """Draws green bounding boxes, IDs, and speeds on the frame."""
    
    # Draw frame number
    cv2.putText(frame, f"Frame: {frame_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # 🌟 GREEN COLOR DEFINITION (BGR)
    BOX_COLOR = (0, 255, 0) 
    
    # FIX: This loop now correctly unpacks the 7 values from the Analyser's return list
    for x1, y1, x2, y2, track_id, cls_id, speed in tracked_objects_with_speed:
        
        # Ensure coordinates are integers
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        
        # 1. Draw Bounding Box (Rectangle)
        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, thickness=2)

        # Get class name
        cls_name = class_names.get(cls_id, f"Class {cls_id}")
        
        # Prepare Label
        speed_text = f"{speed:.2f} km/h" if speed > 1.0 else ""
        label = f"ID:{track_id} {cls_name} {speed_text}"
        
        # 2. Draw Label Background (Filled rectangle)
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - text_height - 15), (x1 + text_width + 10, y1), BOX_COLOR, -1) 

        # 3. Draw Label Text (White text for contrast)
        cv2.putText(frame, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), thickness=2)
        
    return frame

# --------------------------------------------------------------------------


def run_analysis(video_path: str, output_dir: str, file_id: str) -> dict:
    """Core function to run the full analysis pipeline on a video file."""
    print(f"Processing... Video: {video_path}")
    
    cap = None
    out = None
    try:
       
        detector = Detector(model_path='yolov8n.pt') 
        tracker = Tracker() 
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file at {video_path}")
            
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize Analyser with FPS
        analyser = Analyser(detector.class_names, fps=fps)
        
        output_video_name = f"{file_id}_processed_video.mp4"
        output_video_path = os.path.join(output_dir, output_video_name)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        
    except Exception as e:
        print(f"Error during analysis initialization: {e}")
        if cap and cap.isOpened(): cap.release()
        if out and out.isOpened(): out.release()
        raise e 

  
    frame_number = 0
    start_time = time.time()
    print("Starting frame processing...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame_number += 1
        
       
        detections = detector.detect(frame)
        
        
        tracked_objects = tracker.update(detections, frame) 

        
        # FIX: Capture the return value from analyser.analyse_frame
        tracked_objects_with_speed = analyser.analyse_frame(tracked_objects, frame_number)
        
        
        # FIX: Pass the 7-value list to the drawing function
        processed_frame = draw_boxes_green(frame, tracked_objects_with_speed, detector.class_names, frame_number)
        out.write(processed_frame)

        if frame_number % 100 == 0:
            print(f"  > Processed {frame_number} frames.")


    cap.release()
    out.release()
    
    end_time = time.time()
    
    print("\n" + "="*40)
    print("✔ Detection complete")
    print("✔ Tracking complete")
    print(f"Total time taken: {round(end_time - start_time, 2)} seconds")
    print("="*40)
    
  
    final_data = analyser.get_final_report_data()
    
    # Add metadata to the report for the dashboard
    final_data['metadata'] = {
        'total_frames': frame_number,
        'video_fps': fps,
        'video_width': width,
        'video_height': height,
        'analysis_time_seconds': round(end_time - start_time, 2)
    }
    
    save_reports(final_data, fps, output_dir, file_id) 

    return final_data


def main_cli():
    """Handles Command Line Argument Parsing and launches analysis."""
    parser = argparse.ArgumentParser(description="Realtime Counting Analyser (Terminal Version)")
    parser.add_argument('--video', type=str, required=True, help='Path to the input video file (.mp4, .mov, .avi).')
    parser.add_argument('--output-dir', type=str, default='output', help='Directory to save results.')
    
    args = parser.parse_args()
    
    video_path = args.video
    
    cli_file_id = "report-" + str(uuid.uuid4())[:8] 
    cli_output_dir = args.output_dir
    os.makedirs(cli_output_dir, exist_ok=True) 

    try:
        run_analysis(video_path, cli_output_dir, cli_file_id)
        
        print(f"\nResults successfully saved in the '{cli_output_dir}' directory:")
        print(f" - Processed Video: {cli_output_dir}/{cli_file_id}_processed_video.mp4")
        print(f" - Data JSON: {cli_output_dir}/{cli_file_id}_results.json")
        print(f" - Summary CSV: {cli_output_dir}/{cli_file_id}_report.csv")
        print("\nProcessing complete!")

    except Exception as e:
        print(f"\nFatal Error during CLI run: {e}")


if __name__ == "__main__":
    main_cli()