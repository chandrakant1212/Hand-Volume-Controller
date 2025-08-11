# AI Hand Gesture Volume Control 🖐️🔊

A Python script that allows you to control your computer's system volume in real-time using hand gestures captured through your webcam.

This project uses computer vision to track hand landmarks and maps the distance between the thumb and index finger to the system's volume, providing a futuristic and touchless way to interact with your computer.

## 🎥 Demonstration

Here is a short video demonstrating the project in action. The volume bar on the screen and the system volume change as the distance between the fingertips is adjusted.



<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/feef237a-4eb1-4d83-9191-c770cc3a2606" />

<img width="1909" height="1078" alt="image" src="https://github.com/user-attachments/assets/79e91157-c01f-4d85-88f7-75d556489ffa" />


## ✨ Features

* **Real-Time Hand Tracking:** Utilizes Google's MediaPipe for fast and accurate hand landmark detection.
* **Gesture-Based Control:** Simply pinch your thumb and index finger to control the volume.
* **Visual Feedback:** An on-screen display shows your hand landmarks, the active gesture, and a live volume bar.
* **Cross-Platform:** Built with libraries that are compatible with Windows, macOS, and Linux.

## 🛠️ Tech Stack

* **Python 3**
* **OpenCV:** For capturing and rendering the webcam feed.
* **MediaPipe:** For high-fidelity hand and finger tracking.
* **NumPy:** For numerical operations and value mapping.
* **Pycaw:** For controlling system audio on Windows.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+
* A webcam

### Installation

1.  **Clone the repository (or download the files)**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create and Activate a Virtual Environment**
    This keeps the project's dependencies isolated.

    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **On macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the Required Packages**
    Create a file named `requirements.txt` with the content below, then run the `pip install` command.

    * `requirements.txt`:
        ```
        opencv-python
        mediapipe
        numpy
        pycaw
        ```

    * **Installation Command:**
        ```bash
        pip install -r requirements.txt
        ```

## 💻 Usage

1.  Make sure your virtual environment is activated.
2.  Run the main script from your terminal:
    ```bash
    python volume_controller.py
    ```
3.  A window will pop up showing your webcam feed. Show your hand to the camera.
4.  Control the volume by changing the distance between your thumb and index finger.
5.  To stop the application, make sure the webcam window is active and press the **'q'** key.

## 🎨 Customization

You can easily tweak the sensitivity of the gesture control by modifying the hand distance range in `volume_controller.py`:

```python
# Adjust the list [20, 200] to match your preferred min/max finger distance
vol = np.interp(length, [20, 200], [min_vol, max_vol])
```

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
