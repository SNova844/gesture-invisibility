import cv2
# cv2 functions: cv2.VideoCapture(), cv2.imshow()

import mediapipe as mp

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


while True:
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



    result = segmenter.segment(mp_image)
    # AI 






    # gesture : check 
    gesture_result = gesture_recognizer.recognize(mp_image)

    if gesture_result.gestures:
        gesture = gesture_result.gestures[0][0]
        gesture_name = gesture.category_name

        print("Gesture:", gesture_name)

        if gesture_name == "Open_Palm":
            invisible = True

        elif gesture_name == "Closed_Fist":
            invisible = False










    mask = result.category_mask.numpy_view().squeeze()

    output_frame = frame.copy()

    if background is not None and invisible:
        person_mask = mask == 0

        person_mask = person_mask.astype("uint8") * 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        person_mask = cv2.dilate(person_mask, kernel, iterations=1)

        person_mask = person_mask > 0

        output_frame[person_mask] = background[person_mask]

    cv2.imshow("Invisibility Effect", output_frame)
   
    cv2.imshow("Segmentation Mask", mask )

    cv2.imshow("Gesture Invisibility", frame)
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

