# Soccer Preprocessing Guide

This document outlines the setup and steps required to preprocess soccer match videos by removing unwanted segments, extracting relevant frames, and preparing data for model training

## Environment Setup

1. **Create a Conda Environment**  
   Start by creating a new Conda environment named `soccer-preprocess` with Python 3.11 installed.
   ```
   conda create -n soccer-preprocess python=3.11 -y
   ```
   Activate the environment:
   ```
   conda activate soccer-preprocess
   ```

2. **Install PyTorch**  
   Install PyTorch, torchvision, torchaudio, and the corresponding CUDA toolkit version (e.g., for CUDA 11.7) using the commands below. Adjust the CUDA version based on your system's specifications.
   ```
   conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia
   ```
   For different CUDA versions, refer to [PyTorch's previous versions](https://pytorch.org/get-started/previous-versions/) for guidance.

3. **Additional Dependencies**  
   Install other necessary Python packages:
   ```
   pip install ultralytics supervision moviepy scikit-learn
   ```

## Video Preprocessing

1. **Trim Videos**  
   Remove pre-match programs and halftime advertisements by keeping only the match segments. For example, if the match is from 00:15:00 to 00:50:00 and 01:05:00 to 01:40:00, these segments are retained:
   ```
   python trim_videos.py /path/to/your/video.mp4 00:15:00-00:50:00 01:05:00-01:40:00
   ```
   Alternatively, you can use video editing software for this step. Store the trimmed videos in the `initial-trimmed-videos` directory.

2. **Extract Frames**  
   To extract frames from the videos, adjust the `VIDEO_DIR_PATH` and `IMAGES_DIR_PATH` in `get_video_frames.py` and run:
   ```
   python get_video_frames.py
   ```
   This saves every 300th frame, producing approximately 2000 images (~1000 images per video).

3. **Organize Frames**  
   Manually categorize the frames into relevant and irrelevant folders within a `Data` directory. Typically, use around 650 irrelevant frames and 950 relevant frames.

## Data Preparation for Model Training

1. **Prepare Training Data**  
   Update the paths in `prepare_training_data.py` and execute it to split the data into training, testing, and validation sets.

2. **Model Training**  
   Navigate to the "Model Training" directory and initiate the training process:
   ```
   cd "Model Training"
   python train.py
   ```

## Post-Training Processing

1. **Remove Irrelevant Frames**  
   Inside the `Remove Irrelevant Frames` directory, adjust the paths in `script.py` and run it to segregate videos into relevant and irrelevant frames.

2. **Remove Replays**  
   Manually record replay timestamps in text files (see `Replay Timestamps` folder for examples). Execute the following command to remove replays from videos:
   ```
   python remove_replays.py input_video_path output_video_path timestamps_file_path
   ```

This guide provides a comprehensive walkthrough for preprocessing soccer match videos, from environment setup to data preparation and model training. Follow each step carefully to ensure the successful completion of the process.