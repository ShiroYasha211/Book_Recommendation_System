
import sys
import os
import argparse
from typing import  Dict

# إضافة المسار الحالي للـ Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager
from recommender import BookRecommender
from config import MESSAGES

class BookRecommenderCLI:
    """إصدار سطر الأوامر لتطبيق توصية الكتب"""
    
    def __init__(self, csv_path: str):
        print("🔄 جاري تحميل البيانات...")
        try:
            self.data_manager = DataManager(csv_path)
            self.recommender = BookRecommender(self.data_manager)
            print(f"✅ تم تحميل {len(self.data_manager.df)} كتاب بنجاح!")
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            sys.exit(1)
    
    def search_books(self, query: str, category: str = None, language: str = None, 
                    difficulty: str = None, min_rating: float = 0.0, max_results: int = 10):
        """البحث في الكتب"""
        print(f"\n🔍 البحث عن: '{query}'")
        if category:
            print(f"📂 الفئة: {category}")
        if language:
            print(f"💬 اللغة: {language}")
        if difficulty:
            print(f"🎯 الصعوبة: {difficulty}")
        print(f"⭐ الحد الأدنى للتقييم: {min_rating}")
        print(f"📚 عدد النتائج: {max_results}")
        print("-" * 80)
        
        try:
            results = self.recommender.recommend_books(
                query=query,
                category=category if category != "الكل" else None,
                language=language if language != "الكل" else None,
                difficulty=difficulty if difficulty != "الكل" else None,
                min_rating=min_rating,
                max_results=max_results
            )
            
            if not results:
                print("❌ لم يتم العثور على نتائج!")
                return
            
            print(f"\n📋 نتائج البحث ({len(results)} كتاب):\n")
            
            for i, book in enumerate(results, 1):
                self.print_book_card(book, i)
            
        except Exception as e:
            print(f"❌ خطأ في البحث: {e}")
    
    def show_top_rated(self, limit: int = 10):
        """عرض الكتب الأعلى تقييماً"""
        print(f"\n⭐ أعلى {limit} كتب تقييماً:")
        print("-" * 80)
        
        try:
            top_books = self.data_manager.get_top_rated_books(limit)
            
            for i, (_, book) in enumerate(top_books.iterrows(), 1):
                book_data = {
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
                }
                self.print_book_card(book_data, i)
                
        except Exception as e:
            print(f"❌ خطأ في جلب الكتب الأعلى تقييماً: {e}")
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        print(f"\n📊 {MESSAGES['statistics']}")
        print("=" * 80)
        
        try:
            stats = self.data_manager.get_statistics()
            
            print(f"📚 إجمالي الكتب: {stats['total_books']}")
            print(f"📂 عدد الفئات: {stats['categories']}")
            print(f"💬 عدد اللغات البرمجية: {stats['languages']}")
            print(f"⭐ متوسط التقييم: {stats['avg_rating']:.2f}")
            print(f"📅 نطاق السنوات: {stats['year_range']}")
            
            print(f"\n📂 الفئات الرئيسية:")
            for category, count in stats['top_categories'].items():
                print(f"  • {category}: {count} كتاب")
            
            print(f"\n💬 اللغات البرمجية الرئيسية:")
            for language, count in stats['top_languages'].items():
                print(f"  • {language}: {count} كتاب")
            
            print(f"\n🎯 توزيع مستوى الصعوبة:")
            for difficulty, count in stats['difficulty_distribution'].items():
                print(f"  • {difficulty}: {count} كتاب")
            
        except Exception as e:
            print(f"❌ خطأ في عرض الإحصائيات: {e}")
    
    def show_categories(self):
        """عرض الفئات المتاحة"""
        print(f"\n📂 الفئات المتاحة:")
        print("-" * 50)
        
        try:
            categories = self.data_manager.get_all_categories()
            for category in categories:
                count = len(self.data_manager.df[self.data_manager.df['category'] == category])
                print(f"  • {category}: {count} كتاب")
        except Exception as e:
            print(f"❌ خطأ في عرض الفئات: {e}")
    
    def show_languages(self):
        """عرض اللغات البرمجية المتاحة"""
        print(f"\n💬 اللغات البرمجية المتاحة:")
        print("-" * 50)
        
        try:
            languages = self.data_manager.get_all_languages()
            for language in languages:
                count = len(self.data_manager.df[self.data_manager.df['language'] == language])
                print(f"  • {language}: {count} كتاب")
        except Exception as e:
            print(f"❌ خطأ في عرض اللغات: {e}")
    
    def print_book_card(self, book: Dict, index: int):
        """طباعة بطاقة كتاب"""
        stars = "⭐" * int(book['rating'])
        
        print(f"\n{index}. 📖 {book['title']}")
        print(f"   ✍️  المؤلف: {book['author']}")
        print(f"   📂 الفئة: {book['category']}")
        print(f"   💬 اللغة: {book['language']}")
        print(f"   ⭐ التقييم: {stars} ({book['rating']:.1f}) - {book['rating_category']}")
        print(f"   📅 السنة: {book['year']}")
        print(f"   📄 الصفحات: {book['pages']}")
        print(f"   🎯 الصعوبة: {book['difficulty']}")
        
        # عرض الوصف إذا وجد
        if book['description'] and book['description'] != 'لا يوجد وصف':
            desc = book['description'][:150] + "..." if len(book['description']) > 150 else book['description']
            print(f"   📝 الوصف: {desc}")
        
        # عرض العلامات إذا وجدت
        if book['tags']:
            print(f"   🏷️  العلامات: {book['tags']}")
        
        print("   " + "-" * 70)

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="تطبيق توصية كتب البرمجة - إصدار سطر الأوامر",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python cli.py --search "python" --category "Python" --max-results 5
  python cli.py --top-rated 10
  python cli.py --statistics
  python cli.py --categories
  python cli.py --languages --difficulty "مبتدئ" --min-rating 4.0
        """)
    
    parser.add_argument('--csv', default='programming_books_dataset.csv',
                       help='مسار ملف البيانات')
    
    parser.add_argument('--search', type=str, help='نص البحث')
    parser.add_argument('--category', type=str, help='فلتر الفئة')
    parser.add_argument('--language', type=str, help='فلتر اللغة البرمجية')
    parser.add_argument('--difficulty', type=str, help='فلتر مستوى الصعوبة')
    parser.add_argument('--min-rating', type=float, default=0.0, help='الحد الأدنى للتقييم')
    parser.add_argument('--max-results', type=int, default=10, help='الحد الأقصى للنتائج')
    
    parser.add_argument('--top-rated', type=int, help='عرض أعلى الكتب تقييماً')
    parser.add_argument('--statistics', action='store_true', help='عرض الإحصائيات')
    parser.add_argument('--categories', action='store_true', help='عرض الفئات المتاحة')
    parser.add_argument('--languages', action='store_true', help='عرض اللغات البرمجية المتاحة')
    
    args = parser.parse_args()
    
    # إنشاء كائن CLI
    cli = BookRecommenderCLI(args.csv)
    
    # تنفيذ الأمر المطلوب
    if args.statistics:
        cli.show_statistics()
    elif args.categories:
        cli.show_categories()
    elif args.languages:
        cli.show_languages()
    elif args.top_rated:
        cli.show_top_rated(args.top_rated)
    elif args.search:
        cli.search_books(
            query=args.search,
            category=args.category,
            language=args.language,
            difficulty=args.difficulty,
            min_rating=args.min_rating,
            max_results=args.max_results
        )
    else:
        # عرض القائمة التفاعلية
        while True:
            print("\n" + "="*80)
            print("🚀 مرحباً بك في نظام توصية كتب البرمجة - إصدار سطر الأوامر")
            print("="*80)
            print("1. 🔍 البحث في الكتب")
            print("2. ⭐ عرض أعلى الكتب تقييماً")
            print("3. 📊 عرض الإحصائيات")
            print("4. 📂 عرض الفئات المتاحة")
            print("5. 💬 عرض اللغات البرمجية المتاحة")
            print("0. 🚪 خروج")
            print("="*80)
            
            try:
                choice = input("أدخل اختيارك (0-5): ").strip()
                
                if choice == '0':
                    print("👋 وداعاً!")
                    break
                elif choice == '1':
                    query = input("🔍 أدخل نص البحث: ").strip()
                    if query:
                        cli.search_books(query, max_results=10)
                elif choice == '2':
                    cli.show_top_rated(10)
                elif choice == '3':
                    cli.show_statistics()
                elif choice == '4':
                    cli.show_categories()
                elif choice == '5':
                    cli.show_languages()
                else:
                    print("❌ اختيار غير صحيح!")
                
                input("\n⏸️  اضغط Enter للمتابعة...")
                
            except KeyboardInterrupt:
                print("\n\n👋 وداعاً!")
                break
            except Exception as e:
                print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    main()