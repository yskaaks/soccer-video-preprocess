from moviepy.editor import VideoFileClip, concatenate_videoclips
import sys

def trim_and_concat_video(video_path, segments):
    """
    Trims the video at multiple segments and concatenates them into a single video.

    Parameters:
    - video_path: Path to the video file.
    - segments: List of tuples, each containing start and end timestamps in HH:MM:SS format for segments to keep.
    """
    try:
        video = VideoFileClip(video_path)
        clips = []
        for start_time, end_time in segments:
            start_h, start_m, start_s = map(int, start_time.split(':'))
            end_h, end_m, end_s = map(int, end_time.split(':'))
            start_time_seconds = start_h * 3600 + start_m * 60 + start_s
            end_time_seconds = end_h * 3600 + end_m * 60 + end_s
            clip = video.subclip(start_time_seconds, end_time_seconds)
            clips.append(clip)
        
        final_clip = concatenate_videoclips(clips)
        
        # Use a generic output file name and path
        output_file = "trimmed_video.mp4"
        
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=video.fps)
        print(f"Trimmed and concatenated video has been saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py video_path [start_time-end_time pairs]")
    else:
        video_path = sys.argv[1]
        segments = [tuple(arg.split('-')) for arg in sys.argv[2:]]
        trim_and_concat_video(video_path, segments)