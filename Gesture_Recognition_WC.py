import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.complexity = complexity
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        self.handType = None  # Store handedness

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

        # Get handedness (Left or Right)
            if self.results.multi_handedness:
                self.handType = self.results.multi_handedness[handNo].classification[0].label

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 255), cv2.FILLED)

        return self.lmList


    def fingersUp(self):
        fingers = []
        if len(self.lmList) == 0:
            return [0, 0, 0, 0, 0]

    # Thumb logic based on left/right hand
        if self.handType == "Left":
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:  # Left hand
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

    #  Other fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

# New function to identify gestures
def detectGesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return " OFF"
    elif fingers == [1, 1, 1, 1, 1]:
        return " ON"
    elif fingers == [0, 1, 0, 0, 0]:
        return " Increase Speed (Fan)"
    elif fingers == [0, 1, 1, 1, 0]:
        return " Maximum Speed (Fan)"
    elif fingers == [0, 1, 1, 0, 0]:
        return " Decrease Speed (Fan)"
    else:
        return "Unknown Gesture"





def main():
    pTime = 0
    cap = cv2.VideoCapture(1)  
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        gesture = ""

        if len(lmList) != 0:
            fingers = detector.fingersUp()
            gesture = detectGesture(fingers)

        # FPS and Display
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f'Gesture: {gesture}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, "Press 'q' to quit", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 255), 2)

        cv2.imshow("Hand Gesture Recognition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()












