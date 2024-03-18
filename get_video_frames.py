import supervision as sv
from tqdm import tqdm

VIDEO_DIR_PATH = "initial-trimmed-videos"
IMAGE_DIR_PATH = "images"
FRAME_STRIDE = 300

video_paths = sv.list_files_with_extensions(
    directory=VIDEO_DIR_PATH,
    extensions=["mov", "mp4", "mkv"])

for video_path in tqdm(video_paths):
    video_name = video_path.stem
    image_name_pattern = video_name + "-{:05d}.png"
    with sv.ImageSink(target_dir_path=IMAGE_DIR_PATH, image_name_pattern=image_name_pattern) as sink:
        for image in tqdm(sv.get_video_frames_generator(source_path=str(video_path), stride=FRAME_STRIDE)):
            sink.save_image(image=image)