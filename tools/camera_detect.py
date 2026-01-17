import cv2

for index in range(5):
    cap = cv2.VideoCapture(index)
    if cap.read()[0]:
        print(f"\033[92m[{index}] : Available\033[0m")
        cap.release()
    else:
        print(f"\033[91m[{index}] : Unavailable\033[0m")