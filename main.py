import cv2
import mediapipe as mp
import subprocess
import time
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
start_time = time.time()
song_started = False

while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, _ = img.shape

    left_distance = None
    right_distance = None

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_type = results.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
            landmark_list = hand_landmarks.landmark

            # Thumb (ID 4) and Index (ID 8)
            thumb = landmark_list[4]
            index = landmark_list[8]

            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            index_x, index_y = int(index.x * w), int(index.y * h)

            # Draw thumb and index
            cv2.circle(img, (thumb_x, thumb_y), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 0), 2)

            # Calculate distance
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            if hand_type == "Left":
                left_distance = distance
            elif hand_type == "Right":
                right_distance = distance

    # Show both distances and map left hand to speed
    font_scale = 1.0
    font_thickness = 2
    color = (0, 255, 255)

    if left_distance is not None:
        # Calculate speed: distance 50–200 px maps to 0.5x–2.0x
        speed = max(0.5, min(2.0, left_distance / 100))
        # Write speed to file
        with open("speed.txt", "w") as f:
            f.write(str(speed))

        # Display distance + speed on screen
        cv2.putText(img, f"Left: {int(left_distance)} px  Speed: {speed:.2f}x",
                    (30, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)

    if right_distance is not None:
        cv2.putText(img, f"Right: {int(right_distance)} px",
                    (w - 300, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)

    # Show webcam feed
    cv2.imshow("Hand Tracking", img)

    # Auto-launch song after 10 seconds
    if not song_started and (time.time() - start_time) > 10:
        print("🎶 Starting song...")
        subprocess.Popen(["python", "song.py"])
        song_started = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
