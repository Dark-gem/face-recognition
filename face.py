import os
import numpy as np
import cv2
import pickle

def capture_and_store_face_data(name, data_limit=100):
    # Check if the 'data' directory exists, and create it if it doesn't
    if not os.path.exists('data/'):
        os.makedirs('data/')

    face_data = []
    i = 0

    camera = cv2.VideoCapture(0)

    facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    ret = True

    while ret:
        ret, frame = camera.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face_coordinates = facecascade.detectMultiScale(gray, 1.3, 4)

            for (a, b, w, h) in face_coordinates:
                faces = frame[b:b + h, a:a + w, :]
                resized_faces = cv2.resize(faces, (50, 50))

                if i % 10 == 0 and len(face_data) < data_limit:  # Store every 10th frame up to the limit
                    face_data.append(resized_faces)
                cv2.rectangle(frame, (a, b), (a + w, b + h), (255, 0, 0), 2)
            i += 1

            cv2.imshow('frames', frame)

            if cv2.waitKey(1) == 27 or len(face_data) >= data_limit:  # Exit when 'Esc' is pressed or data limit is reached
                break
        else:
            print('error')
            break

    cv2.destroyAllWindows()
    camera.release()

    face_data = np.asarray(face_data)
    face_data = face_data.reshape(len(face_data), -1)

    if 'names.pkl' not in os.listdir('data/'):
        names = [name] * len(face_data)
        with open('data/names.pkl', 'wb') as file:
            pickle.dump(names, file)
    else:
        with open('data/names.pkl', 'rb') as file:
            names = pickle.load(file)

        names = names + [name] * len(face_data)
        with open('data/names.pkl', 'wb') as file:
            pickle.dump(names, file)

    if 'faces.pkl' not in os.listdir('data/'):
        with open('data/faces.pkl', 'wb') as w:
            pickle.dump(face_data, w)
    else:
        with open('data/faces.pkl', 'rb') as w:
            faces = pickle.load(w)

        faces = np.append(faces, face_data, axis=0)
        with open('data/faces.pkl', 'wb') as w:
            pickle.dump(faces, w)

if __name__ == "__main__":
    name = input('Enter your name --> ')
    capture_and_store_face_data(name)
