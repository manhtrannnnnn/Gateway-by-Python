from gtts import gTTS
import os

def text_to_speech(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang='vi')
    tts.save(output_file)
    os.system("mpg321 " + output_file)  # Phát âm thanh bằng lệnh mpg321 trên Linux, bạn có thể thay đổi lệnh tương ứng cho hệ điều hành của mình

text = "Xin chào! Đây là một ví dụ về cách sử dụng gTTS trong Python để tạo ra âm thanh tiếng Việt."
text_to_speech(text)
