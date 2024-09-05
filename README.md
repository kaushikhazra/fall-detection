# Fall Detection Using Computer Vision

## Introduction

This project implements a non-invasive, camera-based fall detection system using computer vision. The system is designed to monitor a closed space, such as a room or office, and detect falls in real-time. It automatically sends alerts and records videos of detected falls, providing a quick and reliable solution to aid elderly people or individuals at risk of falling.

The solution leverages a Raspberry Pi 4B paired with an REES52 night vision camera, enabling detection even in low-light conditions. Powered by Python, OpenCV, and the NanoDet Lite neural network, the system balances performance and accuracy on resource-constrained hardware. This project is particularly beneficial for home-based surveillance and healthcare environments where privacy and comfort are critical concerns.

## Features

- **Non-Invasive Fall Detection**: Uses a camera-based approach, avoiding the need for wearable devices that may cause discomfort or privacy concerns.
- **Real-Time Monitoring**: Continuously monitors a designated area for falls, triggering alerts as soon as a fall is detected.
- **Infrared Camera Support**: Equipped with a night vision camera, the system works efficiently in low-light conditions.
- **Lightweight Neural Network**: The system utilizes the NanoDet Lite neural network for accurate fall detection, optimized for running on Raspberry Pi.
- **Video Recording and Alerts**: Records video footage of detected falls and sends notifications via email to designated recipients.
- **Web-Based Interface**: Users can access the system via a Flask-based web application, allowing them to view recorded incidents and monitor the system remotely.


# Prerequisites

- Python 3.6+
- `pip` (Python package manager)
- Git

## Setup Instructions

### Step 1: Clone the Repository
First, clone the GitHub repository to your local machine:

```bash
git clone https://github.com/kaushikhazra/fall-detection.git
cd fall-detection
```

### Step 2: Create and Activate a Virtual Environment
It is recommended to use a virtual environment to isolate dependencies. To create and activate a virtual environment:

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

For **Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Once the virtual environment is active, install the necessary dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

### 1. To Run the Fall Detection System:
The fall detection system is located inside the `detection` folder. Navigate to this folder and run the `main.py` script:

```bash
cd detection
python main.py
```

This will start the fall detection process. Ensure that the video input (e.g., from a camera or video file) is correctly configured in the code.

### 2. To Run the Automatic Test:
Navigate to `detection` folder and run the `test.py` script:

```bash
cd detection
python test.py
```

### 3. To Run the Web Application:
The web app is located inside the `webapp` folder. Navigate to this folder and run the `app.py` script:

```bash
cd webapp
python app.py
```

The web app will start, and you can access it via your web browser at `http://127.0.0.1:5000/` or another port as configured.

## Contributing
If you wish to contribute to the project, feel free to submit a pull request or report issues via GitHub.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

