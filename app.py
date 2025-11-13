import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from main_app import MainApplication

def main():
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("blue")  
    
    try:
        app = MainApplication()
        app.mainloop()
        
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {e}")
        
        # إنشاء نافذة خطأ بسيطة
        root = ctk.CTk()
        root.title("خطأ في التشغيل")
        root.geometry("400x200")
        
        error_label = ctk.CTkLabel(
            root,
            text=f"حدث خطأ في تشغيل التطبيق:\n\n{str(e)}\n\nتأكد من تثبيت جميع المكتبات المطلوبة:\npip install -r requirements.txt",
            font=("Arial", 14),
            wraplength=350
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        root.mainloop()

if __name__ == "__main__":
    main()