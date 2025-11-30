# 🚀 Realtime-Analyser

**Realtime-Analyser** is a robust, real-time video analysis tool using **YOLOv8 + OpenCV** to detect, track, and precisely analyze objects (like vehicles or production items) in videos or live streams.

---

## 🔹 Key Features

* **Real-time Object Detection and Tracking**
* **Speed & Motion Analysis:** Calculates speed in km/h or other relevant units.
* **Counting & Analytics:** Provides detailed counts and statistics per object class/type.
* **Customizable Detection Models:** Easily integrate different YOLO models for specific tasks.
* **Lightweight and Efficient:** Designed for high-performance processing on standard hardware.



---

## 🏁 Getting Started

To get the project running, follow these simple steps in your terminal:

1.  **Clone the repo**:
    ```bash
    git clone [https://github.com/pandeymehak217-lab/realtime-analyser.git](https://github.com/pandeymehak217-lab/realtime-analyser.git)
    cd Realtime-Analyser
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Analyzer on a Video (CLI Mode):**
    ```bash
    python main.py --video path_to_video.mp4
    ```
4.  **Run the Web Dashboard (Recommended for Interactive Use):**
    ```bash
    streamlit run dashboard.py
    ```

---

## 🖥️ Web Dashboard (Interactive Analysis)

The project includes an **interactive web dashboard**, typically accessible at **`http://localhost:8501/`**, which provides a user-friendly interface for the Realtime-Analyser.

This dashboard allows users to:

* **Upload** or specify a video source easily.
* **Visualize** the real-time object detection and tracking output directly in the browser.
* View **live statistics** (counts, speed, etc.) updated dynamically as the analysis runs.

Use the command `streamlit run dashboard.py` (Step 4 in **Getting Started**) to launch this interactive tool.

---

## 🎥 Output Screenshots Gallery

Here are example screenshots/visuals from the analysis. **Consider replacing one of the static images below with a short, for a more dynamic preview!**

| Processed Video  | Object Detection | Speed & Analytics |
| :-------------: | :--------------: | :---------------: |
| <img width="1157" height="686" alt="Screenshot 2025-11-30 at 14 14 17" src="https://github.com/user-attachments/assets/b0ec2dd5-9ba5-4114-a871-52a681e5c057" /> |<img width="1455" height="792" alt="Screenshot 2025-11-30 at 17 30 01" src="https://github.com/user-attachments/assets/27bb225e-01ad-418a-b5a9-76f75b9d6872" /> |<img width="1650" height="827" alt="Screenshot 2025-11-30 at 17 29 26" src="https://github.com/user-attachments/assets/14a5f80b-1174-4993-9db5-7387965c98fa" />|


## ✅ Use Cases

The versatility of the SpeedAI-Analyser allows its application across various industries:

* 🚗 **Traffic monitoring & speed analysis**
* 🏟️ **Sports analytics** (e.g., tracking players or balls)
* 📹 **Security & surveillance** (e.g., perimeter monitoring)
* 🏭 **Industrial automation & process monitoring** (e.g., counting items on a conveyor belt)

---

## 📄 License

This project is released under the **MIT License**. 
