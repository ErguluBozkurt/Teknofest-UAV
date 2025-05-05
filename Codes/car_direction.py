import cv2
import numpy as np
from ultralytics import YOLO
import math

video_path = "car_video.mp4"
model_path = "best.pt"

cap = cv2.VideoCapture(video_path)
model = YOLO(model_path)

while True:
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
        results = model.track(frame, persist=True, verbose=False)[0]
        
        # print(results.keypoints.data.tolist())

        points = np.array(results.keypoints.data.tolist())

        for point in points:
            # print(point)
            for index in point:
                # print(index)
                cv2.circle(frame, (int(index[0]), int(index[1])), 5, (0, 0, 255), -1)
                

            try:
                cv2.circle(frame, (int(point[1][0]), int(point[1][1])), 5, (255, 0, 0), -1)
                cv2.circle(frame, (int(point[2][0]), int(point[2][1])), 5, (255, 0, 0), -1)
                x1=point[1][0]   
                y1=point[1][1]
                x2=point[2][0]   
                y2=point[2][1]
                derece = math.degrees(math.atan2(x2 - x1, y2 - y1))
                print(derece)
                if derece > 90 and derece < 180:
                    text = "Direction : Turn Left " + str(round(derece-90, 2)) + "'"
                    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
                    cv2.line(frame, (int(point[0][0]), int(point[0][1])), (int(point[0][0]) + 50, int(point[0][1]) + 50), (0, 255, 0), 5)
                    cv2.ellipse(frame, (int(point[0][0]) + 20, int(point[0][1]) + 20), (50, 50), 0, 30, 60, (0, 0, 255), 2)
                    cv2.ellipse(frame, (int(point[0][0]) + 30, int(point[0][1]) + 30), (50, 50), 0, 15, 80, (0, 0, 255), 2)
                    cv2.ellipse(frame, (int(point[0][0]) + 40, int(point[0][1]) + 40), (50, 50), 0, 0, 100, (0, 0, 255), 2)
                elif derece > -90 and derece < 0 :
                    text = "Direction : Turn Right " + str(round(90-derece, 2)) + "'"
                    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
                    cv2.line(frame, (int(point[0][0]), int(point[0][1])), (int(point[0][0]) - 50, int(point[0][1]) - 50), (0, 255, 0), 5)
                    cv2.ellipse(frame, (int(point[0][0]) - 20, int(point[0][1]) - 20), (50, 50), 0, 210, 240, (0, 0, 255), 2)
                    cv2.ellipse(frame, (int(point[0][0]) - 30, int(point[0][1]) - 30), (50, 50), 0, 195, 260, (0, 0, 255), 2)
                    cv2.ellipse(frame, (int(point[0][0]) - 40, int(point[0][1]) - 40), (50, 50), 0, 180, 280, (0, 0, 255), 2)
                elif derece < 90 and derece > 0 :
                    text = "Direction : Go Back " + str(round(90-derece, 2)) + "'"
                    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
                    cv2.line(frame, (int(point[0][0]), int(point[0][1])), (int(point[0][0]), int(point[0][1]) + 60), (0, 255, 0), 5)

                else:
                    cv2.putText(frame, "Direction : Go Straight", (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
                    cv2.line(frame, (int(point[0][0]), int(point[0][1])), (int(point[0][0]), int(point[0][1]) - 60), (0, 255, 0), 5)
                

            except:
                cv2.putText(frame, "Circle Detection Error", (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 1)

            


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Read Error")
        break

cap.release()
cv2.destroyAllWindows()
