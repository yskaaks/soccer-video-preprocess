from moviepy.editor import VideoFileClip, concatenate_videoclips
import sys

def read_omit_timestamps(file_path):
    """
    Reads the timestamps to omit from the given file.

    Parameters:
    - file_path: Path to the text file containing timestamps to omit.
    
    Returns:
    - A list of tuples, each containing start and end timestamps in HH:MM:SS format to omit.
    """
    timestamps = []
    with open(file_path, 'r') as f:
        for line in f:
            start_time, end_time = line.strip().split(', ')
            timestamps.append((start_time, end_time))
    return timestamps

def calculate_segments_to_keep(video_duration, timestamps_to_omit):
    """
    Calculates the segments to keep based on the timestamps to omit.

    Parameters:
    - video_duration: Duration of the video in seconds.
    - timestamps_to_omit: List of tuples with timestamps to omit.
    
    Returns:
    - A list of tuples, each containing start and end timestamps in seconds for segments to keep.
    """
    segments_to_keep = []
    last_end_time = 0
    for start_time, end_time in timestamps_to_omit:
        # Convert start_time and end_time from HH:MM:SS to seconds
        start_h, start_m, start_s = map(int, start_time.split(':'))
        end_h, end_m, end_s = map(int, end_time.split(':'))
        start_time_seconds = start_h * 3600 + start_m * 60 + start_s
        end_time_seconds = end_h * 3600 + end_m * 60 + end_s
        
        if start_time_seconds > last_end_time:
            segments_to_keep.append((last_end_time, start_time_seconds))
        last_end_time = end_time_seconds
    
    if last_end_time < video_duration:
        segments_to_keep.append((last_end_time, video_duration))
    
    return segments_to_keep

def trim_and_concat_video(input_video_path, output_video_path, timestamps_file):
    try:
        # Load the video file
        video = VideoFileClip(input_video_path)
        video_duration = video.duration
        
        # Read timestamps to omit and calculate segments to keep
        timestamps_to_omit = read_omit_timestamps(timestamps_file)
        segments = calculate_segments_to_keep(video_duration, timestamps_to_omit)
        
        clips = []
        for start_time_seconds, end_time_seconds in segments:
            # Trim the video for each segment and add to the list
            clip = video.subclip(start_time_seconds, end_time_seconds)
            clips.append(clip)
        
        # Concatenate all the clips into one video
        final_clip = concatenate_videoclips(clips)
        
        # Write the concatenated video file without audio
        final_clip.write_videofile(output_video_path, codec="libx264", audio=False, fps=video.fps)
        
        print(f"Trimmed and concatenated video has been saved as {output_video_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py input_video_path output_video_path timestamps_file")
    else:
        input_video_path = sys.argv[1]
        output_video_path = sys.argv[2]
        timestamps_file = sys.argv[3]
        trim_and_concat_video(input_video_path, output_video_path, timestamps_file)
