from ultralytics import YOLO
import cv2
from tqdm import tqdm

# Initialize the model
model_path = '../Model Training/runs/classify/train/weights/best.pt'
model = YOLO(model_path)

# Video paths
video_input_path = 'initial-trimmed-videos/match2.mkv'
video_output_path = 'Relevant Frames Videos/match2.mp4'
relevant_frames_path = 'Relevant Frames Videos/match2_frames.txt'  # Path for the text file to store relevant frame indices

irrelevant_frames_video_path = 'Irrelevant Frames Videos/match2.mp4'
irrelevant_frames_path = 'Irrelevant Frames Videos/match2_frames.txt'  # Path for the text file to store irrelevant frame indices

try:
    # Initialize video capture
    cap = cv2.VideoCapture(video_input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize video writer
    out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width, frame_height))

    out_irrelevant = cv2.VideoWriter(irrelevant_frames_video_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width, frame_height))

    relevant_frames = []  # List to store indices of relevant frames
    irrelevant_frames = []  # List to store indices of irrelevant frames

    # Process video with tqdm progress bar
    for frame_idx in tqdm(range(total_frames), desc="Processing Video"):
        ret, frame = cap.read()
        if not ret:
            break
        
        result = model(frame, verbose=False)
        class_names_dict = result[0].names
        class_with_max_prob = result[0].probs.top1
        pred_class = class_names_dict[class_with_max_prob]

        if pred_class == 'relevant':
            out.write(frame)
            relevant_frames.append(frame_idx)  # Store index of relevant frame
        else:
            out_irrelevant.write(frame)
            irrelevant_frames.append(frame_idx)

finally:
    # Release resources
    cap.release()
    out.release()
    out_irrelevant.release()

    # Write relevant frame indices to text file
    with open(relevant_frames_path, 'w') as file:
        for frame_idx in relevant_frames:
            file.write(f"{frame_idx}\n")
    
    # Write irrelevant frame indices to text file
    with open(irrelevant_frames_path, 'w') as file:
        for frame_idx in irrelevant_frames:
            file.write(f"{frame_idx}\n")


print("The video and the list of relevant frames were successfully saved.")
