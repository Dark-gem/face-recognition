import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier  # Import the KNeighborsClassifier
import pickle

# Initialize the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the known faces and labels
with open('data/faces.pkl', 'rb') as file:
    known_faces = pickle.load(file)

with open('data/names.pkl', 'rb') as file:
    labels = pickle.load(file)

# Create and train the KNN classifier
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(known_faces, labels)

# Define a similarity threshold
threshold = 0.8  # Adjust this threshold as needed

# Initialize the camera
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    if ret:
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            # Resize the face to match the expected number of features (e.g., 50x50 pixels)
            face = cv2.resize(face_roi, (50, 50))

            # Flatten the resized face
            face = face.flatten().reshape(1, -1)

            # Predict the label and calculate similarity score
            label = knn.predict(face)
            similarity_score = knn.predict_proba(face).max()

            # Check if the similarity score is below the threshold
            if similarity_score < threshold:
                label = "Unknown"

            # Draw the bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({similarity_score:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break
    else:
        print("Error capturing frame")
        break

# Release the camera and close OpenCV windows
camera.release()
cv2.destroyAllWindows()
