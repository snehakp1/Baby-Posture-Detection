import os
import cv2

def extract_even_frames_from_folder(video_folder, output_root="frames", max_frames=50, pad=3):
    """
    Extract up to max_frames evenly spaced frames from each video in `video_folder`.
    Saves frames to output_root/<folder_name>/ with clear numbered names.

    Args:
        video_folder (str): folder containing video files
        output_root (str): where to create the frames folder
        max_frames (int): maximum frames to extract per video
        pad (int): zero-pad width for saved frame numbers (e.g., 3 => 001)
    """
    folder_name = os.path.basename(video_folder)
    output_folder = os.path.join(output_root, folder_name)
    os.makedirs(output_folder, exist_ok=True)

    video_files = [f for f in os.listdir(video_folder)
                   if f.lower().endswith((".mp4"))]

    if not video_files:
        print(f"No video files found in {video_folder}")
        return

    print(f"\nProcessing folder: {folder_name}  (found {len(video_files)} videos)")

    for vid_idx, video_name in enumerate(video_files, start=1):
        video_path = os.path.join(video_folder, video_name)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f" Cannot open {video_name}")
            continue

        # get total frames (may be float), cast to int
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0

        # fallback: if total_frames is 0, try reading frames sequentially (safe fallback)
        if total_frames <= 0:
            # fallback: iterate until EOF but still limit to max_frames
            extracted = 0
            video_id = f"{folder_name}_video{vid_idx}"
            while extracted < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                fname = f"{video_id}_frame{extracted+1:0{pad}d}.jpg"
                cv2.imwrite(os.path.join(output_folder, fname), frame)
                extracted += 1
            cap.release()
            print(f"  ✔ Extracted {extracted} frames (fallback) from {video_name}")
            continue

        # if total_frames <= max_frames extract every frame
        if total_frames <= max_frames:
            frame_indices = list(range(total_frames))
        else:
            # choose max_frames indices evenly spread across [0, total_frames-1]
            # using integer rounding to distribute samples
            frame_indices = [int(round(i * (total_frames - 1) / (max_frames - 1))) for i in range(max_frames)]

        video_id = f"{folder_name}_video{vid_idx}"
        extracted = 0

        for out_idx, frm_idx in enumerate(frame_indices, start=1):
            # seek to frame index
            cap.set(cv2.CAP_PROP_POS_FRAMES, frm_idx)
            ret, frame = cap.read()
            if not ret:
                # if seeking failed, skip that index
                continue

            fname = f"{video_id}_frame{out_idx:0{pad}d}.jpg"
            cv2.imwrite(os.path.join(output_folder, fname), frame)
            extracted += 1

        cap.release()
        print(f"   Extracted {extracted} frames from {video_name}  (total_frames={total_frames}, fps={fps:.2f})")

    print(f"\nAll done. Frames saved under: {os.path.abspath(output_folder)}")



# Loop through all subfolders

if __name__ == "__main__":
    main_folder = r"C:\Users\user\OneDrive\Desktop\PROJECT\DataSet\baby_videos"  # your main folder
    for sub in sorted(os.listdir(main_folder)):
        subpath = os.path.join(main_folder, sub)
        if os.path.isdir(subpath):
            extract_even_frames_from_folder(subpath, output_root="frames", max_frames=50, pad=3)
