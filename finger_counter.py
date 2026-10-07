# 
# Đếm số ngón tay.
# Nguyên lý: Dựa vào vị trí các landmark của bàn tay,
# so sánh vị trí đầu ngón với các khớp để xác định ngón đang duỗi.
# 
def count_fingers(hand_landmarks, side):
    count = 0
    # Ngón cái
    if side == "LEFT":
        # Tay bên trái màn hình
        if hand_landmarks[4].x > hand_landmarks[3].x:
            count += 1

    elif side == "RIGHT":
        # Tay bên phải màn hình
        if hand_landmarks[4].x < hand_landmarks[3].x:
            count += 1

    # Ngón trỏ
    if hand_landmarks[8].y < hand_landmarks[6].y:
        count += 1

    # Ngón giữa
    if hand_landmarks[12].y < hand_landmarks[10].y:
        count += 1

    # Ngón áp út
    if hand_landmarks[16].y < hand_landmarks[14].y:
        count += 1

    # Ngón út
    if hand_landmarks[20].y < hand_landmarks[18].y:
        count += 1

    return count