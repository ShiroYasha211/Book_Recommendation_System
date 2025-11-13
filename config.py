COLORS = {
    'dark': {
        'primary': '#2E8B57',           
        'secondary': '#4169E1',         
        'accent': '#FF6B35',            
        'background': '#1E1E1E',        
        'surface': '#2D2D2D',           
        'text': '#FFFFFF',              
        'text_secondary': '#B0B0B0',    
        'border': '#404040',            
        'success': '#28A745',           
        'warning': '#FFC107',           
        'error': '#DC3545',             
        'info': '#17A2B8'               
    },
    
    'light': {
        'primary': '#2E8B57',           
        'secondary': '#4169E1',         
        'accent': '#FF6B35',            
        'background': '#F8F9FA',       
        'surface': '#FFFFFF',           
        'text': '#212529',              
        'text_secondary': '#6C757D',    
        'border': '#DEE2E6',            
        'success': '#28A745',           
        'warning': '#FFC107',           
        'error': '#DC3545',             
        'info': '#17A2B8'               
    }
}


FONTS = {
    'title': ('Arial', 18, 'bold'),
    'subtitle': ('Arial', 14, 'bold'),
    'body': ('Arial', 12, 'normal'),
    'small': ('Arial', 10, 'normal'),
    'button': ('Arial', 12, 'bold'),
    'entry': ('Arial', 11, 'normal')
}


APP_CONFIG = {
    'title': 'نظام توصية كتب البرمجة',
    'width': 1200,
    'height': 800,
    'min_width': 1000,
    'min_height': 600,
    'icon_path': None, 
    'theme': 'dark'     
}


FILTER_OPTIONS = {
    'categories': ['الكل'],
    'languages': ['الكل'],
    'difficulties': ['الكل', 'مبتدئ', 'متوسط', 'متقدم'],
    'rating_min': [0.0, 3.0, 3.5, 4.0, 4.5]
}

CARD_CONFIG = {
    'width': 350,
    'height': 200,
    'padding': 15,
    'border_radius': 10,
    'shadow_offset': (2, 2)
}

ICONS = {
    'search': '🔍',
    'filter': '🔧',
    'star': '⭐',
    'book': '📚',
    'author': '✍️',
    'category': '📂',
    'rating': '💯',
    'year': '📅',
    'pages': '📄',
    'language': '💬',
    'difficulty': '🎯',
    'refresh': '🔄',
    'settings': '⚙️',
    'info': 'ℹ️',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'statistics': '📊',
    'recommendations': '🎯',
    'search_results': '🔍',
    'reset': '🔄',
    'close': '❌',
    'menu': '📋'
}

MESSAGES = {
    'search_placeholder': 'ابحث عن كتاب أو مواضيع برمجية...',
    'no_results': 'لم يتم العثور على نتائج',
    'loading': 'جاري التحميل...',
    'error_loading': 'خطأ في تحميل البيانات',
    'welcome': 'مرحباً بك في نظام توصية كتب البرمجة',
    'statistics': 'إحصائيات البيانات',
    'recommendations': 'التوصيات',
    'filters': 'المرشحات',
    'details': 'تفاصيل الكتاب',
    'similar_books': 'كتب مشابهة',
    'top_rated': 'أعلى الكتب تقييماً',
    'search_results': 'نتائج البحث'
}