import cv2
import numpy as np
from ultralytics import YOLO
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import os
from scipy.spatial.distance import cosine


# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize MTCNN face detector
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=False, device=device)

# Initialize InceptionResnetV1 model for face recognition
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


# Function to extract face embedding from an image
def get_face_embedding(image):
    face, _ = mtcnn(image, return_prob=True)
    if face is not None:
        face = face.unsqueeze(0).to(device)
        embedding = resnet(face).detach().cpu().numpy()
        return embedding
    return None


# Function to process video and search for the input person
def process_video(video_path, input_embedding):
    cap = cv2.VideoCapture(video_path)
    person_found = False
    matched_folder = 'matched'
    os.makedirs(matched_folder, exist_ok=True)
    person_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect persons using YOLOv8
        results = model(frame)
        for result in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, result[:4])
            person_roi = frame[y1:y2, x1:x2]

            # Detect face within the person bounding box
            face_embedding = get_face_embedding(person_roi)
            if face_embedding is not None:
                # Ensure both embeddings are 1-dimensional
                input_embedding_1d = input_embedding.flatten()
                face_embedding_1d = face_embedding[0].flatten()

                # Compare the face embedding with the input embedding
                similarity = cosine(input_embedding_1d, face_embedding_1d)
                if similarity < 0.6:  # Threshold for similarity
                    person_found = True
                    person_image_path = os.path.join(matched_folder, f'person_{person_count}.png')
                    cv2.imwrite(person_image_path, person_roi)
                    person_count += 1
                    break  # Stop searching if the person is found

        if person_found:
            break  # Exit the loop if the person is found

    cap.release()
    cv2.destroyAllWindows()
    return person_found


# Main function to handle user input and video processing
def main(input_image_path, video_path):
    # Load the input image
    input_image = cv2.imread(input_image_path)
    input_embedding = get_face_embedding(input_image)

    if input_embedding is not None:
        # Process the video to search for the person
        person_found = process_video(video_path, input_embedding)
        if person_found:
            print("Person found and image saved.")
        else:
            print("Person not found in the video.")
    else:
        print("No face detected in the input image.")


# Define paths to the input image and video
downloads_folder = os.path.expanduser(r'E:\New folder')
input_image_name = 'WhatsApp Image 2024-05-22 at 11.18.08 PM.jpeg'  # Replace with your image filename
input_image_path = os.path.join(downloads_folder, input_image_name)
video_path = r'video/WhatsApp Video 2024-05-22 at 17.05.33_146e7909.mp4'  # Replace with your video path

# Run the main function with the input image and video paths
main(input_image_path, video_path)