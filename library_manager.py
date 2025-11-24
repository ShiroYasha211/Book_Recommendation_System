import sqlite3
from typing import List, Dict, Optional

class LibraryManager:    
    def __init__(self, db_path: str = "my_library.db"):
        self.db_path = db_path
        self._create_database()
    
    def _create_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # إنشاء جدول المكتبة الشخصية
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT,
                description TEXT,
                personal_rating REAL,
                reading_status TEXT DEFAULT 'لم أقرأ بعد',
                tags TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_book(self, title: str, author: str, category: str = "", 
                 description: str = "", personal_rating: float = 0, 
                 reading_status: str = "لم أقرأ بعد", tags: str = "") -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO my_library (title, author, category, description, 
                                  personal_rating, reading_status, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, category, description, personal_rating, 
              reading_status, tags))
        
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return book_id
    
    def get_all_books(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, author, category, description, 
                   personal_rating, reading_status, tags, date_added
            FROM my_library 
            ORDER BY date_added DESC
        """)
        
        books = []
        for row in cursor.fetchall():
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'category': row[3],
                'description': row[4],
                'personal_rating': row[5],
                'reading_status': row[6],
                'tags': row[7],
                'date_added': row[8]
            })
        
        conn.close()
        return books
    
    def search_books(self, query: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT id, title, author, category, description, 
                   personal_rating, reading_status, tags, date_added
            FROM my_library 
            WHERE title LIKE ? OR author LIKE ? OR tags LIKE ?
            ORDER BY date_added DESC
        """, (search_term, search_term, search_term))
        
        books = []
        for row in cursor.fetchall():
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'category': row[3],
                'description': row[4],
                'personal_rating': row[5],
                'reading_status': row[6],
                'tags': row[7],
                'date_added': row[8]
            })
        
        conn.close()
        return books
    
    def update_book(self, book_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # بناء استعلام UPDATE ديناميكياً
        fields = []
        values = []
        
        for field, value in kwargs.items():
            if field in ['title', 'author', 'category', 'description', 
                        'personal_rating', 'reading_status', 'tags']:
                fields.append(f"{field} = ?")
                values.append(value)
        
        if not fields:
            conn.close()
            return False
        
        values.append(book_id)
        query = f"UPDATE my_library SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete_book(self, book_id: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM my_library WHERE id = ?", (book_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, author, category, description, 
                   personal_rating, reading_status, tags, date_added
            FROM my_library 
            WHERE id = ?
        """, (book_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'category': row[3],
                'description': row[4],
                'personal_rating': row[5],
                'reading_status': row[6],
                'tags': row[7],
                'date_added': row[8]
            }
        return None
    
    def get_statistics(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # إجمالي الكتب
        cursor.execute("SELECT COUNT(*) FROM my_library")
        total_books = cursor.fetchone()[0]
        
        # حالة القراءة
        cursor.execute("""
            SELECT reading_status, COUNT(*) 
            FROM my_library 
            GROUP BY reading_status
        """)
        reading_stats = dict(cursor.fetchall())
        
        # متوسط التقييم
        cursor.execute("""
            SELECT AVG(personal_rating) 
            FROM my_library 
            WHERE personal_rating > 0
        """)
        avg_rating = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_books': total_books,
            'reading_stats': reading_stats,
            'average_rating': round(avg_rating, 1) if avg_rating else 0
        }
    
    def reset_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM my_library")
        conn.commit()
        conn.close()
