# 
# Ổn định dữ liệu đầu vào.
# Nguyên lý: Kiểm tra kết quả có giống nhau trong nhiều frame liên tiếp hay không,
# chỉ xác nhận khi kết quả đủ ổn định.
# 
class NumberStabilizer:

    def __init__(self, required_frames):
        # Cần số giống nhau trong bao nhiêu frame
        self.required_frames = required_frames

        # Số hiện tại
        self.current_number = None

        # Số frame liên tiếp giữ nguyên
        self.stable_frames = 0

        # Đã xác nhận số này chưa
        self.confirmed = False

        # Số frame không phát hiện tay
        self.no_hand_frames = 0

    def update(self, number):

        # KHÔNG PHÁT HIỆN TAY
        if number is None:

            self.no_hand_frames += 1

            # Nếu không thấy tay trong 5 frame
            # thì cho phép nhập số mới
            if self.no_hand_frames >= 5:
                self.current_number = None
                self.stable_frames = 0
                self.confirmed = False

            return None

        # Có tay trở lại
        self.no_hand_frames = 0

        # SỐ GIỐNG FRAME TRƯỚC
        if number == self.current_number:
            self.stable_frames += 1

        # SỐ THAY ĐỔI
        else:
            self.current_number = number
            self.stable_frames = 1
            self.confirmed = False

        # XÁC NHẬN
        if (
            self.stable_frames >= self.required_frames
            and not self.confirmed
        ):
            self.confirmed = True

            return number

        return None