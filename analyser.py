
import numpy as np
import collections

# --- Constants for Speed Calculation ---
# NOTE: YOU MUST CALIBRATE THESE VALUES FOR ACCURATE REAL-WORLD SPEED!
# PIXELS_PER_METER_FACTOR: How many pixels in the video equal 1 meter in the real world.
PIXELS_PER_METER_FACTOR = 5 
FPS_DEFAULT = 30 

class ObjectData:
    """A simple class to hold state for a single tracked object, updated for speed."""
    def __init__(self, track_id, class_name, frame_number):
        self.id = track_id
        self.class_name = class_name
        self.entry_frame = frame_number
        self.exit_frame = frame_number
        self.duration_frames = 0
        # Stores (x_center, y_center, frame_number)
        self.path = collections.deque(maxlen=10) # Using deque to store recent history for speed
        
        # New speed metrics
        self.speeds_kph = []
        self.avg_speed_kph = 0.0
        self.max_speed_kph = 0.0

class Analyser:
    def __init__(self, detector_class_names, fps=FPS_DEFAULT, scale_factor=PIXELS_PER_METER_FACTOR):
        """Initializes the analysis state."""
        self.tracked_objects_data = {} 
        self.class_names = detector_class_names
        self.total_counts = {name: 0 for name in self.class_names.values()}
        self.fps = fps
        self.scale_factor = scale_factor
        print("Analyser initialized.")

    def _calculate_speed(self, obj_data):
        """Calculates instantaneous speed for the object in km/h based on the last two points."""
        path = obj_data.path
        if len(path) < 2:
            return 0.0 # Not enough history to calculate speed

        # Get the last two positions and frames from the deque
        (x2, y2, t2) = path[-1]
        (x1, y1, t1) = path[-2]
        
        # 1. Calculate distance moved (Euclidean distance in pixels)
        distance_pixels = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # 2. Calculate time elapsed (frames)
        time_frames = t2 - t1
        
        if time_frames == 0 or time_frames > 5: # Avoid division by zero, limit max frame gap
            return 0.0
        
        # 3. Convert to Kilometers/Hour 
        # Formula: (distance_pixels / time_frames) * (FPS / PIXELS_PER_METER) * 3.6
        speed_kph = (distance_pixels / time_frames) * (self.fps / self.scale_factor) * 3.6
        
        return speed_kph

    def analyse_frame(self, tracked_objects, frame_number):
        """
        Processes the tracked objects for the current frame.
        Returns a list of 7 values per object: (x1, y1, x2, y2, track_id, class_id, speed_kph)
        """
        current_frame_analysis = [] 
        
        if hasattr(tracked_objects, 'tolist'):
            tracked_objects = tracked_objects.tolist()

        for obj in tracked_objects:
            if len(obj) < 6: continue 
                
            # Unpack the 6 values: (x1, y1, x2, y2, track_id, class_id)
            x1, y1, x2, y2, track_id, class_id = map(int, obj)
            
            class_name = self.class_names.get(class_id, "Unknown")
            x_center = (x1 + x2) // 2
            y_center = (y1 + y2) // 2
            current_speed = 0.0

            if track_id not in self.tracked_objects_data:
                # New object detected
                self.tracked_objects_data[track_id] = ObjectData(track_id, class_name, frame_number)
                self.total_counts[class_name] = self.total_counts.get(class_name, 0) + 1 
            
            # Update object data
            obj_data = self.tracked_objects_data[track_id]
            obj_data.exit_frame = frame_number
            
            # Append new position including frame number
            obj_data.path.append((x_center, y_center, frame_number))
            obj_data.duration_frames += 1
            
            # Calculate and store speed
            current_speed = self._calculate_speed(obj_data)
            
            # Store speed data only if the speed is realistic (e.g., above 1 km/h)
            if current_speed > 1:
                 obj_data.speeds_kph.append(current_speed)
                 obj_data.avg_speed_kph = np.mean(obj_data.speeds_kph)
                 obj_data.max_speed_kph = max(obj_data.max_speed_kph, current_speed)
            
            # Append the full 7-value analysis result for the draw function to use
            # FIX: Ensure all 7 values are included in the return list
            current_frame_analysis.append((x1, y1, x2, y2, track_id, class_id, current_speed))
            
        return current_frame_analysis 


    def get_final_report_data(self):
        """Formats the final data structure for saving."""
        all_tracked_objects_list = []
        
        for id, data in self.tracked_objects_data.items():
            # Only report objects tracked for a minimum duration
            if data.duration_frames > 10:
                all_tracked_objects_list.append({
                    "track_id": id,
                    "class_name": data.class_name,
                    "entry_frame": data.entry_frame,
                    "exit_frame": data.exit_frame,
                    "total_frames_tracked": data.duration_frames,
                    "avg_speed_kph": round(data.avg_speed_kph, 2),
                    "max_speed_kph": round(data.max_speed_kph, 2),
                    "path_length": len(data.path)
                })
        
        report = {
            "total_objects_per_class": self.total_counts,
            "all_tracked_objects": all_tracked_objects_list
        }
        
        return report