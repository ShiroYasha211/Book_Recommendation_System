import customtkinter as ctk
from tkinter import messagebox
from library_manager import LibraryManager
from config import COLORS, FONTS, ICONS
from typing import Dict

class MyLibraryWindow(ctk.CTkToplevel):
    
    def __init__(self, parent, library_manager: LibraryManager, colors: Dict):
        super().__init__(parent)
        
        self.parent = parent
        self.library_manager = library_manager
        self.colors = colors
        self.all_books = []
        self.filtered_books = []
        
        # إعداد النافذة
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات
        self.refresh_books()
        
        # التأكد من إغلاق النافذة
        self.transient(self.parent)
        self.grab_set()
        
    def setup_window(self):
        """إعداد النافذة"""
        self.title("مكتبتي الشخصية")
        self.geometry("800x600")
        self.minsize(600, 400)
        self.configure(fg_color=self.colors['background'])
        
        # إغلاق النافذة عند الضغط على X
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        # الإطار الرئيسي
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عنوان النافذة
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"{ICONS['book']} مكتبتي الشخصية",
            font=FONTS['title'],
            text_color=self.colors['primary']
        )
        title_label.pack(side="left")
        
        # زر الإحصائيات
        stats_btn = ctk.CTkButton(
            title_frame,
            text=f"{ICONS['statistics']} إحصائيات",
            command=self.show_statistics,
            font=FONTS['button'],
            fg_color=self.colors['secondary'],
            hover_color=self._adjust_color(self.colors['secondary'], -0.2),
            width=100,
            height=35
        )
        stats_btn.pack(side="right")
        
        # شريط البحث
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            search_frame,
            text=f"{ICONS['search']} البحث:",
            font=FONTS['body'],
            text_color=self.colors['text']
        ).pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث في عنوان الكتاب أو المؤلف أو العلامات...",
            font=FONTS['body'],
            fg_color=self.colors['surface'],
            border_color=self.colors['border'],
            text_color=self.colors['text'],
            height=40
        )
        self.search_entry.pack(fill="x", padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # عدد النتائج
        self.results_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=FONTS['body'],
            text_color=self.colors['text_secondary']
        )
        self.results_label.pack(anchor="w", pady=(0, 10))
        
        # إطار الكتب
        self.books_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=self.colors['surface']
        )
        self.books_frame.pack(fill="both", expand=True)
        
        # رسالة عدم وجود كتب
        self.no_books_label = ctk.CTkLabel(
            main_frame,
            text=f"{ICONS['info']} مكتبتك فارغة حالياً\nقم بإضافة كتب جديدة من النافذة الرئيسية",
            font=FONTS['body'],
            text_color=self.colors['text_secondary'],
            justify="center"
        )
    
    def refresh_books(self):
        """تحديث قائمة الكتب"""
        self.all_books = self.library_manager.get_all_books()
        self.filtered_books = self.all_books.copy()
        self.display_books()
    
    def on_search_change(self, event=None):
        """معالجة تغيير نص البحث"""
        query = self.search_entry.get().strip()
        
        if not query:
            self.filtered_books = self.all_books.copy()
        else:
            self.filtered_books = self.library_manager.search_books(query)
        
        self.display_books()
    
    def display_books(self):
        """عرض قائمة الكتب"""
        # مسح الكتب السابقة
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        
        # عرض رسالة عدم وجود كتب
        if not self.filtered_books:
            if self.search_entry.get().strip():
                self.no_books_label.configure(
                    text=f"{ICONS['info']} لم يتم العثور على نتائج للبحث\nجرب كلمات بحث مختلفة"
                )
            else:
                self.no_books_label.configure(
                    text=f"{ICONS['info']} مكتبتك فارغة حالياً\nقم بإضافة كتب جديدة من النافذة الرئيسية"
                )
            self.no_books_label.pack(expand=True)
            self.results_label.configure(text="")
            return
        
        # إخفاء رسالة عدم وجود كتب
        self.no_books_label.pack_forget()
        
        # تحديث عدد النتائج
        total_text = f"📚 عدد الكتب: {len(self.filtered_books)} من أصل {len(self.all_books)}"
        if self.search_entry.get().strip():
            total_text += f" | 🔍 البحث: '{self.search_entry.get().strip()}'"
        self.results_label.configure(text=total_text)
        
        # عرض الكتب
        for book in self.filtered_books:
            self.create_book_card(book)
    
    def create_book_card(self, book: Dict):
        """إنشاء بطاقة كتاب"""
        book_frame = ctk.CTkFrame(
            self.books_frame,
            fg_color=self.colors['background'],
            border_color=self.colors['border'],
            border_width=1
        )
        book_frame.pack(fill="x", pady=5, padx=5)
        
        # الإطار الداخلي
        inner_frame = ctk.CTkFrame(book_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # عنوان الكتاب
        title_label = ctk.CTkLabel(
            inner_frame,
            text=f"{ICONS['book']} {book['title']}",
            font=("Helvetica", 16, "bold"),
            text_color=self.colors['primary'],
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))
        
        # المؤلف
        author_label = ctk.CTkLabel(
            inner_frame,
            text=f"{ICONS['author']} {book['author']}",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        author_label.pack(fill="x", pady=(0, 8))
        
        # معلومات إضافية
        info_text = ""
        if book['category']:
            info_text += f"{ICONS['category']} {book['category']} | "
        if book['personal_rating'] > 0:
            stars = "⭐" * int(book['personal_rating'])
            info_text += f"{ICONS['rating']} {stars} ({book['personal_rating']}/5) | "
        if book['reading_status']:
            status_icon = "📖" if book['reading_status'] == "أقرأ حالياً" else "✅" if book['reading_status'] == "مكتمل" else "⏳"
            info_text += f"{status_icon} {book['reading_status']}"
        
        if info_text:
            info_label = ctk.CTkLabel(
                inner_frame,
                text=info_text,
                font=FONTS['body'],
                text_color=self.colors['text_secondary'],
                anchor="w",
                wraplength=600
            )
            info_label.pack(fill="x", pady=(0, 10))
        
        # وصف الكتاب
        if book['description']:
            desc_label = ctk.CTkLabel(
                inner_frame,
                text=book['description'][:200] + ("..." if len(book['description']) > 200 else ""),
                font=FONTS['body'],
                text_color=self.colors['text_secondary'],
                anchor="w",
                wraplength=700
            )
            desc_label.pack(fill="x", pady=(0, 10))
        
        # العلامات
        if book['tags']:
            tags_label = ctk.CTkLabel(
                inner_frame,
                text=f"🏷️ {book['tags']}",
                font=FONTS['body'],
                text_color=self.colors['accent'],
                anchor="w",
                wraplength=700
            )
            tags_label.pack(fill="x", pady=(0, 10))
        
        # تاريخ الإضافة
        date_label = ctk.CTkLabel(
            inner_frame,
            text=f"📅 تاريخ الإضافة: {book['date_added'][:10]}",
            font=FONTS['body'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        date_label.pack(fill="x", pady=(0, 10))
        
        # أزرار التحكم
        buttons_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # زر التعديل
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text=f"{ICONS['edit']} تعديل",
            command=lambda: self.edit_book(book),
            font=FONTS['button'],
            fg_color=self.colors['warning'],
            hover_color=self._adjust_color(self.colors['warning'], -0.2),
            width=80,
            height=30
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        # زر التفاصيل
        details_btn = ctk.CTkButton(
            buttons_frame,
            text=f"{ICONS['info']} تفاصيل",
            command=lambda: self.show_book_details(book),
            font=FONTS['button'],
            fg_color=self.colors['info'],
            hover_color=self._adjust_color(self.colors['info'], -0.2),
            width=80,
            height=30
        )
        details_btn.pack(side="left", padx=(0, 10))
        
        # زر الحذف
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text=f"{ICONS['delete']} حذف",
            command=lambda: self.delete_book(book),
            font=FONTS['button'],
            fg_color=self.colors['error'],
            hover_color=self._adjust_color(self.colors['error'], -0.2),
            width=80,
            height=30
        )
        delete_btn.pack(side="right")
    
    def edit_book(self, book: Dict):
        """تعديل كتاب"""
        EditBookDialog(self, self.library_manager, book, self.colors)
    
    def show_book_details(self, book: Dict):
        """عرض تفاصيل الكتاب"""
        # إنشاء نافذة تفاصيل
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"تفاصيل كتاب: {book['title']}")
        details_window.geometry("600x500")
        details_window.configure(fg_color=self.colors['surface'])
        details_window.transient(self)
        
        # إطار قابل للتمرير
        scroll_frame = ctk.CTkScrollableFrame(details_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عرض التفاصيل
        details_text = f"""
{ICONS['book']} العنوان: {book['title']}
{ICONS['author']} المؤلف: {book['author']}
{ICONS['category']} الفئة: {book['category'] or 'غير محدد'}
{ICONS['rating']} التقييم الشخصي: {'⭐' * int(book['personal_rating'])} ({book['personal_rating']}/5)
📖 حالة القراءة: {book['reading_status']}
🏷️ العلامات: {book['tags'] or 'لا توجد'}
📅 تاريخ الإضافة: {book['date_added']}

{ICONS['info']} الوصف:
{book['description'] or 'لا يوجد وصف'}
"""
        
        details_label = ctk.CTkLabel(
            scroll_frame,
            text=details_text,
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w",
            justify="right"
        )
        details_label.pack(fill="x", pady=(0, 20))
        
        # زر الإغلاق
        close_btn = ctk.CTkButton(
            scroll_frame,
            text="إغلاق",
            command=details_window.destroy,
            font=FONTS['button'],
            fg_color=self.colors['error'],
            hover_color=self._adjust_color(self.colors['error'], -0.2)
        )
        close_btn.pack()
    
    def delete_book(self, book: Dict):
        """حذف كتاب"""
        result = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف الكتاب \"{book['title']}\" من مكتبتك؟\n\nهذا الإجراء لا يمكن التراجع عنه."
        )
        
        if result:
            if self.library_manager.delete_book(book['id']):
                messagebox.showinfo("نجح!", f"تم حذف الكتاب \"{book['title']}\" من مكتبتك")
                self.refresh_books()
            else:
                messagebox.showerror("خطأ", "فشل في حذف الكتاب")
    
    def show_statistics(self):
        """عرض إحصائيات المكتبة"""
        stats = self.library_manager.get_statistics()
        
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("إحصائيات المكتبة")
        stats_window.geometry("400x300")
        stats_window.configure(fg_color=self.colors['surface'])
        stats_window.transient(self)
        
        # إطار قابل للتمرير
        scroll_frame = ctk.CTkScrollableFrame(stats_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عنوان
        title_label = ctk.CTkLabel(
            scroll_frame,
            text=f"{ICONS['statistics']} إحصائيات المكتبة",
            font=("Helvetica", 16, "bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))
        
        # إجمالي الكتب
        total_label = ctk.CTkLabel(
            scroll_frame,
            text=f"📚 إجمالي الكتب: {stats['total_books']}",
            font=FONTS['body'],
            text_color=self.colors['text']
        )
        total_label.pack(pady=5)
        
        # حالة القراءة
        reading_label = ctk.CTkLabel(
            scroll_frame,
            text="📖 حالة القراءة:",
            font=FONTS['body'],
            text_color=self.colors['text']
        )
        reading_label.pack(pady=(20, 5))
        
        for status, count in stats['reading_stats'].items():
            status_label = ctk.CTkLabel(
                scroll_frame,
                text=f"  • {status}: {count} كتاب",
                font=FONTS['body'],
                text_color=self.colors['text_secondary']
            )
            status_label.pack()
        
        # متوسط التقييم
        rating_label = ctk.CTkLabel(
            scroll_frame,
            text=f"⭐ متوسط التقييم: {'⭐' * int(stats['average_rating'])} ({stats['average_rating']}/5)",
            font=FONTS['body'],
            text_color=self.colors['text']
        )
        rating_label.pack(pady=(20, 5))
        
        # زر الإغلاق
        close_btn = ctk.CTkButton(
            scroll_frame,
            text="إغلاق",
            command=stats_window.destroy,
            font=FONTS['button'],
            fg_color=self.colors['primary'],
            hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        close_btn.pack(pady=20)
    
    def _adjust_color(self, color: str, factor: float) -> str:
        """تعديل لون معين"""
        if color.startswith('#'):
            color = color[1:]
        
        r = int(color[0:2], 16)
        g = int(color[2:4], 16) 
        b = int(color[4:6], 16)
        
        r = max(0, min(255, int(r + (factor * 255))))
        g = max(0, min(255, int(g + (factor * 255))))
        b = max(0, min(255, int(b + (factor * 255))))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_close(self):
        """إغلاق النافذة"""
        self.destroy()


class EditBookDialog(ctk.CTkToplevel):
    """نافذة تعديل كتاب"""
    
    def __init__(self, parent, library_manager: LibraryManager, book: Dict, colors: Dict):
        super().__init__(parent)
        
        self.parent = parent
        self.library_manager = library_manager
        self.book = book
        self.colors = colors
        
        self.setup_window()
        self.create_widgets()
        self.load_book_data()
        
        self.transient(self.parent)
        self.grab_set()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.title("تعديل كتاب")
        self.geometry("500x600")
        self.configure(fg_color=self.colors['surface'])
        self.resizable(False, False)
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"{ICONS['edit']} تعديل كتاب",
            font=FONTS['title'],
            text_color=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))
        
        # عنوان الكتاب
        ctk.CTkLabel(main_frame, text="عنوان الكتاب *", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.title_entry = ctk.CTkEntry(main_frame, font=FONTS['body'], height=40)
        self.title_entry.pack(fill="x", pady=(0, 15))
        
        # اسم المؤلف
        ctk.CTkLabel(main_frame, text="اسم المؤلف *", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.author_entry = ctk.CTkEntry(main_frame, font=FONTS['body'], height=40)
        self.author_entry.pack(fill="x", pady=(0, 15))
        
        # فئة الكتاب
        ctk.CTkLabel(main_frame, text="فئة الكتاب", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.category_entry = ctk.CTkEntry(main_frame, font=FONTS['body'], height=40)
        self.category_entry.pack(fill="x", pady=(0, 15))
        
        # وصف الكتاب
        ctk.CTkLabel(main_frame, text="وصف الكتاب", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.description_text = ctk.CTkTextbox(main_frame, height=80, font=FONTS['body'])
        self.description_text.pack(fill="x", pady=(0, 15))
        
        # تقييم شخصي
        ctk.CTkLabel(main_frame, text="التقييم الشخصي", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.rating_var = ctk.StringVar(value="0")
        rating_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        rating_frame.pack(fill="x", pady=(0, 15))
        
        for i in range(1, 6):
            ctk.CTkRadioButton(
                rating_frame,
                text=f"{'⭐' * i} ({i})",
                variable=self.rating_var,
                value=str(i)
            ).pack(side="left", padx=(0, 10))
        
        # حالة القراءة
        ctk.CTkLabel(main_frame, text="حالة القراءة", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.reading_status_var = ctk.StringVar(value="لم أقرأ بعد")
        reading_status_menu = ctk.CTkOptionMenu(
            main_frame,
            variable=self.reading_status_var,
            values=["لم أقرأ بعد", "أقرأ حالياً", "مكتمل"]
        )
        reading_status_menu.pack(fill="x", pady=(0, 15))
        
        # العلامات
        ctk.CTkLabel(main_frame, text="العلامات", font=FONTS['body']).pack(anchor="w", pady=(10, 5))
        self.tags_entry = ctk.CTkEntry(main_frame, font=FONTS['body'], height=40)
        self.tags_entry.pack(fill="x", pady=(0, 20))
        
        # أزرار التحكم
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="إلغاء",
            command=self.destroy,
            width=100
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text=f"{ICONS['success']} حفظ التغييرات",
            command=self.on_save,
            width=140
        )
        save_btn.pack(side="right")
    
    def load_book_data(self):
        """تحميل بيانات الكتاب"""
        self.title_entry.insert(0, self.book['title'])
        self.author_entry.insert(0, self.book['author'])
        self.category_entry.insert(0, self.book['category'] or "")
        self.description_text.insert("1.0", self.book['description'] or "")
        self.rating_var.set(str(int(self.book['personal_rating'])))
        self.reading_status_var.set(self.book['reading_status'])
        self.tags_entry.insert(0, self.book['tags'] or "")
    
    def on_save(self):
        """حفظ التغييرات"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        
        if not title or not author:
            messagebox.showerror("خطأ", "عنوان الكتاب واسم المؤلف مطلوبان")
            return
        
        # تحديث البيانات
        success = self.library_manager.update_book(
            self.book['id'],
            title=title,
            author=author,
            category=self.category_entry.get().strip(),
            description=self.description_text.get("1.0", "end-1c").strip(),
            personal_rating=float(self.rating_var.get()),
            reading_status=self.reading_status_var.get(),
            tags=self.tags_entry.get().strip()
        )
        
        if success:
            messagebox.showinfo("نجح!", "تم تحديث الكتاب بنجاح")
            self.parent.refresh_books()
            self.destroy()
        else:
            messagebox.showerror("خطأ", "فشل في تحديث الكتاب")