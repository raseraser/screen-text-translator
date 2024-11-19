import tkinter as tk
from tkinter import ttk
import pyautogui
import pytesseract
import time
from PIL import Image
from googletrans import Translator
import threading

class ScreenTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("螢幕文字翻譯器")
        self.root.geometry("600x400")
        
        # 設置視窗永遠置頂
        self.root.attributes('-topmost', True)
        
        # 創建介面元件
        self.create_widgets()
        
        # 初始化翻譯器
        self.translator = Translator()
        
        # 控制掃描的標誌
        self.scanning = False
        
    def create_widgets(self):
        # 控制按鈕
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=10)
        
        self.start_button = ttk.Button(self.control_frame, text="開始掃描", command=self.toggle_scan)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # 文字顯示區域
        self.text_frame = ttk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # 英文區域
        ttk.Label(self.text_frame, text="偵測到的英文:").pack(anchor=tk.W)
        self.english_text = tk.Text(self.text_frame, height=5)
        self.english_text.pack(fill=tk.X, pady=(0, 10))
        
        # 中文區域
        ttk.Label(self.text_frame, text="中文翻譯:").pack(anchor=tk.W)
        self.chinese_text = tk.Text(self.text_frame, height=5)
        self.chinese_text.pack(fill=tk.X)
        
    def toggle_scan(self):
        if not self.scanning:
            self.scanning = True
            self.start_button.configure(text="停止掃描")
            # 在新執行緒中開始掃描
            self.scan_thread = threading.Thread(target=self.scan_screen)
            self.scan_thread.daemon = True
            self.scan_thread.start()
        else:
            self.scanning = False
            self.start_button.configure(text="開始掃描")
            
    def scan_screen(self):
        while self.scanning:
            try:
                # 截取螢幕畫面
                screenshot = pyautogui.screenshot()
                
                # 使用OCR識別文字
                text = pytesseract.image_to_string(screenshot)
                
                # 如果有識別到文字
                if text.strip():
                    # 翻譯成中文
                    translation = self.translator.translate(text, dest='zh-tw')
                    
                    # 更新顯示
                    self.update_display(text, translation.text)
                
                # 等待1秒
                time.sleep(1)
                
            except Exception as e:
                print(f"Error: {e}")
                
    def update_display(self, eng_text, chi_text):
        # 使用 after 方法確保在主執行緒中更新 UI
        self.root.after(0, lambda: self.update_text_fields(eng_text, chi_text))
        
    def update_text_fields(self, eng_text, chi_text):
        # 清空文字區域
        self.english_text.delete(1.0, tk.END)
        self.chinese_text.delete(1.0, tk.END)
        
        # 插入新文字
        self.english_text.insert(tk.END, eng_text)
        self.chinese_text.insert(tk.END, chi_text)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenTranslator()
    app.run()