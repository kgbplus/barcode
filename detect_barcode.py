# USAGE
# python detect_barcode.py
# python detect_barcode.py --video video/barcode_example.mov

# import the necessary packages
#from pyimagesearch import simple_barcode_detection
import argparse
import cv2
import numpy as np
import zbar


scanner = zbar.Scanner()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping over the frames
while True:
    # grab the current frame
    try:
        (grabbed, frame) = camera.read()
    except Exception as e:
        print(e)

    # check to see if we have reached the end of the
    # video
    if not grabbed:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect the barcode in the image
    results = scanner.scan(gray)
    for result in results:
        rect = cv2.minAreaRect(np.array(result.position))
        box = np.int0(cv2.boxPoints(rect))

        cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)

        text_x = int(rect[0][0] - 60)
        text_y = int(rect[0][1] + rect[1][1] * 0.5 + 25)
        cv2.putText(frame, result.data.decode('utf-8'),
                    (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # show the frame and record if the user presses a key
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
