# Source - https://stackoverflow.com/a
# Posted by sastanin, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-18, License - CC BY-SA 3.0

import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("preview", gray_frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
