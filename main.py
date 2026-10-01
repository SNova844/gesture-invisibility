import cv2
# cv2 functions: cv2.VideoCapture(), cv2.imshow()

import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# tasks - AI/computer-vision tools

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions




options = ImageSegmenterOptions(
    base_options=BaseOptions(
        # The AI model needed is inside models folder, and this is its filename
        # model_asset_path="models/selfie_segmenter_landscape.tflite"
        model_asset_path="models/selfie_segmenter.tflite"
    ),
    running_mode=VisionRunningMode.IMAGE,
    # process each webcam frame as an individual image
    output_category_mask=True
    # output segmentation mask
)





gesture_options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path="models/gesture_recognizer.task"
    ),
    running_mode=VisionRunningMode.IMAGE
)


segmenter = ImageSegmenter.create_from_options(options)
gesture_recognizer = GestureRecognizer.create_from_options(gesture_options)

camera = cv2.VideoCapture(0)
# VideoCapture(): get video from a camera 
# (0) -> zero means the laptop's default webcam

background = None
invisible = False
last_gesture = None
gesture_count = 0
gesture_name = "None"
previous_time = time.time()
frame_count = 0
fps_values = []


while True:

    frame_count += 1

    success, frame = camera.read()
    # camera.read(): ask for the next frame ( video - collection of frames displayed quickly)
    # openCV returns two pieces of information;
        # whether taking picture worked - success (true/ false)
        # the picture - frame

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # OpenCv stores image colors in BGR, but MediaPipe uses it in RGB (so conversion of colors)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )
    # turns OpenCV/NumPy image into a MediaPipe Image that MediaPipe knows how to process



    # result = segmenter.segment(mp_image)
    # AI 

    seg_start = time.time()

    result = segmenter.segment(mp_image)

    seg_time = (time.time() - seg_start) * 1000






    # gesture : check 
    # gesture_result = gesture_recognizer.recognize(mp_image)

    # fps optimization
    if frame_count % 2 == 0:
        gesture_start = time.time()

        gesture_result = gesture_recognizer.recognize(mp_image)

        gesture_time = (time.time() - gesture_start) * 1000

        if gesture_result.gestures:
            gesture = gesture_result.gestures[0][0]
            gesture_name = gesture.category_name
        
            # print("Gesture:", gesture_name)
        
            if gesture_name == last_gesture:
                gesture_count += 1
            else:
                last_gesture = gesture_name
                gesture_count = 1
        
            if gesture_count >= 5:
                if gesture_name == "Open_Palm":
                    invisible = True
        
                elif gesture_name == "Closed_Fist":
                    invisible = False

        else:
            gesture_name = "None"
            last_gesture = None
            gesture_count = 0


  

    
   









    mask = result.category_mask.numpy_view().squeeze()

    output_frame = frame.copy()

    if background is not None and invisible:
        person_mask = mask == 0

        person_mask = person_mask.astype("uint8") * 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        person_mask = cv2.dilate(person_mask, kernel, iterations=1)
        
        person_mask = person_mask > 0

        output_frame[person_mask] = background[person_mask]



    if invisible:
        status_text = "Status: INVISIBLE"
    else:
        status_text = "Status: VISIBLE"


    current_time = time.time()
    frame_time = current_time - previous_time
    fps = 1 / frame_time
    previous_time = current_time

    fps_values.append(fps)

    if len(fps_values) > 10:
        fps_values.pop(0)

    average_fps = sum(fps_values) / len(fps_values)

    if invisible:
        status_color = (0, 0, 255)  # Red
    else:
        status_color = (0, 255, 0)  # Green

    overlay = output_frame.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (450, 150),
        (0, 0, 0),
        -1
    )

    output_frame = cv2.addWeighted(
        overlay, 0.4,
        output_frame, 0.6,
        0
    )

    # cv2.putText -> draw text onto an image
    cv2.putText(
        output_frame,
        status_text,
        (20, 40), #text position
        cv2.FONT_HERSHEY_SIMPLEX,#font
        1, #font size
        status_color, #bgr color
        2 #thickness
    )

    cv2.putText(
        output_frame,
        "Gesture: " + gesture_name,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        output_frame,
        f"FPS: {average_fps:.1f}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        output_frame,
        "B: Capture Background | Q: Quit",
        (20,145 ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )


    if background is None:
        cv2.putText(
            output_frame,
            "Move out of frame and press B to capture background",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )
         
    cv2.imshow("Invisibility Effect", output_frame)
   
    # cv2.imshow("Segmentation Mask", mask )

    # cv2.imshow("Gesture Invisibility", frame)
    # opens the window to show the frame

    key = cv2.waitKey(1) & 0xFF

    if key == ord("b"):
        background = frame.copy()
        print("Background captured!")

    if key == ord("q"):
        # if q is pressed (break: getting out of the loop)
        break


camera.release()
# turn off the window 
 

cv2.destroyAllWindows()
# Close all the windows you created

