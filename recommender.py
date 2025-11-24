import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

class BookRecommender:
    """نظام التوصية المحسن للكتب"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.df = data_manager.df
        self.vectorizer = None
        self.feature_matrix = None
        self.similarity_matrix = None
        self._prepare_recommendation_system()
    
    def _prepare_recommendation_system(self):
        """إعداد نظام التوصية"""
        # إنشاء ميزات مجمعة مع أوزان
        self._create_weighted_features()
        
        # إنشاء متجه TF-IDF
        self._create_tfidf_matrix()
        
        # إنشاء مصفوفة التشابه
        self._create_similarity_matrix()
        
        print("تم إعداد نظام التوصية بنجاح")
    
    def _create_weighted_features(self):
        """إنشاء ميزات موزونة"""
        # إزالة القيم الفارغة
        self.df['title'] = self.df['title'].fillna('')
        self.df['author'] = self.df['author'].fillna('')
        self.df['category'] = self.df['category'].fillna('')
        self.df['description'] = self.df['description'].fillna('')
        self.df['tags'] = self.df['tags'].fillna('')
        
        # إنشاء ميزات موزونة
        self.df['weighted_features'] = (
            self.df['title'] * 3 + ' ' +  # وزن أعلى للعنوان
            self.df['category'] * 2 + ' ' +  # وزن متوسط للفئة
            self.df['tags'] * 2 + ' ' +  # وزن متوسط للعلامات
            self.df['author'] + ' ' +  # وزن عادي للمؤلف
            self.df['description']  # وزن عادي للوصف
        ).str.replace('nan', '')
    
    def _create_tfidf_matrix(self):
        """إنشاء مصفوفة TF-IDF"""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)  # استخدام 1-2 كلمة
        )
        self.feature_matrix = self.vectorizer.fit_transform(self.df['weighted_features'])
    
    def _create_similarity_matrix(self):
        """إنشاء مصفوفة التشابه"""
        self.similarity_matrix = cosine_similarity(self.feature_matrix)
    
    def find_book_by_title(self, title_query: str) -> List[int]:
        """البحث عن الكتب المشابهة للعنوان"""
        if not title_query.strip():
            return []
        
        # البحث الدقيق أولاً
        exact_matches = self.df[self.df['title'].str.lower().str.contains(
            title_query.lower(), case=False, na=False
        )].index.tolist()
        
        if exact_matches:
            return exact_matches
        
        # البحث الغامض إذا لم توجد نتائج دقيقة
        fuzzy_matches = []
        for idx, row in self.df.iterrows():
            similarity = fuzz.ratio(title_query.lower(), row['title'].lower())
            if similarity > 70:  # حد التشابه
                fuzzy_matches.append((idx, similarity))
        
        # ترتيب النتائج حسب التشابه
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        return [idx for idx, _ in fuzzy_matches[:5]]
    
    def recommend_books(self, 
                       query: str, 
                       category: str = None, 
                       language: str = None,
                       difficulty: str = None,
                       min_rating: float = 0.0,
                       max_results: int = 10) -> List[Dict]:
        """توصية الكتب مع المرشحات"""
        
        if not query.strip():
            # إذا لم يكن هناك استعلام، اعرض أفضل الكتب
            return self._get_top_recommended_books(max_results, min_rating)
        
        # البحث عن الكتب المناسبة
        book_indices = self.find_book_by_title(query)
        
        if not book_indices:
            # إذا لم توجد كتب مشابهة، ابحث عامة
            search_results = self.data_manager.search_books(query)
            if not search_results.empty:
                # اعرض نتائج البحث مرتبة حسب التقييم
                top_books = search_results.nlargest(max_results, 'rating')
                return self._format_book_results(top_books)
            else:
                # لم يتم العثور على شيء
                return self._get_top_recommended_books(max_results, min_rating)
        
        recommendations = []
        
        for book_idx in book_indices:
            # الحصول على التشابهات مع هذا الكتاب
            similarity_scores = list(enumerate(self.similarity_matrix[book_idx]))
            
            # ترتيب حسب التشابه
            sorted_books = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            
            for book_index, similarity_score in sorted_books[1:20]:  # فحص 20 كتاب
                book_info = self.df.iloc[book_index]
                
                # تطبيق المرشحات
                if self._passes_filters(book_info, category, language, difficulty, min_rating):
                    recommendations.append({
                        'book': book_info,
                        'similarity_score': similarity_score,
                        'query': query
                    })
        
        # إزالة التكرارات وترتيب النتائج
        unique_recommendations = self._remove_duplicates(recommendations)
        
        # ترتيب نهائي (تشابه + تقييم)
        final_recommendations = sorted(
            unique_recommendations, 
            key=lambda x: (x['similarity_score'] * 0.7 + x['book']['rating'] / 5.0 * 0.3), 
            reverse=True
        )
        
        return self._format_book_results(
            pd.DataFrame([rec['book'] for rec in final_recommendations[:max_results]])
        )
    
    def _passes_filters(self, book_info, category, language, difficulty, min_rating):
        """فحص ما إذا كان الكتاب يمرر المرشحات"""
        if category and category != 'الكل' and category not in str(book_info['category']):
            return False
        
        if language and language != 'الكل' and language not in str(book_info['language']):
            return False
        
        if difficulty and difficulty != 'الكل' and book_info['difficulty'] != difficulty:
            return False
        
        if book_info['rating'] < min_rating:
            return False
        
        return True
    
    def _remove_duplicates(self, recommendations):
        """إزالة التكرارات"""
        seen_titles = set()
        unique_recommendations = []
        
        for rec in recommendations:
            title = rec['book']['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _get_top_recommended_books(self, max_results, min_rating):
        """الحصول على أفضل الكتب عندما لا يوجد استعلام"""
        top_books = self.df[self.df['rating'] >= min_rating].nlargest(max_results, 'rating')
        return self._format_book_results(top_books)
    
    def _format_book_results(self, books_df):
        """تنسيق نتائج الكتب"""
        results = []
        
        for idx, row in books_df.iterrows():
            result = {
                'id': row['book_id'],
                'title': row['title'],
                'author': row['author'],
                'category': row['category'],
                'language': row['language'],
                'rating': row['rating'],
                'year': row['year'],
                'pages': row['pages'],
                'description': row['description'][:200] + '...' if len(str(row['description'])) > 200 else row['description'],
                'tags': row['tags'],
                'difficulty': row['difficulty'],
                'rating_category': row['rating_category']
            }
            results.append(result)
        
        return results
    
    def get_similar_books(self, book_id: int, max_results: int = 5) -> List[Dict]:
        """الحصول على كتب مشابهة لكتاب معين"""
        try:
            book_idx = self.df[self.df['book_id'] == book_id].index[0]
            similarity_scores = list(enumerate(self.similarity_matrix[book_idx]))
            sorted_books = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            
            similar_books = []
            for i, (book_index, score) in enumerate(sorted_books[1:max_results+1]):
                book_info = self.df.iloc[book_index]
                similar_books.append({
                    'book': book_info,
                    'similarity_score': score
                })
            
            return self._format_book_results(
                pd.DataFrame([rec['book'] for rec in similar_books])
            )
        except IndexError:
            return []