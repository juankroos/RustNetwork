import platform
import sys
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv3D, MaxPooling3D, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from scipy import stats

# Check platform architecture
architecture = platform.architecture()
print(f"Platform architecture: {architecture}")

# Check if Python is 64-bit
is_64bits = sys.maxsize > 2**32
print(f"Is Python 64-bit: {is_64bits}")

# Print Python version

# Initialize MediaPipe Holistic model and drawing utilities
mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

# Define main path for the WLASL dataset
main_path = '/kaggle/input/wlasl-processed/'

# Load WLASL dataset
wlas_df = pd.read_json(main_path + 'WLASL_v0.3.json')

# Display first few rows and shape of the dataset
print(wlas_df.head())
print(wlas_df.shape)

# Function to extract available video IDs from the dataset
def get_videos_ids(json_list):
    """
    Function to check if the video ID is available in the dataset
    and return the video IDs of the current instance
    
    Input: instance JSON list
    Output: list of video IDs
    """
    videos_list = []    
    for ins in json_list:
        video_id = ins['video_id']
        if os.path.exists(f'{main_path}videos/{video_id}.mp4'):
            videos_list.append(video_id)
    return videos_list

# Function to extract video IDs and paths
def get_json_features(json_list):
    """
    Function to check if the video ID is available in the dataset
    and return the video IDs and paths of the current instance
    
    Input: instance JSON list
    Output: list of video IDs, list of video paths
    """
    videos_ids = []
    videos_urls = []
    videos_paths = []
    for ins in json_list:
        video_id = ins['video_id']
        video_url = ins['url']
        path = f'{main_path}videos/{video_id}.mp4'
        if os.path.exists(path):
            videos_ids.append(video_id)
            videos_urls.append(video_url)
            videos_paths.append(path)
    return videos_ids, videos_paths

# Load JSON data
with open(main_path + 'WLASL_v0.3.json', 'r') as data_file:
    json_data = data_file.read()

instance_json = json.loads(json_data)

# Test functions
print(get_videos_ids(instance_json[0]['instances'])[0])
print(get_json_features(instance_json[1]['instances'])[0])
print(get_json_features(instance_json[1]['instances'])[1])
print(len(get_videos_ids(instance_json[1]['instances'])))

# Add video IDs to the DataFrame
wlas_df['videos_ids'] = wlas_df['instances'].apply(get_videos_ids)

# Display updated DataFrame
print(wlas_df)

# Add number of samples per gloss
wlas_df['samples_num'] = wlas_df['videos_ids'].apply(len)
print(wlas_df.head())

# Create training DataFrame
train_df = wlas_df.explode("videos_ids")
train_df = train_df[["videos_ids", "gloss"]]
train_df.columns = ["video_id", "sign"]
train_df["path"] = f'{main_path}videos/' + train_df["video_id"].astype(str) + ".mp4"
train_df["sequence_id"] = train_df.groupby('sign').cumcount() + 1
features_df = train_df.copy()

# Save features_df to CSV
features_df.to_csv('features_df.csv', index=False)
print("features_df saved to 'features_df.csv'")
print(features_df)

# Display first 10 rows of train_df
print(train_df[0:10])

# Define a custom function to generate the path, participant_id, sign, and sequence_id columns
def process_row(row):
    video_id = row["videos_ids"]
    path = f"{main_path}videos/{video_id}.mp4"
    participant_id = video_id
    sign = row["gloss"]
    sequence_id = row["samples_num"]
    return pd.Series([path, participant_id, sign, sequence_id])

# Apply the custom function to each row of the wlas_df DataFrame
train_df = wlas_df.apply(process_row, axis=1, result_type="expand")
train_df.columns = ["path", "participant_id", "sign", "sequence_id"]

# MediaPipe detection function
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
    return image, results

# Draw landmarks with basic connections
def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)  # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections

# Draw styled landmarks with custom colors
def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )

# Print OpenCV version
print(cv2.__version__)

# Function to extract keypoints
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

# Path for exported data, numpy arrays
DATA_PATH = os.path.join('MP_Data')

# Actions to detect (using a subset of WLASL glosses)
actions = np.array(['book', 'drink', 'computer'])  # Adjust based on your needs

# Number of sequences and sequence length
no_sequences = 30
sequence_length = 30
start_folder = 0

# Create directories for storing keypoints
for action in actions:
    for sequence in range(no_sequences):
        try:
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

# Process videos from the dataset and extract keypoints
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for action in actions:
        # Get video IDs for the current action
        video_ids = wlas_df[wlas_df['gloss'] == action]['videos_ids'].iloc[0]
        for sequence, video_id in enumerate(video_ids[:no_sequences]):
            video_path = f'{main_path}videos/{video_id}.mp4'
            cap = cv2.VideoCapture(video_path)
            frame_num = 0
            while cap.isOpened() and frame_num < sequence_length:
                ret, frame = cap.read()
                if not ret:
                    break

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Draw landmarks
                draw_styled_landmarks(image, results)

                # Export keypoints
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                os.makedirs(os.path.dirname(npy_path), exist_ok=True)
                np.save(npy_path, keypoints)

                frame_num += 1

            cap.release()

# Preprocess data and create labels
label_map = {label: num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            npy_path = os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy")
            if os.path.exists(npy_path):
                res = np.load(npy_path)
                window.append(res)
            else:
                window.append(np.zeros(1662))  # 1662 = 33*4 + 468*3 + 21*3 + 21*3
        sequences.append(window)
        labels.append(label_map[action])

# Convert to numpy arrays
X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# Build 3D CNN model
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()

# First 3D convolutional layer
model.add(Conv3D(filters=32, kernel_size=(3, 3, 3), activation='relu', input_shape=(30, 1662, 1, 1)))  # Adjusted for keypoints
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2, 2, 1)))
model.add(Dropout(0.25))

# Second 3D convolutional layer
model.add(Conv3D(filters=64, kernel_size=(3, 3, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2, 2, 1)))
model.add(Dropout(0.25))

# Third 3D convolutional layer
model.add(Conv3D(filters=128, kernel_size=(3, 3, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2, 2, 1)))
model.add(Dropout(0.25))

# Flatten and dense layers
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(actions.shape[0], activation='softmax'))

# Compile the model
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# Display model summary
model.summary()

# Train the model
model.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])

# Make predictions
res = model.predict(X_test)
print(actions[np.argmax(res[4])])
print(actions[np.argmax(y_test[4])])

# Save model weights
model.save('action.h5')

# Load model weights
model.load_weights('action.h5')

# Evaluate model
yhat = model.predict(X_test)
ytrue = np.argmax(y_test, axis=1).tolist()
yhat = np.argmax(yhat, axis=1).tolist()
print(multilabel_confusion_matrix(ytrue, yhat))
print(accuracy_score(ytrue, yhat))

# Real-time visualization function
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return output_frame

# Test with a sample video from the dataset (or webcam for real-time)
sequence = []
sentence = []
predictions = []
threshold = 0.5

# Use a sample video from the dataset for testing
cap = cv2.VideoCapture(f'{main_path}videos/{wlas_df["videos_ids"].iloc[0][0]}.mp4')  # First video as example
# For webcam testing, uncomment the following line and comment the above line
# cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        print(results)

        # Draw landmarks
        draw_styled_landmarks(image, results)

        # Prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(actions[np.argmax(res)])
            predictions.append(np.argmax(res))

            # Visualization logic
            if np.unique(predictions[-10:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

            if len(sentence) > 5:
                sentence = sentence[-5:]

            # Visualize probabilities
            image = prob_viz(res, actions, image, colors)

        cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show to screen (commented out for non-GUI environments)
        # cv2.imshow('OpenCV Feed', image)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break

    cap.release()
    # cv2.destroyAllWindows()

# Plot sample visualization (using last processed frame)
# Note: This assumes 'image' is available; if running in a non-GUI environment, you may need to save the image instead
plt.figure(figsize=(18, 18))
plt.imshow(prob_viz(res, actions, image, colors))
plt.show()