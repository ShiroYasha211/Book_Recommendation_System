import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable
from config import COLORS, FONTS, ICONS, CARD_CONFIG

class BookCard(ctk.CTkFrame):
    
    def __init__(self, parent, book_data: Dict, on_click: Callable = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.book_data = book_data
        self.on_click = on_click
        self.colors = COLORS['dark']  # استخدام الوضع الداكن
        self.setup_ui()
        
        # ربط الحدث النقر
        self.bind("<Button-1>", self._on_card_click)
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
        
        # تعيين العلامة النقرية
        self.configure(cursor="hand2")
    
    def setup_ui(self):
        """إعداد واجهة البطاقة"""
        # إزالة الإطار الافتراضي وإضافة ظل
        self.configure(
            width=CARD_CONFIG['width'], 
            height=CARD_CONFIG['height'],
            fg_color=self.colors['surface'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=CARD_CONFIG['border_radius']
        )
        
        # إنشاء تخطيط البطاقة
        self.grid_columnconfigure(1, weight=1)
        
        # أيقونة الكتاب
        self.book_icon_label = ctk.CTkLabel(
            self,
            text=ICONS['book'],
            font=ctk.CTkFont(size=24),
            text_color=self.colors['primary']
        )
        self.book_icon_label.grid(row=0, column=0, padx=15, pady=15, sticky="nw")
        
        # عنوان الكتاب
        self.title_label = ctk.CTkLabel(
            self,
            text=self.truncate_text(self.book_data['title'], 35),
            font=FONTS['subtitle'],
            text_color=self.colors['text'],
            anchor="w"
        )
        self.title_label.grid(row=0, column=1, columnspan=2, padx=(0, 15), pady=(15, 5), sticky="ew")
        
        # معلومات الكتاب
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=1, column=1, columnspan=2, padx=(0, 15), pady=5, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # المؤلف
        self.author_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['author']} {self.truncate_text(self.book_data['author'], 25)}",
            font=FONTS['small'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        self.author_label.grid(row=0, column=0, padx=(0, 10), pady=2, sticky="w")
        
        # الفئة
        self.category_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['category']} {self.book_data['category']}",
            font=FONTS['small'],
            text_color=self.colors['secondary'],
            anchor="w"
        )
        self.category_label.grid(row=0, column=1, padx=10, pady=2, sticky="w")
        
        # التقييم والسنة
        rating_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        rating_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        
        # النجوم
        stars = "⭐" * int(self.book_data['rating'])
        self.rating_label = ctk.CTkLabel(
            rating_frame,
            text=f"{stars} {self.book_data['rating']:.1f} ({self.book_data['rating_category']})",
            font=FONTS['small'],
            text_color=self.colors['warning'],
            anchor="w"
        )
        self.rating_label.pack(side="left")
        
        # السنة
        self.year_label = ctk.CTkLabel(
            rating_frame,
            text=f"{ICONS['year']} {self.book_data['year']}",
            font=FONTS['small'],
            text_color=self.colors['text_secondary'],
            anchor="e"
        )
        self.year_label.pack(side="right")
        
        # الوصف (مختصر)
        if self.book_data['description'] and self.book_data['description'] != 'لا يوجد وصف':
            self.description_label = ctk.CTkLabel(
                self,
                text=self.truncate_text(self.book_data['description'], 80),
                font=FONTS['small'],
                text_color=self.colors['text_secondary'],
                anchor="w",
                wraplength=280
            )
            self.description_label.grid(row=2, column=0, columnspan=3, padx=15, pady=5, sticky="ew")
        
        # علامات الصعوبة والتقييم
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=3, column=0, columnspan=3, padx=15, pady=(5, 15), sticky="ew")
        
        # مستوى الصعوبة
        difficulty_color = self._get_difficulty_color(self.book_data['difficulty'])
        self.difficulty_label = ctk.CTkLabel(
            bottom_frame,
            text=f"{ICONS['difficulty']} {self.book_data['difficulty']}",
            font=FONTS['small'],
            text_color=difficulty_color,
            anchor="w"
        )
        self.difficulty_label.pack(side="left")
        
        # عدد الصفحات
        pages_color = self._get_pages_color(self.book_data['pages'])
        self.pages_label = ctk.CTkLabel(
            bottom_frame,
            text=f"{ICONS['pages']} {self.book_data['pages']} صفحة",
            font=FONTS['small'],
            text_color=pages_color,
            anchor="e"
        )
        self.pages_label.pack(side="right")
    
    def truncate_text(self, text: str, max_length: int) -> str:
        """تقصير النص إذا كان طويلاً"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _get_difficulty_color(self, difficulty: str) -> str:
        """الحصول على لون مستوى الصعوبة"""
        colors = {
            'مبتدئ': self.colors['success'],
            'متوسط': self.colors['warning'], 
            'متقدم': self.colors['error']
        }
        return colors.get(difficulty, self.colors['text_secondary'])
    
    def _get_pages_color(self, pages: int) -> str:
        """الحصول على لون عدد الصفحات"""
        if pages < 300:
            return self.colors['success']
        elif pages < 600:
            return self.colors['warning']
        else:
            return self.colors['error']
    
    def _on_card_click(self, event):
        """حدث النقر على البطاقة"""
        if self.on_click:
            self.on_click(self.book_data)
    
    def _on_hover_enter(self, event):
        """حدث تمرير الماوس فوق البطاقة"""
        self.configure(
            border_color=self.colors['accent'],
            fg_color=self._adjust_color(self.colors['surface'], 0.1)
        )
    
    def _on_hover_leave(self, event):
        """حدث مغادرة الماوس للبطاقة"""
        self.configure(
            border_color=self.colors['border'],
            fg_color=self.colors['surface']
        )
    
    def _adjust_color(self, color: str, factor: float) -> str:
        """تعديل لون (تبسيط)"""
        # تحويل بسيط للون - في التطبيق الحقيقي سنستخدم مكتبة الألوان
        if color == self.colors['surface']:
            return "#353535"
        return color


class BookDetailsDialog(ctk.CTkToplevel):
    """نافذة تفاصيل الكتاب"""
    
    def __init__(self, parent, book_data: Dict):
        super().__init__(parent)
        
        self.book_data = book_data
        self.colors = COLORS['dark']
        self.setup_window()
        self.create_details_ui()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.title(f"تفاصيل كتاب: {self.book_data['title']}")
        self.geometry("600x700")
        self.configure(fg_color=self.colors['background'])
        
        # جعل النافذة في المنتصف
        self.transient(self.master)
        self.grab_set()
        
        # زر الإغلاق
        close_btn = ctk.CTkButton(
            self,
            text="إغلاق",
            command=self.destroy,
            font=FONTS['button'],
            fg_color=self.colors['error'],
            hover_color=self._adjust_color(self.colors['error'], -0.2)
        )
        close_btn.pack(pady=20)
    
    def create_details_ui(self):
        """إنشاء واجهة التفاصيل"""
        # إطارج الرئيسية للتمرير
        main_frame = ctk.CTkScrollableFrame(
            self,
            width=580,
            height=600,
            fg_color=self.colors['surface']
        )
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # عنوان الكتاب
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"{ICONS['book']} {self.book_data['title']}",
            font=FONTS['title'],
            text_color=self.colors['primary'],
            wraplength=540
        )
        title_label.pack(pady=15)
        
        # معلومات أساسية
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # المؤلف
        author_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['author']} المؤلف: {self.book_data['author']}",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        author_label.pack(fill="x", pady=5)
        
        # الفئة
        category_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['category']} الفئة: {self.book_data['category']}",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        category_label.pack(fill="x", pady=5)
        
        # التقييم
        stars = "⭐" * int(self.book_data['rating'])
        rating_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['rating']} التقييم: {stars} {self.book_data['rating']:.1f} ({self.book_data['rating_category']})",
            font=FONTS['body'],
            text_color=self.colors['warning'],
            anchor="w"
        )
        rating_label.pack(fill="x", pady=5)
        
        # اللغة البرمجية
        language_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONS['language']} اللغة: {self.book_data['language']}",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        language_label.pack(fill="x", pady=5)
        
        # السنة والصفحات
        details_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
        details_frame.pack(fill="x", padx=20, pady=10)
        
        year_label = ctk.CTkLabel(
            details_frame,
            text=f"{ICONS['year']} سنة النشر: {self.book_data['year']}",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        year_label.pack(fill="x", padx=15, pady=5)
        
        pages_label = ctk.CTkLabel(
            details_frame,
            text=f"{ICONS['pages']} عدد الصفحات: {self.book_data['pages']} صفحة",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        pages_label.pack(fill="x", padx=15, pady=5)
        
        # مستوى الصعوبة
        difficulty_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
        difficulty_frame.pack(fill="x", padx=20, pady=10)
        
        difficulty_color = self._get_difficulty_color(self.book_data['difficulty'])
        difficulty_label = ctk.CTkLabel(
            difficulty_frame,
            text=f"{ICONS['difficulty']} مستوى الصعوبة: {self.book_data['difficulty']}",
            font=FONTS['body'],
            text_color=difficulty_color,
            anchor="w"
        )
        difficulty_label.pack(fill="x", padx=15, pady=5)
        
        # الوصف
        if self.book_data['description'] and self.book_data['description'] != 'لا يوجد وصف':
            desc_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
            desc_frame.pack(fill="x", padx=20, pady=10)
            
            desc_title = ctk.CTkLabel(
                desc_frame,
                text=f"{ICONS['info']} الوصف:",
                font=FONTS['subtitle'],
                text_color=self.colors['secondary'],
                anchor="w"
            )
            desc_title.pack(fill="x", padx=15, pady=(10, 5))
            
            desc_text = ctk.CTkLabel(
                desc_frame,
                text=self.book_data['description'],
                font=FONTS['body'],
                text_color=self.colors['text'],
                anchor="w",
                wraplength=540,
                justify="right"
            )
            desc_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # العلامات
        if self.book_data['tags']:
            tags_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
            tags_frame.pack(fill="x", padx=20, pady=10)
            
            tags_title = ctk.CTkLabel(
                tags_frame,
                text=f"{ICONS['filter']} العلامات:",
                font=FONTS['subtitle'],
                text_color=self.colors['secondary'],
                anchor="w"
            )
            tags_title.pack(fill="x", padx=15, pady=(10, 5))
            
            tags_text = ctk.CTkLabel(
                tags_frame,
                text=self.book_data['tags'],
                font=FONTS['body'],
                text_color=self.colors['text'],
                anchor="w",
                wraplength=540
            )
            tags_text.pack(fill="x", padx=15, pady=(0, 10))
    
    def _get_difficulty_color(self, difficulty: str) -> str:
        colors = {
            'مبتدئ': self.colors['success'],
            'متوسط': self.colors['warning'],
            'متقدم': self.colors['error']
        }
        return colors.get(difficulty, self.colors['text_secondary'])
    
    def _adjust_color(self, color: str, factor: float) -> str:
        return color