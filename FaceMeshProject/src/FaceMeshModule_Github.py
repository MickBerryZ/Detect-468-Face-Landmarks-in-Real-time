import cv2
import mediapipe as mp
import time

class findhand():
    def __init__(self, mode=False, maxHands=2, detectionCon=False
             ,trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(self.mode, self.maxHands
                                        ,self.detectionCon
                                        ,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

class findFace():
    def __init__(self, mode=False, maxFaces=1, detectionCon=False
               ,trackCon=0.5):
        self.mode = mode
        self.maxFaces = maxFaces
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpFaceMesh = mp.solutions.face_mesh

        self.face_mesh = self.mpFaceMesh.FaceMesh(self.mode
                                                 ,self.maxFaces
                                                 ,self.detectionCon
                                                 ,self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(imgRGB)

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms,
                                               self.mpFaceMesh.FACE_CONNECTIONS)

        return img

class findPose():
    def __init__(self, mode=False, complexity=1,detectionCon=0.5,landmarks=True
                 ,trackCon=0.5):
        self.mode = mode
        self.maxFace = 1
        self.detectionCon = 0.5
        self.trackCon = 0.5
        self.landmarks = landmarks
        self.complexity = complexity
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(self.mode, self.complexity
                                         ,self.detectionCon
                                         ,self.trackCon
                                         ,self.landmarks)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.result.pose_landmarks:
            PoseLms = self.results.pose_landmarks
            mpDraw.draw_landmarks(img, PoseLms, self.mpPose.POSE_CONNECTIONS,
                                  drawSpec, drawSpec)

        return img

def main():

    cTime, pTime = 0, 0

    hand_detector = findhand()
    face_detector = findFace()
    pose_detector = findPose()

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:

        success, img = cap.read()
        img = face_detector.findFace(img)
        if not success:
            print("GPU Didn't Success At Loading Video")
            continue

        handlmList = hand_detector.findHands(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Detector", img)

        if cv2.waitKey(1) != -1:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()