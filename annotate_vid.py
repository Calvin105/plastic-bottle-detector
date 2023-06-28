import cv2
import os
import shutil
import datetime


def save_frame_as_image(frame, video_name, output_directory):
    # Generate a unique filename based on the current date and time
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y%m%d%H%M%S%f")
    filename = f"{video_name[:-4]}-{timestamp}.jpg"

    # Save the frame as an image file
    output_path = os.path.join(output_directory, filename).strip()
    cv2.imwrite(output_path, frame)
    print("Frame saved as:", filename)


def handle_key(key, frame_number, total_frame):
    next_video = False
    save_frame = False

    if key == ord('n'):  # Save image and next
        frame_number += 1
        save_frame = True
        if frame_number + 1 >= total_frame:
            next_video = True

    elif key == ord('s'):  # Skip image
        frame_number += 1
        if frame_number + 1 >= total_frame:
            next_video = True

    elif key == ord('1'):  # Skip 10 frames
        frame_number += 10
        if frame_number + 10 >= total_frame:
            next_video = True

    elif key == ord('2'):  # Skip 100 frames
        frame_number += 100
        if frame_number + 100 >= total_frame:
            next_video = True

    elif key == ord('3'):  # Skip 1000 frames
        frame_number += 1000
        if frame_number + 1000 >= total_frame:
            next_video = True

    elif key == ord('p') and frame_number != 0:  # Previous image
        frame_number -= 1

    elif key == ord('q'):  # Next video
        next_video = True
    return next_video, save_frame, frame_number


def get_image_files(directory):
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_files.append(os.path.join(directory, filename))
    return image_files


def save_video_as_image(video_path, cache_path, ext='jpg'):
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    if len(os.listdir(cache_path)) > 0:
        print("Cache detected. Skipped caching process.")
        return

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error opening video file")
        return

    print("Running, this might take a while...")
    frame_index = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        filename = f"frame_{frame_index}.{ext}"
        cv2.imwrite(os.path.join(cache_path, filename), frame)

        frame_index += 1


def read_video_frames_from_cache(save_folder, video_folder):
    """
    Convert MP4 video into JPG image only when there is no cache content. Delete cache content when finishes video

    Benefits:
    1. Fast and convenient

    Notes:
    1. Cache folder don't have to be created
    2. One have to make sure cache directory doesn't contain any other files other than the video files
    3. One have to remove cache content when quitting interface manually
    """
    video_names = [video for video in os.listdir(video_folder) if video.endswith('.mp4')]
    total_videos = len(video_names)

    for i in range(total_videos):
        video_path = os.path.join(video_folder, video_names[i])
        cache_path = os.path.join(os.getcwd(), 'cache')
        save_video_as_image(video_path, cache_path)

        image_files = get_image_files(cache_path)

        image_number = 0
        total_frame = len(image_files)
        while True:
            cv2.destroyAllWindows()
            image = cv2.imread(image_files[image_number])

            image_name = f"Video [{i + 1}/{total_videos}] | Video Frame [{image_number}/{total_frame}]"
            cv2.imshow(image_name, image)
            cv2.moveWindow(image_name, 100, 100)

            key = cv2.waitKey(0)

            next_video, save_frame, image_number = handle_key(key, image_number, total_frame)
            if save_frame:
                save_frame_as_image(image, video_names[i], save_folder)
            if next_video:
                break

        cv2.destroyAllWindows()
        shutil.rmtree(cache_path)
        print("Cache folder deleted")


def read_video_frames(save_folder, video_folder):
    """
    Open video with indexing system.
    Cons:
    1. Slow and inconvenient
    """
    video_names = [video for video in os.listdir(video_folder) if video.endswith('.mp4')]
    total_videos = len(video_names)

    for i in range(total_videos):
        video_path = os.path.join(video_folder, video_names[i])

        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print("Error opening video file")
            return

        frame_number = 0
        total_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            cv2.destroyAllWindows()
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = video.read()

            if not ret:
                break

            frame_name = f"Video [{i + 1}/{total_videos}] | Video Frame [{frame_number}/{total_frame}]"
            cv2.imshow(frame_name, frame)
            cv2.moveWindow(frame_name, 100, 100)

            key = cv2.waitKey(0)

            next_video, save_frame, frame_number = handle_key(key, frame_number, total_frame)
            if save_frame:
                save_frame_as_image(frame, video_names[i], save_folder)
            if next_video:
                break

        video.release()
        cv2.destroyAllWindows()


save_image_path = r"C:\Users\user\PycharmProjects\Bottle-Detection\archive\images\video_images"
video_folder_path = r"C:\Users\user\PycharmProjects\Bottle-Detection\archive\videos"
read_video_frames_from_cache(save_image_path, video_folder_path)
