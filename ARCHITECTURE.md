# Architecture Overview

## High-level structure

The repository is split into two primary subsystems:

1. **Detection pipeline (`detection/`)**: Captures video, detects motion, detects falls with NanoDet, records incident clips, and sends email alerts.
2. **Web application (`webapp/`)**: Flask UI for live camera streaming and browsing recorded incident thumbnails.

## Detection pipeline

The detection workflow is orchestrated by `DetectionPipeline`, which wires together the major services and drives the frame-processing loop. `main.py` instantiates the pipeline and starts it. The pipeline uses:

- **VideoCapture** to read frames from a camera or a configured video file.
- **MovementDetector** to gate processing on motion events via background subtraction.
- **FallDetector** to run NanoDet inference and classify whether a person is lying down.
- **VideoRecorder** to capture a 10-second clip and a thumbnail for the incident.
- **EmailSender** to send a notification with the generated thumbnail.

When movement is detected, the pipeline runs fall detection. If a fall is detected, the recorder writes the video clip and thumbnail into the webapp’s `static` directories. Once recording ends, the pipeline triggers the email notification.

## Web application

The Flask app registers a blueprint with routes for:

- **Home/About pages** for basic navigation.
- **Live feed** that streams frames from the local camera using a multipart JPEG response.
- **Incidents page** that enumerates saved thumbnails from the static folder.

The webapp reads assets directly from `webapp/static/` and templates from `webapp/templates/`.

## Data flow summary

1. `DetectionPipeline` captures a frame.
2. Movement detection decides whether to run fall detection.
3. NanoDet inference + person posture logic classify a fall.
4. If a fall is detected, `VideoRecorder` saves a clip and thumbnail under `webapp/static/videos/` and `webapp/static/thumbnails/`.
5. `EmailSender` sends the thumbnail in an alert email.
6. The web UI lists the thumbnails and can serve the saved videos.
