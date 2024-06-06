import tkinter as tk
from picamera2 import Picamera2, Preview
import io

# 루트 창 생성
root = tk.Tk()
root.title("파이캠 이미지 출력")

picam2 = Picamera2()

picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
time.sleep(2)


# 캔버스 생성
canvas_width = 640
canvas_height = 480
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# 이미지 출력 함수
def 이미지_출력():
  try:
    # 메모리 객체 생성
    output = io.BytesIO()

    # 카메라 캡처
    picam2.capture_file(output, format='jpeg')

    # 읽기 포인터 초기화
    output.seek(0)

    # 이미지 데이터 읽기
    image_data = output.read()

    # 이미지 객체 생성
    image = tk.PhotoImage(data=image_data)

    # 이미지 출력
    canvas.create_image(canvas_width // 2, canvas_height // 2, image=image)

  except Exception as e:
    print(f"오류 발생: {e}")

# 버튼 생성
capture_button = tk.Button(root, text="캡처", command=이미지_출력)
capture_button.pack()

# 루트 창 실행
root.mainloop()
