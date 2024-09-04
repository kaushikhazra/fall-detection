import cv2

test_video = "test-videos/fall/cam1.avi"

cap = cv2.VideoCapture(test_video)
fgbgMOG2 = cv2.createBackgroundSubtractorMOG2()
fgbgKNN = cv2.createBackgroundSubtractorKNN()

if not cap.isOpened():
    print('Error: Could not open camera.')
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print('Error: Could not read frame.')
        break

    fgmaskMOG = fgbgMOG2.apply(frame)
    fgmaskKNN = fgbgKNN.apply(frame)

    cv2.imshow('Background Subtraction MOG', fgmaskMOG)
    cv2.imshow('Background Subtraction KNN', fgmaskKNN)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()