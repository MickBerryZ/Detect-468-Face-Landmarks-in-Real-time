import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("FaceMeshProject/Videos/travel4.mp4")
previousTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=2, circle_radius=2)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLandMarks in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(img, faceLandMarks, mpFaceMesh.FACE_CONNECTIONS)
            mpDraw.draw_landmarks(img, faceLandMarks, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
            for id, lm in enumerate(faceLandMarks.landmark):
                #  print(lm)
                 ih, iw, ic = img.shape
                 x,y = int(lm.x*iw), int(lm.y*ih)
                 print(id,x,y)
    
    
    
    
    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Image", img)
    # cv2.waitKey(60)
    cv2.waitKey(1) & 0xFF == ord('q')
    
    
