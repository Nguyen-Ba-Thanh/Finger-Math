# 
# Xử lý logic trò chơi toán học.
# Nguyên lý: Tạo phép tính → nhận số thứ nhất → nhận số thứ hai
# → nhận đáp án → so sánh với kết quả đúng → chuyển sang câu hỏi mới.
# 
import random
import time


class MathGame:

    def __init__(self):

        # Trạng thái game
        self.state = "WAIT_FIRST"

        # Hai số trong phép tính
        self.number1 = None
        self.number2 = None

        # Đáp án đúng
        self.correct_answer = None

        # Câu hỏi
        self.question = ""

        # Đáp án người chơi
        self.user_answer = None

        # Thời gian chờ giữa các lần nhập
        self.input_delay = 1.5

        # Thời điểm được phép nhận input tiếp theo
        self.next_input_time = 0

        # Điểm số
        self.score = 0

        # Tạo câu hỏi đầu tiên
        self.new_question()


    # TẠO CÂU HỎI
    def new_question(self):
         # Chọn phép tính
        self.operator = random.choice([
            "+",
            "-"
        ])
        
        # PHÉP CỘNG
        if self.operator == "+":
            self.number1 = random.randint(0, 5)
            self.number2 = random.randint(0, 5)

            self.correct_answer = (
                self.number1 + self.number2
            )
        else:

            self.number1 = random.randint(0, 10)

            # Đảm bảo number2 <= number1
            self.number2 = random.randint(
                0,
                self.number1
            )

            self.correct_answer = (
                self.number1 - self.number2
            )
        # Tạo câu hỏi
        self.question = (
            f"{self.number1} {self.operator} {self.number2} = ?"
        )

        # Trạng thái ban đầu
        self.state = "WAIT_FIRST"

        self.user_answer = None

        self.next_input_time = time.time()

    # KIỂM TRA CÓ ĐƯỢC NHẬN INPUT KHÔNG
    def can_accept_input(self):

        return time.time() >= self.next_input_time


    # BẮT ĐẦU DELAY
    def start_delay(self):

        self.next_input_time = (
            time.time() + self.input_delay
        )


    # NHẬP SỐ THỨ NHẤT
    def input_first_number(self, number):

        if self.state != "WAIT_FIRST":
            return False

        if not self.can_accept_input():
            return False

        if number == self.number1:

            print(
                f" Số thứ nhất đúng: {number}"
            )

            self.state = "WAIT_SECOND"

            self.start_delay()

            return True

        else:

            print(
                f"Số thứ nhất sai: {number}"
            )

            self.start_delay()

            return False


    # NHẬP SỐ THỨ HAI
    def input_second_number(self, number):

        if self.state != "WAIT_SECOND":
            return False

        if not self.can_accept_input():
            return False

        if number == self.number2:

            print(
                f" Số thứ hai đúng: {number}"
            )

            self.state = "WAIT_RESULT"

            self.start_delay()

            return True

        else:

            print(
                f" Số thứ hai sai: {number}"
            )

            self.start_delay()

            return False


    # NHẬP KẾT QUẢ

    def input_result(self, number):

        if self.state != "WAIT_RESULT":
            return False

        if not self.can_accept_input():
            return False

        self.user_answer = number

        if number == self.correct_answer:

            print("ĐÁP ÁN CHÍNH SÁC CHÍNH XÁC!")

            self.score +=1

            self.new_question()

            self.start_delay()

            return "CORRECT"

        else:

            print()
            print(" SAI!")

            print(
                f"Bạn nhập: {number}"
            )

            self.start_delay()

            return "WRONG!"


    # LẤY HƯỚNG DẪN CHO NGƯỜI CHƠI
    def get_instruction(self):

        if self.state == "WAIT_FIRST":

            return "SHOW FIRST NUMBER"

        elif self.state == "WAIT_SECOND":

            return "SHOW SECOND NUMBER"

        elif self.state == "WAIT_RESULT":

            return "SHOW YOUR ANSWER"

        return ""