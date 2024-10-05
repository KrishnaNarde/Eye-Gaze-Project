import cv2
import mediapipe as mp
import pyautogui
from math import hypot

# Initialize the camera
cam = cv2.VideoCapture(0)

# Load the MediaPipe FaceMesh model
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Define the blink threshold
blink_thresh = 0.25  # Adjust as needed

# Define the indexes for eye landmarks
left_eye_landmarks = list(range(159, 145, -1)) + [145]
right_eye_landmarks = list(range(386, 380, -1)) + [380]

# Function to calculate the eye aspect ratio
def calculate_ear(eye_landmarks):
    # Calculate the euclidean distances between the landmarks
    horizontal_length = hypot(eye_landmarks[1][0] - eye_landmarks[5][0], eye_landmarks[1][1] - eye_landmarks[5][1])
    vertical_length = hypot(eye_landmarks[2][0] - eye_landmarks[4][0], eye_landmarks[2][1] - eye_landmarks[4][1])
    # Calculate the eye aspect ratio
    ear = vertical_length / horizontal_length
    return ear

# Main loop
while True:
    # Read a frame from the camera
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect facial landmarks
    output = face_mesh.process(rgb_frame)
    if output.multi_face_landmarks:
        landmarks = output.multi_face_landmarks[0].landmark

        # Extract landmarks for left and right eyes
        left_eye_coords = [(int(landmarks[i].x * screen_width), int(landmarks[i].y * screen_height)) for i in left_eye_landmarks]
        right_eye_coords = [(int(landmarks[i].x * screen_width), int(landmarks[i].y * screen_height)) for i in right_eye_landmarks]

        # Calculate the eye aspect ratios
        left_ear = calculate_ear(left_eye_coords)
        right_ear = calculate_ear(right_eye_coords)

        # Check for left eye blink
        if left_ear < blink_thresh:
            pyautogui.click(button='left')

        # Check for right eye blink
        if right_ear < blink_thresh:
            pyautogui.click(button='right')

        # Draw landmarks for left eye
        for coord in left_eye_coords:
            cv2.circle(frame, coord, 1, (0, 255, 0), -1)

        # Draw landmarks for right eye
        for coord in right_eye_coords:
            cv2.circle(frame, coord, 1, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Face Mesh', frame)

    # Check for termination key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cam.release()
cv2.destroyAllWindows()