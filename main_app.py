import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager
from recommender import BookRecommender
from book_card import BookCard, BookDetailsDialog
from library_manager import LibraryManager
from add_book_dialog import AddBookDialog
from my_library_window import MyLibraryWindow
from config import CARD_CONFIG, COLORS, FONTS, ICONS, APP_CONFIG, FILTER_OPTIONS, MESSAGES
from typing import List, Dict
import threading

class MainApplication(ctk.CTk):    
    def __init__(self):
        super().__init__()
        
        # إعداد المتغيرات أولاً
        self.current_theme = APP_CONFIG['theme']
        self.colors = COLORS[self.current_theme]
        
        # إعداد النافذة الرئيسية
        self.setup_main_window()
        
        # إعداد البيانات
        self.data_manager = None
        self.recommender = None
        self.current_recommendations = []
        
        # إعداد المكتبة الشخصية
        self.library_manager = LibraryManager()
        
        # إعداد الواجهة
        self.create_widgets()
        self.load_data()
    
    def setup_main_window(self):
        """إعداد النافذة الرئيسية"""
        self.title(APP_CONFIG['title'])
        self.geometry(f"{APP_CONFIG['width']}x{APP_CONFIG['height']}")
        self.minsize(APP_CONFIG['min_width'], APP_CONFIG['min_height'])
        
        # إعداد اللون الافتراضي
        self.configure(fg_color=self.colors['background'])
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # التخطيط الرئيسي
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # إنشاء النوافذ الفرعية
        self.create_search_frame()
        self.create_results_frame()
        self.create_sidebar()
        self.create_status_bar()
    
    def create_search_frame(self):
        """إنشاء إطار البحث والمرشحات"""
        search_frame = ctk.CTkFrame(self, fg_color=self.colors['surface'])
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(4, weight=1)  # عمود جديد للأزرار
        
        # العنوان
        title_label = ctk.CTkLabel(
            search_frame,
            text=f"{ICONS['book']} {MESSAGES['welcome']}",
            font=FONTS['title'],
            text_color=self.colors['primary']
        )
        title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")
        
        # شريط البحث
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_text_change)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text=MESSAGES['search_placeholder'],
            font=FONTS['entry'],
            width=400
        )
        self.search_entry.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # زر البحث
        self.search_btn = ctk.CTkButton(
            search_frame,
            text=f"{ICONS['search']} بحث",
            command=self.perform_search,
            font=FONTS['button'],
            fg_color=self.colors['primary'],
            hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.search_btn.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # زر الإحصائيات
        stats_btn = ctk.CTkButton(
            search_frame,
            text=f"{ICONS['statistics']} إحصائيات",
            command=self.show_statistics,
            font=FONTS['button'],
            fg_color=self.colors['secondary'],
            hover_color=self._adjust_color(self.colors['secondary'], -0.2)
        )
        stats_btn.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # زر إضافة كتاب للمكتبة الشخصية
        add_book_btn = ctk.CTkButton(
            search_frame,
            text=f"{ICONS['add']} إضافة كتاب لمكتبي",
            command=self.show_add_book_dialog,
            font=FONTS['button'],
            fg_color=self.colors['success'],
            hover_color=self._adjust_color(self.colors['success'], -0.2)
        )
        add_book_btn.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # زر عرض المكتبة الشخصية
        show_library_btn = ctk.CTkButton(
            search_frame,
            text=f"{ICONS['book']} عرض مكتبي",
            command=self.show_my_library,
            font=FONTS['button'],
            fg_color=self.colors['accent'],
            hover_color=self._adjust_color(self.colors['accent'], -0.2)
        )
        show_library_btn.grid(row=1, column=4, padx=10, pady=10, sticky="w")
        
        # قسم المرشحات
        filters_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        filters_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=(10, 20))
        filters_frame.grid_columnconfigure(0, weight=1)
        filters_frame.grid_columnconfigure(1, weight=1)
        filters_frame.grid_columnconfigure(2, weight=1)
        filters_frame.grid_columnconfigure(3, weight=1)
        
        # مرشح الفئة
        self.category_var = tk.StringVar(value="الكل")
        self.category_combo = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.category_var,
            values=["الكل"],
            font=FONTS['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.category_combo.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # مرشح اللغة البرمجية
        self.language_var = tk.StringVar(value="الكل")
        self.language_combo = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.language_var,
            values=["الكل"],
            font=FONTS['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.language_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # مرشح مستوى الصعوبة
        self.difficulty_var = tk.StringVar(value="الكل")
        self.difficulty_combo = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.difficulty_var,
            values=FILTER_OPTIONS['difficulties'],
            font=FONTS['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.difficulty_combo.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # مرشح الحد الأدنى للتقييم
        self.min_rating_var = tk.StringVar(value="0.0")
        self.rating_combo = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.min_rating_var,
            values=[str(r) for r in FILTER_OPTIONS['rating_min']],
            font=FONTS['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self._adjust_color(self.colors['primary'], -0.2)
        )
        self.rating_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # ربط تغييرات المرشحات
        self.category_var.trace('w', self.on_filter_change)
        self.language_var.trace('w', self.on_filter_change)
        self.difficulty_var.trace('w', self.on_filter_change)
        self.min_rating_var.trace('w', self.on_filter_change)
    
    def create_results_frame(self):
        """إنشاء إطار النتائج"""
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color=self.colors['surface'])
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=self.colors['surface'])
        self.sidebar_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # عنوان الشريط الجانبي
        sidebar_title = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"{ICONS['info']} لوحة التحكم",
            font=FONTS['subtitle'],
            text_color=self.colors['primary']
        )
        sidebar_title.pack(pady=15)
        
        # معلومات سريعة
        self.quick_info_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=self.colors['background'])
        self.quick_info_frame.pack(fill="x", padx=15, pady=10)
        
        self.total_books_label = ctk.CTkLabel(
            self.quick_info_frame,
            text="",
            font=FONTS['body'],
            text_color=self.colors['text'],
            anchor="w"
        )
        self.total_books_label.pack(fill="x", padx=10, pady=5)
        
        self.top_categories_label = ctk.CTkLabel(
            self.quick_info_frame,
            text="",
            font=FONTS['small'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        self.top_categories_label.pack(fill="x", padx=10, pady=5)
        
        # أزرار سريعة
        quick_actions_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=self.colors['background'])
        quick_actions_frame.pack(fill="x", padx=15, pady=10)
        
        top_rated_btn = ctk.CTkButton(
            quick_actions_frame,
            text=f"{ICONS['star']} أعلى الكتب تقييماً",
            command=self.show_top_rated,
            font=FONTS['small'],
            fg_color=self.colors['warning'],
            hover_color=self._adjust_color(self.colors['warning'], -0.2)
        )
        top_rated_btn.pack(fill="x", padx=10, pady=5)
        
        recent_btn = ctk.CTkButton(
            quick_actions_frame,
            text=f"{ICONS['year']} الكتب الحديثة",
            command=self.show_recent_books,
            font=FONTS['small'],
            fg_color=self.colors['info'],
            hover_color=self._adjust_color(self.colors['info'], -0.2)
        )
        recent_btn.pack(fill="x", padx=10, pady=5)
        
        beginner_btn = ctk.CTkButton(
            quick_actions_frame,
            text=f"{ICONS['difficulty']} كتب المبتدئين",
            command=self.show_beginner_books,
            font=FONTS['small'],
            fg_color=self.colors['success'],
            hover_color=self._adjust_color(self.colors['success'], -0.2)
        )
        beginner_btn.pack(fill="x", padx=10, pady=5)
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_frame = ctk.CTkFrame(self, fg_color=self.colors['surface'])
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=FONTS['small'],
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(side="left", padx=20, pady=10)
        
        # مؤشر التحميل
        self.loading_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=FONTS['small'],
            text_color=self.colors['accent']
        )
        self.loading_label.pack(side="right", padx=20, pady=10)
    
    def load_data(self):
        """تحميل البيانات"""
        def load_thread():
            try:
                self.data_manager = DataManager('programming_books_dataset.csv')
                self.recommender = BookRecommender(self.data_manager)
                
                # تحديث المرشحات
                self.update_filters()
                
                # عرض الكتب الأعلى تقييماً
                self.show_top_rated()
                
                # تحديث المعلومات السريعة
                self.update_quick_info()
                
            except Exception as e:
                self.show_error(f"خطأ في تحميل البيانات: {str(e)}")
        
        # تشغيل التحميل في خيط منفصل
        threading.Thread(target=load_thread, daemon=True).start()
    
    def update_filters(self):
        """تحديث قيم المرشحات"""
        if self.data_manager:
            # تحديث قائمة الفئات
            categories = ["الكل"] + self.data_manager.get_all_categories()
            self.category_combo.configure(values=categories)
            
            # تحديث قائمة اللغات
            languages = ["الكل"] + self.data_manager.get_all_languages()
            self.language_combo.configure(values=languages)
    
    def update_quick_info(self):
        """تحديث المعلومات السريعة"""
        if self.data_manager:
            stats = self.data_manager.get_statistics()
            
            self.total_books_label.configure(
                text=f"{ICONS['book']} إجمالي الكتب: {stats['total_books']}"
            )
            
            top_cats = list(stats['top_categories'].keys())[:3]
            if top_cats:
                cats_text = f"{ICONS['category']} الفئات الرئيسية:\n" + "\n".join([f"• {cat}" for cat in top_cats])
                self.top_categories_label.configure(text=cats_text)
    
    def show_loading(self, show: bool = True):
        """إظهار/إخفاء مؤشر التحميل"""
        if show:
            self.loading_label.configure(text=f"{ICONS['refresh']} جاري التحميل...")
        else:
            self.loading_label.configure(text="")
        self.update()
    
    def update_status(self, message: str):
        """تحديث رسالة الحالة"""
        self.status_label.configure(text=message)
    
    def show_error(self, message: str):
        """عرض رسالة خطأ"""
        try:
            # محاولة عرض رسالة خطأ رسومية
            messagebox.showerror("خطأ", message)
        except:
            # في حالة عدم وجود بيئة رسومية، عرض الخطأ في Terminal
            print(f"❌ خطأ: {message}")
    
    def show_info(self, message: str):
        """عرض رسالة معلومات"""
        try:
            # محاولة عرض رسالة معلومات رسومية
            messagebox.showinfo("معلومات", message)
        except:
            # في حالة عدم وجود بيئة رسومية، عرض الرسالة في Terminal
            print(f"ℹ️  {message}")
    
    def on_search_text_change(self, *args):
        """حدث تغيير النص في البحث"""
        # بحث تلقائي عند كتابة 3 أحرف أو أكثر
        search_text = self.search_var.get()
        if len(search_text) >= 3:
            self.perform_search()
    
    def on_filter_change(self, *args):
        """حدث تغيير المرشحات"""
        # تحديث النتائج عند تغيير المرشحات
        search_text = self.search_var.get()
        if search_text.strip():
            self.perform_search()
    
    def perform_search(self):
        """تنفيذ البحث"""
        def search_thread():
            try:
                self.show_loading(True)
                
                search_text = self.search_var.get()
                category = self.category_var.get()
                language = self.language_var.get()
                difficulty = self.difficulty_var.get()
                min_rating = float(self.min_rating_var.get())
                
                # تنفيذ البحث
                results = self.recommender.recommend_books(
                    query=search_text,
                    category=category if category != "الكل" else None,
                    language=language if language != "الكل" else None,
                    difficulty=difficulty if difficulty != "الكل" else None,
                    min_rating=min_rating,
                    max_results=12
                )
                
                self.current_recommendations = results
                
                # تحديث الواجهة في الخيط الرئيسي
                self.after(0, lambda: self.display_results(results, search_text))
                
            except Exception as e:
                self.after(0, lambda: self.show_error(f"خطأ في البحث: {str(e)}"))
            finally:
                self.after(0, lambda: self.show_loading(False))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def display_results(self, results: List[Dict], search_text: str):
        """عرض النتائج"""
        # مسح النتائج السابقة
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not results:
            # إنشاء رسالة عدم وجود نتائج
            no_results_label = ctk.CTkLabel(
                self.results_frame,
                text=MESSAGES['no_results'],
                font=FONTS['subtitle'],
                text_color=self.colors['text_secondary']
            )
            no_results_label.pack(expand=True)
            return
        
        # عرض النتائج
        if search_text.strip():
            title = f"{ICONS['search_results']} نتائج البحث عن: '{search_text}' ({len(results)} نتيجة)"
        else:
            title = f"{ICONS['recommendations']} التوصيات ({len(results)} كتاب)"
        
        results_title = ctk.CTkLabel(
            self.results_frame,
            text=title,
            font=FONTS['subtitle'],
            text_color=self.colors['primary']
        )
        results_title.pack(pady=10)
        
        # عرض البطاقات
        for i, book in enumerate(results):
            card = BookCard(
                self.results_frame,
                book,
                on_click=self.show_book_details,
                width=CARD_CONFIG['width'],
                height=CARD_CONFIG['height']
            )
            card.pack(fill="x", padx=10, pady=5)
    
    def show_book_details(self, book_data: Dict):
        """عرض تفاصيل الكتاب"""
        dialog = BookDetailsDialog(self, book_data)
        dialog.wait_window()
    
    def show_top_rated(self):
        """عرض الكتب الأعلى تقييماً"""
        def get_top_rated():
            try:
                self.show_loading(True)
                top_books = self.data_manager.get_top_rated_books(limit=12)
                results = []
                for _, book in top_books.iterrows():
                    results.append({
                        'id': book['book_id'],
                        'title': book['title'],
                        'author': book['author'],
                        'category': book['category'],
                        'language': book['language'],
                        'rating': book['rating'],
                        'year': book['year'],
                        'pages': book['pages'],
                        'description': book['description'],
                        'tags': book['tags'],
                        'difficulty': book['difficulty'],
                        'rating_category': book['rating_category']
                    })
                
                self.after(0, lambda: self.display_results(results, ""))
                
            except Exception as e:
                self.after(0, lambda: self.show_error(f"خطأ في جلب الكتب الأعلى تقييماً: {str(e)}"))
            finally:
                self.after(0, lambda: self.show_loading(False))
        
        threading.Thread(target=get_top_rated, daemon=True).start()
    
    def show_recent_books(self):
        """عرض الكتب الحديثة"""
        if not self.data_manager:
            return
        
        try:
            recent_books = self.data_manager.df.nlargest(12, 'year')
            results = []
            for _, book in recent_books.iterrows():
                results.append({
                    'id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'language': book['language'],
                    'rating': book['rating'],
                    'year': book['year'],
                    'pages': book['pages'],
                    'description': book['description'],
                    'tags': book['tags'],
                    'difficulty': book['difficulty'],
                    'rating_category': book['rating_category']
                })
            
            self.display_results(results, "")
            
        except Exception as e:
            self.show_error(f"خطأ في جلب الكتب الحديثة: {str(e)}")
    
    def show_beginner_books(self):
        """عرض كتب المبتدئين"""
        if not self.data_manager:
            return
        
        try:
            beginner_books = self.data_manager.df[self.data_manager.df['difficulty'] == 'مبتدئ'].head(12)
            results = []
            for _, book in beginner_books.iterrows():
                results.append({
                    'id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'language': book['language'],
                    'rating': book['rating'],
                    'year': book['year'],
                    'pages': book['pages'],
                    'description': book['description'],
                    'tags': book['tags'],
                    'difficulty': book['difficulty'],
                    'rating_category': book['rating_category']
                })
            
            self.display_results(results, "")
            
        except Exception as e:
            self.show_error(f"خطأ في جلب كتب المبتدئين: {str(e)}")
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        if not self.data_manager:
            self.show_info("لا يمكن عرض الإحصائيات: لم يتم تحميل البيانات بعد")
            return
        
        try:
            stats = self.data_manager.get_statistics()
            
            # التحقق من البيئة الرسومية
            try:
                # إنشاء نافذة الإحصائيات
                stats_window = ctk.CTkToplevel(self)
                stats_window.title(MESSAGES['statistics'])
                stats_window.geometry("800x600")
                stats_window.configure(fg_color=self.colors['background'])
                
                # إطار التمرير
                stats_frame = ctk.CTkScrollableFrame(
                    stats_window,
                    width=780,
                    height=580,
                    fg_color=self.colors['surface']
                )
                stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # عرض الإحصائيات
                stats_text = f"""
{ICONS['statistics']} إحصائيات قاعدة البيانات
                
{ICONS['book']} إجمالي الكتب: {stats['total_books']}
{ICONS['category']} عدد الفئات: {stats['categories']}
{ICONS['language']} عدد اللغات البرمجية: {stats['languages']}
{ICONS['star']} متوسط التقييم: {stats['avg_rating']:.2f}
{ICONS['year']} نطاق السنوات: {stats['year_range']}

{ICONS['category']} الفئات الرئيسية:
"""
                
                for category, count in stats['top_categories'].items():
                    stats_text += f"• {category}: {count} كتاب\n"
                
                stats_text += f"\n{ICONS['language']} اللغات الرئيسية:\n"
                for language, count in stats['top_languages'].items():
                    stats_text += f"• {language}: {count} كتاب\n"
                
                stats_text += f"\n{ICONS['difficulty']} توزيع مستوى الصعوبة:\n"
                for difficulty, count in stats['difficulty_distribution'].items():
                    stats_text += f"• {difficulty}: {count} كتاب\n"
                
                stats_label = ctk.CTkLabel(
                    stats_frame,
                    text=stats_text,
                    font=FONTS['body'],
                    text_color=self.colors['text'],
                    justify="right"
                )
                stats_label.pack(padx=20, pady=20)
                
            except Exception as ui_error:
                # في حالة عدم وجود بيئة رسومية، عرض الإحصائيات في Terminal
                print(f"\n{ICONS['statistics']} إحصائيات قاعدة البيانات")
                print("=" * 60)
                print(f"{ICONS['book']} إجمالي الكتب: {stats['total_books']}")
                print(f"{ICONS['category']} عدد الفئات: {stats['categories']}")
                print(f"{ICONS['language']} عدد اللغات البرمجية: {stats['languages']}")
                print(f"{ICONS['star']} متوسط التقييم: {stats['avg_rating']:.2f}")
                print(f"{ICONS['year']} نطاق السنوات: {stats['year_range']}")
                print(f"\n{ICONS['category']} الفئات الرئيسية:")
                for category, count in stats['top_categories'].items():
                    print(f"  • {category}: {count} كتاب")
                print(f"\n{ICONS['language']} اللغات الرئيسية:")
                for language, count in stats['top_languages'].items():
                    print(f"  • {language}: {count} كتاب")
                print(f"\n{ICONS['difficulty']} توزيع مستوى الصعوبة:")
                for difficulty, count in stats['difficulty_distribution'].items():
                    print(f"  • {difficulty}: {count} كتاب")
                print("=" * 60)
                
        except Exception as e:
            # تحسين معالجة الأخطاء
            error_msg = f"خطأ في عرض الإحصائيات: {str(e)}"
            print(f"❌ {error_msg}")
            try:
                self.show_error(error_msg)
            except:
                # في حالة فشل show_error أيضاً
                pass
    
    def _adjust_color(self, color: str, factor: float) -> str:
        """تعديل لون بسيط - في التطبيق الحقيقي سنستخدم مكتبة ألوان متقدمة"""
        # تبسيط: إرجاع نفس اللون مع تغيير بسيط
        return color
    
    # ========================================
    # وظائف المكتبة الشخصية
    # ========================================
    
    def show_add_book_dialog(self):
        """عرض نافذة إضافة كتاب جديد"""
        try:
            dialog = AddBookDialog(self, self.library_manager, self.colors)
            # التركيز على النافذة المنبثقة
            dialog.focus_set()
            dialog.grab_set()
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة إضافة الكتاب: {str(e)}"
            print(f"❌ {error_msg}")
            self.show_error(error_msg)
    
    def show_my_library(self):
        """عرض نافذة المكتبة الشخصية"""
        try:
            # إنشاء نافذة المكتبة الشخصية
            library_window = MyLibraryWindow(self, self.library_manager, self.colors)
            
            # التركيز على النافذة الجديدة
            library_window.focus_set()
            
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة المكتبة الشخصية: {str(e)}"
            print(f"❌ {error_msg}")
            self.show_error(error_msg)
    
    def cleanup(self):
        """تنظيف الموارد قبل إغلاق التطبيق"""
        try:
            # إغلاق اتصال قاعدة بيانات المكتبة الشخصية
            if hasattr(self, 'library_manager'):
                self.library_manager.close()
        except Exception as e:
            print(f"خطأ في تنظيف الموارد: {e}")
        finally:
            try:
                self.destroy()
            except:
                pass