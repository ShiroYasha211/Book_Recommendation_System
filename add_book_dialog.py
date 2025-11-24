import customtkinter as ctk
from tkinter import messagebox
from library_manager import LibraryManager
from config import COLORS, FONTS, ICONS
from typing import Dict

class AddBookDialog(ctk.CTkToplevel):    
    def __init__(self, parent, library_manager: LibraryManager, colors: Dict):
        super().__init__(parent)
        
        self.parent = parent
        self.library_manager = library_manager
        self.colors = colors
        
        # إعداد النافذة
        self.setup_window()
        self.create_widgets()
        
        # التأكد من إغلاق النافذة
        self.transient(self.parent)
        self.grab_set()
        
    def setup_window(self):
        self.title("إضافة كتاب جديد لمكتبي")
        self.geometry("500x600")
        self.configure(fg_color=self.colors['surface'])
        
        # منع تغيير حجم النافذة
        self.resizable(False, False)
        
        # وضع النافذة في المنتصف
        self.after(200, lambda: self.focus_set())
    
    def create_widgets(self):
        # الإطار الرئيسي
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عنوان النافذة
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"{ICONS['add']} إضافة كتاب جديد",
            font=FONTS['title'],
            text_color=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))
        
        # عنوان الكتاب (مطلوب)
        ctk.CTkLabel(
            main_frame,
            text="عنوان الكتاب *",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.title_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="أدخل عنوان الكتاب",
            font=FONTS['body'],
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            height=40
        )
        self.title_entry.pack(fill="x", pady=(0, 15))
        
        # اسم المؤلف (مطلوب)
        ctk.CTkLabel(
            main_frame,
            text="اسم المؤلف *",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.author_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="أدخل اسم المؤلف",
            font=FONTS['body'],
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            height=40
        )
        self.author_entry.pack(fill="x", pady=(0, 15))
        
        # فئة الكتاب
        ctk.CTkLabel(
            main_frame,
            text="فئة الكتاب",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.category_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="مثال: Python، Java، Web Development",
            font=FONTS['body'],
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            height=40
        )
        self.category_entry.pack(fill="x", pady=(0, 15))
        
        # وصف الكتاب
        ctk.CTkLabel(
            main_frame,
            text="وصف الكتاب",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.description_text = ctk.CTkTextbox(
            main_frame,
            height=80,
            font=FONTS['body'],
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            scrollbar_button_color=self.colors['primary'],
            scrollbar_button_hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.description_text.pack(fill="x", pady=(0, 15))
        
        # تقييم شخصي
        ctk.CTkLabel(
            main_frame,
            text="التقييم الشخصي",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.rating_var = ctk.StringVar(value="0")
        rating_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        rating_frame.pack(fill="x", pady=(0, 15))
        
        for i in range(1, 6):
            ctk.CTkRadioButton(
                rating_frame,
                text=f"{'⭐' * i} ({i})",
                variable=self.rating_var,
                value=str(i),
                font=FONTS['body'],
                text_color=self.colors['text'],
                fg_color=self.colors['primary'],
                hover_color=self._adjust_color(self.colors['primary'], -0.2)
            ).pack(side="left", padx=(0, 10))
        
        # حالة القراءة
        ctk.CTkLabel(
            main_frame,
            text="حالة القراءة",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.reading_status_var = ctk.StringVar(value="لم أقرأ بعد")
        reading_status_menu = ctk.CTkOptionMenu(
            main_frame,
            variable=self.reading_status_var,
            values=["لم أقرأ بعد", "أقرأ حالياً", "مكتمل"],
            font=FONTS['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self._adjust_color(self.colors['primary'], -0.2),
            dropdown_fg_color=self.colors['surface'],
            text_color=self.colors['text']
        )
        reading_status_menu.pack(fill="x", pady=(0, 15))
        
        # العلامات
        ctk.CTkLabel(
            main_frame,
            text="العلامات",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(anchor="w", pady=(10, 5))
        
        self.tags_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="مثال: مبتدئ، متقدم، تطبيقي (مفصولة بفواصل)",
            font=FONTS['body'],
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            height=40
        )
        self.tags_entry.pack(fill="x", pady=(0, 20))
        
        # أزرار التحكم
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)
        
        # زر الإلغاء
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="إلغاء",
            command=self.on_cancel,
            font=FONTS['button'],
            fg_color=self.colors['error'],
            hover_color=self._adjust_color(self.colors['error'], -0.2),
            width=100,
            height=40
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # زر الحفظ
        save_btn = ctk.CTkButton(
            buttons_frame,
            text=f"{ICONS['success']} حفظ الكتاب",
            command=self.on_save,
            font=FONTS['button'],
            fg_color=self.colors['success'],
            hover_color=self._adjust_color(self.colors['success'], -0.2),
            width=120,
            height=40
        )
        save_btn.pack(side="right")
    
    def _adjust_color(self, color: str, factor: float) -> str:
        if color.startswith('#'):
            color = color[1:]
        
        # تحويل hex إلى RGB
        r = int(color[0:2], 16)
        g = int(color[2:4], 16) 
        b = int(color[4:6], 16)
        
        # تعديل القيم
        r = max(0, min(255, int(r + (factor * 255))))
        g = max(0, min(255, int(g + (factor * 255))))
        b = max(0, min(255, int(b + (factor * 255))))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_save(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        
        # التحقق من الحقول المطلوبة
        if not title:
            messagebox.showerror("خطأ", "عنوان الكتاب مطلوب")
            self.title_entry.focus()
            return
        
        if not author:
            messagebox.showerror("خطأ", "اسم المؤلف مطلوب")
            self.author_entry.focus()
            return
        
        # جمع البيانات
        category = self.category_entry.get().strip()
        description = self.description_text.get("1.0", "end-1c").strip()
        personal_rating = float(self.rating_var.get())
        reading_status = self.reading_status_var.get()
        tags = self.tags_entry.get().strip()
        
        # حفظ الكتاب
        try:
            book_id = self.library_manager.add_book(
                title=title,
                author=author,
                category=category,
                description=description,
                personal_rating=personal_rating,
                reading_status=reading_status,
                tags=tags
            )
            
            messagebox.showinfo(
                "نجح!", 
                f"تم إضافة الكتاب \"{title}\" إلى مكتبتك بنجاح!"
            )
            
            self.on_cancel()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الكتاب:\n{str(e)}")
    
    def on_cancel(self):
        self.destroy()