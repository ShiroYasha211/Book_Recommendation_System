import pandas as pd
from typing import List, Dict

class DataManager:
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.csv_path)
            self._clean_data()
            print(f"تم تحميل {len(self.df)} كتاب بنجاح")
        except Exception as e:
            print(f"خطأ في تحميل البيانات: {e}")
    
    def _clean_data(self):
        # ملء القيم الفارغة
        self.df['description'] = self.df['description'].fillna('لا يوجد وصف')
        self.df['tags'] = self.df['tags'].fillna('')
        self.df['author'] = self.df['author'].fillna('مؤلف غير معروف')
        
        # إضافة عمود الصعوبة
        self._add_difficulty_level()
        
        # إضافة عمود مستوى التقييم
        self._add_rating_category()
    
    def _add_difficulty_level(self):
        def get_difficulty(row):
            pages = row['pages']
            tags = str(row['tags']).lower()
            
            # قواعد بسيطة لتحديد الصعوبة
            if pages < 300:
                if any(word in tags for word in ['beginner', 'introduction', 'basics', 'مبتدئ']):
                    return 'مبتدئ'
                else:
                    return 'متوسط'
            elif pages < 600:
                if any(word in tags for word in ['advanced', 'deep', 'comprehensive', 'متقدم']):
                    return 'متقدم'
                else:
                    return 'متوسط'
            else:
                return 'متقدم'
        
        self.df['difficulty'] = self.df.apply(get_difficulty, axis=1)
    
    def _add_rating_category(self):
        def get_rating_category(rating):
            if rating >= 4.7:
                return 'ممتاز'
            elif rating >= 4.3:
                return 'جيد جداً'
            elif rating >= 4.0:
                return 'جيد'
            elif rating >= 3.5:
                return 'متوسط'
            else:
                return 'ضعيف'
        
        self.df['rating_category'] = self.df['rating'].apply(get_rating_category)
    
    def get_books_by_category(self, category: str) -> pd.DataFrame:
        return self.df[self.df['category'].str.contains(category, case=False, na=False)]
    
    def get_books_by_language(self, language: str) -> pd.DataFrame:
        return self.df[self.df['language'].str.contains(language, case=False, na=False)]
    
    def get_top_rated_books(self, limit: int = 10) -> pd.DataFrame:
        return self.df.nlargest(limit, 'rating')
    
    def get_statistics(self) -> Dict:
        stats = {
            'total_books': len(self.df),
            'categories': self.df['category'].nunique(),
            'languages': self.df['language'].nunique(),
            'avg_rating': self.df['rating'].mean(),
            'top_categories': self.df['category'].value_counts().head(5).to_dict(),
            'top_languages': self.df['language'].value_counts().head(3).to_dict(),
            'difficulty_distribution': self.df['difficulty'].value_counts().to_dict(),
            'year_range': f"{self.df['year'].min()} - {self.df['year'].max()}"
        }
        return stats
    
    def search_books(self, query: str) -> pd.DataFrame:
        if not query:
            return pd.DataFrame()
        
        # البحث في العنوان، المؤلف، الفئة، الوصف، والعلامات
        mask = (
            self.df['title'].str.contains(query, case=False, na=False) |
            self.df['author'].str.contains(query, case=False, na=False) |
            self.df['category'].str.contains(query, case=False, na=False) |
            self.df['description'].str.contains(query, case=False, na=False) |
            self.df['tags'].str.contains(query, case=False, na=False)
        )
        
        return self.df[mask]
    
    def get_all_categories(self) -> List[str]:
        return sorted(self.df['category'].unique().tolist())
    
    def get_all_languages(self) -> List[str]:
        return sorted(self.df['language'].unique().tolist())