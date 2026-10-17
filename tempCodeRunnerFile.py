
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Game variables
ship_x, ship_y = 400, 300

while True:
    # --- Part A: Get Webcam & AI Tracking Data ---
    success, frame = cap.read()