import cv2
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
    person_image_path = None  # Initialize to None
    person_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Your existing code for detecting and processing persons
        results = model(frame)
        for result in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, result[:4])
            person_roi = frame[y1:y2, x1:x2]
            face_embedding = get_face_embedding(person_roi)
            if face_embedding is not None:
                input_embedding_1d = input_embedding.flatten()
                face_embedding_1d = face_embedding[0].flatten()
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
    return person_found, person_image_path  # Return the status and path


# Main function to handle user input and video processing
def main(input_image_path, video_path):
    input_image = cv2.imread(input_image_path)
    input_embedding = get_face_embedding(input_image)
    if input_embedding is not None:
        person_found, person_image_path = process_video(video_path, input_embedding)
        if person_found:
            print("Person found and image saved at:", person_image_path)
            return person_found, person_image_path
        else:
            print("Person not found in the video.")
    else:
        print("No face detected in the input image.")

    return False, None
