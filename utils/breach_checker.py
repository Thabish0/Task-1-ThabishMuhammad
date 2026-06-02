import sqlite3
import os
import hashlib

class BreachChecker:
    def __init__(self, db_path='database/breached_passwords.db', common_path='database/common_passwords.txt'):
        self.db_path = db_path
        self.common_path = common_path
        self.common_passwords = set()
        self.init_database()
        self.load_common_passwords()
    
    def init_database(self):
        """Initialize SQLite database with breached passwords"""
        os.makedirs('database', exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS breached_passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT UNIQUE,
                hash_sha256 TEXT,
                breach_count INTEGER DEFAULT 1
            )
        ''')
        
        # Insert common breached passwords
        breached_list = [
            '123456', 'password', '123456789', '12345', '12345678', 'qwerty', 'abc123',
            'admin', 'welcome', 'letmein', 'password1', '123123', 'iloveyou', 'sunshine',
            'qwerty123', 'admin123', 'football', 'monkey', 'login', 'master', 'hello',
            'whatever', 'dragon', 'passw0rd', 'trustno1', 'princess', 'adminadmin'
        ]
        
        for pwd in breached_list:
            pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
            try:
                cursor.execute('INSERT OR IGNORE INTO breached_passwords (password, hash_sha256) VALUES (?, ?)',
                             (pwd, pwd_hash))
            except:
                pass
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized with {len(breached_list)} breached passwords")
    
    def load_common_passwords(self):
        """Load common passwords from text file"""
        try:
            if os.path.exists(self.common_path):
                with open(self.common_path, 'r', encoding='utf-8') as f:
                    self.common_passwords = set(line.strip().lower() for line in f if line.strip())
                print(f"✅ Loaded {len(self.common_passwords)} common passwords")
            else:
                # Create default common passwords file
                os.makedirs('database', exist_ok=True)
                default_passwords = [
                    '123456', 'password', '12345678', 'qwerty', 'abc123', 'monkey', 'dragon',
                    'letmein', 'admin', 'welcome', 'master', 'sunshine', 'password1', 'iloveyou'
                ]
                with open(self.common_path, 'w', encoding='utf-8') as f:
                    for pwd in default_passwords:
                        f.write(pwd + '\n')
                self.common_passwords = set(default_passwords)
                print(f"✅ Created common passwords file with {len(default_passwords)} entries")
        except Exception as e:
            print(f"⚠️ Error loading common passwords: {e}")
            self.common_passwords = set()
    
    def check_breach(self, password):
        """
        Check if password appears in breach database or common passwords
        Returns dict with status and risk level
        """
        if not password:
            return {'breached': False, 'risk_level': 'none', 'message': 'No password provided'}
        
        password_lower = password.lower()
        
        # Check common passwords
        if password_lower in self.common_passwords:
            return {
                'breached': True,
                'risk_level': 'critical',
                'message': '⚠️ This password is commonly used and appears in breach databases!'
            }
        
        # Check SQLite database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('SELECT password FROM breached_passwords WHERE password = ? OR hash_sha256 = ?',
                         (password, pwd_hash))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'breached': True,
                    'risk_level': 'high',
                    'message': '⚠️ This password has appeared in known data breaches!'
                }
        except Exception as e:
            print(f"Database error: {e}")
        
        return {
            'breached': False,
            'risk_level': 'none',
            'message': '✅ Password not found in breach database'
        }
    
    def add_breached_password(self, password):
        """Add a new breached password to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('INSERT OR IGNORE INTO breached_passwords (password, hash_sha256) VALUES (?, ?)',
                         (password, pwd_hash))
            conn.commit()
            conn.close()
            return True
        except:
            return False