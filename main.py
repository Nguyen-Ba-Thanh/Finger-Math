import cv2
import mediapipe as mp
from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from finger_counter import count_fingers
from input_stabilizer import NumberStabilizer
from math_game import MathGame



# MODEL
MODEL_PATH = Path(__file__).parent / "hand_landmarker.task"

# MEDIAPIPE
base_options = python.BaseOptions(
    model_asset_path=str(MODEL_PATH)
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)

hand_landmarker = vision.HandLandmarker.create_from_options(
    options
)

# WEBCAM
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không thể mở webcam!")
    exit()

# STABILIZER
input_stabilizer = NumberStabilizer(
    required_frames=10
)


# GAME
game = MathGame()

# BIẾN GIAO DIỆN
result_message = ""
result_timer = 0

# RESET STABILIZER
def reset_stabilizer():
    input_stabilizer.current_number = None
    input_stabilizer.stable_frames = 0
    input_stabilizer.confirmed = False
    input_stabilizer.no_hand_frames = 0

# HÀM VẼ PANEL
def draw_panel(
    frame,
    x1,
    y1,
    x2,
    y2
):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        (30, 30, 30),
        -1
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.75,
        frame,
        0.25,
        0
    )


# DRAW TEXT
def draw_text(
    frame,
    text,
    position,
    font_scale=0.7,
    color=(255, 255, 255),
    thickness=2
):

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA
    )

# MAIN WINDOW
cv2.namedWindow(
    "Finger Math",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "Finger Math",
    1280,
    720
)

# MAIN LOOP
while True:
    # READ CAMERA
    ret, frame = cap.read()

    if not ret:

        print("Không thể đọc webcam!")
        break


    # lật camera giống gương
    frame = cv2.flip(
        frame,
        1
    )

    # FRAME SIZE
    h, w, _ = frame.shape

    # CHUYỂN BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # TẠO MEDIAPIPE IMAGE
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # DETECT HAND
    result = hand_landmarker.detect(
        mp_image
    )

    # BIẾN LƯU TRẠNG THÁI TAY
    left_count = 0
    right_count = 0

    left_hand_detected = False
    right_hand_detected = False

    # XỬ LÝ CÁC BÀN TAY   
    if result.hand_landmarks:

        for hand_landmarks in result.hand_landmarks:

            # XÁC ĐỊNH VỊ TRÍ TAY TRÊN MÀN HÌNH
            # x < 0.5  → bên trái màn hình
            # x >= 0.5 → bên phải màn hình
            
            wrist = hand_landmarks[0]
            if wrist.x < 0.5:
                side = "LEFT"
            else:
                side = "RIGHT"
            
            # ĐẾM NGÓN
    
            finger_count = count_fingers(
                hand_landmarks,
                side
            )

            # LƯU SỐ NGÓN
            if side == "LEFT":

                left_count = finger_count
                left_hand_detected = True

            else:

                right_count = finger_count
                right_hand_detected = True

            # VẼ LANDMARK
            for index, landmark in enumerate(
                hand_landmarks
            ):
                x = int(
                    landmark.x * w
                )
                y = int(
                    landmark.y * h
                )
                
                # Vẽ điểm landmark
                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (255,0, 0),
                    -1
                )

                # Vẽ số landmark
                cv2.putText(
                    frame,
                    str(index),
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA
                )


    # TÍNH TỔNG 2 TAY
    # Không có tay: = 0

    total_count = (
        left_count + right_count
    )

    # STABILIZER
    # Kiểm tra hands
    if (
        left_hand_detected
        or right_hand_detected
    ):

        confirmed_number = (
            input_stabilizer.update(
                total_count
            )
        )

    else:

        confirmed_number = (
            input_stabilizer.update(
                None
            )
        )


    # GAME STATE
    if game.state == "WAIT_FIRST":

        if confirmed_number is not None:
            game.input_first_number(
                confirmed_number
            )

            reset_stabilizer()


    elif game.state == "WAIT_SECOND":

        if confirmed_number is not None:
            game.input_second_number(
                confirmed_number
            )

            reset_stabilizer()


    elif game.state == "WAIT_RESULT":

        if confirmed_number is not None:

            result = game.input_result(confirmed_number)

            if result == "CORRECT":
                result_message = "CORRECT!"
                result_timer = 60

            elif result == "WRONG!":
                result_message = "WRONG!"
                result_timer = 60

            reset_stabilizer()

    
    # RESULT TIMER
    if result_timer > 0:

        result_timer -= 1

    else:

        result_message = ""

    # INSTRUCTION
    if game.state == "WAIT_FIRST":

        instruction = (
            "SHOW FIRST NUMBER"
        )

    elif game.state == "WAIT_SECOND":

        instruction = (
            "SHOW SECOND NUMBER"
        )

    elif game.state == "WAIT_RESULT":

        instruction = (
            "SHOW YOUR ANSWER"
        )

    else:

        instruction = ""

# draw
    # TOP PANEL
    draw_panel(
        frame,
        20,
        20,
        290,
        320
    )

    # QUESTION
    draw_text(
        frame,
        game.question,
        (45, 75),
        font_scale=1.3,
        color=(0, 255, 255),
        thickness=3
    )

    # INSTRUCTION
    draw_text(
        frame,
        instruction,
        (45, 120),
        font_scale=0.65,
        color=(255, 255, 255),
        thickness=2
    )

    # SCORE
    draw_text(
        frame,
        f"SCORE: {game.score}",
        (45, 165),
        font_scale=0.75,
        color=(255, 215, 0),
        thickness=2
    )

    # LEFT HAND
    draw_text(
        frame,
        f"LEFT HAND : {left_count}",
        (45, 210),
        font_scale=0.65,
        color=(255, 255, 255),
        thickness=2
    )


    #  RIGHT HAND
    draw_text(
        frame,
        f"RIGHT HAND: {right_count}",
        (45, 250),
        font_scale=0.65,
        color=(255, 255, 255),
        thickness=2
    )

    # TOTAL
    draw_text(
        frame,
        f"TOTAL: {total_count}",
        (45, 295),
        font_scale=0.8,
        color=(0, 255, 0),
        thickness=2
    )

    # GAME INFORMATION
    draw_panel(
        frame,
        20,
        340,
        290,
        510
    )

    draw_text(
        frame,
        f"NUMBER 1: {game.number1}",
        (45, 385),
        font_scale=0.65,
        thickness=2
    )


    draw_text(
        frame,
        f"NUMBER 2: {game.number2}",
        (45, 425),
        font_scale=0.65,
        thickness=2
    )


    draw_text(
        frame,
        f"ANSWER  : ?",
        (45, 465),
        font_scale=0.65,
        thickness=2
    )

    # RESULT MESSAGE
    if result_message != "":

        color = (
            (0, 255, 0)
            if result_message == "CORRECT!"
            else
            (0, 0, 255)
        )

        draw_text(
            frame,
            result_message,
            (w // 2 - 100, h - 70),
            font_scale=1.2,
            color=color,
            thickness=3
        )

    # QUIT
    draw_text(
        frame,
        "Press Q to quit",
        (w - 180, h - 20),
        font_scale=0.5,
        color=(200, 200, 200),
        thickness=1
    )
  
    # SHOW
    cv2.imshow(
        "Finger Math",
        frame
    )

    # KEYBOARD
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break

# RELEASE

cap.release()

cv2.destroyAllWindows()

hand_landmarker.close()