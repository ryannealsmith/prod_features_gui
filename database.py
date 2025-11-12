"""
Database schema and operations for Product Features application.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class Database:
    def __init__(self, db_path='product_features.db'):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Connect to the database."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
        
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            
    def create_tables(self):
        """Create all database tables."""
        cursor = self.connection.cursor()
        
        # Product Features table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                platform TEXT,
                odd TEXT,
                environment TEXT,
                trailer TEXT,
                details TEXT,
                comments TEXT,
                when_date TEXT,
                start_date DATE,
                trl3_date DATE,
                trl6_date DATE,
                trl9_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Capabilities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS capabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                swimlane TEXT,
                sl TEXT,
                maj REAL,
                min REAL,
                label TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                platform TEXT,
                odd TEXT,
                environment TEXT,
                trailer TEXT,
                details TEXT,
                when_date TEXT,
                dependencies TEXT,
                dependents TEXT,
                start_date DATE,
                trl3_date DATE,
                trl6_date DATE,
                trl9_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Technical Functions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                swimlane TEXT,
                sl TEXT,
                maj REAL,
                min REAL,
                label TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                platform TEXT,
                odd TEXT,
                environment TEXT,
                trailer TEXT,
                details TEXT,
                next TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Many-to-many: Product Features to Capabilities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pf_capabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_feature_id INTEGER NOT NULL,
                capability_id INTEGER NOT NULL,
                FOREIGN KEY (product_feature_id) REFERENCES product_features(id) ON DELETE CASCADE,
                FOREIGN KEY (capability_id) REFERENCES capabilities(id) ON DELETE CASCADE,
                UNIQUE(product_feature_id, capability_id)
            )
        ''')
        
        # Many-to-many: Capabilities to Technical Functions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cap_technical_functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capability_id INTEGER NOT NULL,
                technical_function_id INTEGER NOT NULL,
                FOREIGN KEY (capability_id) REFERENCES capabilities(id) ON DELETE CASCADE,
                FOREIGN KEY (technical_function_id) REFERENCES technical_functions(id) ON DELETE CASCADE,
                UNIQUE(capability_id, technical_function_id)
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pf_label ON product_features(label)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cap_label ON capabilities(label)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tf_label ON technical_functions(label)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pf_cap_pf ON pf_capabilities(product_feature_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pf_cap_cap ON pf_capabilities(capability_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cap_tf_cap ON cap_technical_functions(capability_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cap_tf_tf ON cap_technical_functions(technical_function_id)')
        
        self.connection.commit()
        
    # CRUD operations for Product Features
    def add_product_feature(self, data: Dict) -> int:
        """Add a new product feature."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO product_features 
            (label, name, platform, odd, environment, trailer, details, comments, 
             when_date, start_date, trl3_date, trl6_date, trl9_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('comments'), data.get('when_date'),
            data.get('start_date'), data.get('trl3_date'), 
            data.get('trl6_date'), data.get('trl9_date')
        ))
        self.connection.commit()
        return cursor.lastrowid
        
    def get_product_features(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all product features with optional filters."""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM product_features WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('platform'):
                # Hierarchical: Terberg-1.3 includes 1.2, 1.1, 1
                platform = filters['platform']
                if platform.startswith('Terberg-'):
                    # Extract versions: Terberg-1.3 includes Terberg-1.2, Terberg-1.1, Terberg-1
                    base = platform.split('-')[1]  # e.g., "1.3"
                    parts = base.split('.')
                    included = ['Terberg-' + parts[0]]  # Base version (Terberg-1)
                    
                    # Add intermediate versions
                    if len(parts) > 1:
                        for i in range(1, int(parts[1]) + 1):
                            included.append(f'Terberg-{parts[0]}.{i}')
                    
                    query += ' AND platform IN ({})'.format(','.join('?' * len(included)))
                    params.extend(included)
                else:
                    query += ' AND platform = ?'
                    params.append(platform)
                    
            if filters.get('odd'):
                # Hierarchical: CFG-ODD-2 > CFG-ODD-1.1 > CFG-ODD-1
                odd = filters['odd']
                if odd.startswith('CFG-ODD-'):
                    version = odd.replace('CFG-ODD-', '')
                    included = ['CFG-ODD-1']  # Always include base
                    
                    if version == '1.1' or version == '2':
                        included.append('CFG-ODD-1.1')
                    if version == '2':
                        included.append('CFG-ODD-2')
                    elif '.' in version:
                        included.append(odd)
                    
                    query += ' AND odd IN ({})'.format(','.join('?' * len(included)))
                    params.extend(included)
                else:
                    query += ' AND odd = ?'
                    params.append(odd)
                    
            if filters.get('environment'):
                # CFG-ENV-2.1 includes CFG-ENV-1.1, so show both
                env = filters['environment']
                if env == 'CFG-ENV-2.1':
                    query += ' AND (environment = ? OR environment = ?)'
                    params.append('CFG-ENV-2.1')
                    params.append('CFG-ENV-1.1')
                else:
                    query += ' AND environment = ?'
                    params.append(env)
            if filters.get('trailer'):
                query += ' AND trailer = ?'
                params.append(filters['trailer'])
                
        query += ' ORDER BY label'
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def get_product_feature_by_id(self, pf_id: int) -> Optional[Dict]:
        """Get a product feature by ID."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM product_features WHERE id = ?', (pf_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def update_product_feature(self, pf_id: int, data: Dict):
        """Update a product feature."""
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE product_features 
            SET label=?, name=?, platform=?, odd=?, environment=?, trailer=?,
                details=?, comments=?, when_date=?, start_date=?, trl3_date=?,
                trl6_date=?, trl9_date=?, updated_at=CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('comments'), data.get('when_date'),
            data.get('start_date'), data.get('trl3_date'), 
            data.get('trl6_date'), data.get('trl9_date'), pf_id
        ))
        self.connection.commit()
        
    def delete_product_feature(self, pf_id: int):
        """Delete a product feature."""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM product_features WHERE id = ?', (pf_id,))
        self.connection.commit()
        
    # CRUD operations for Capabilities
    def add_capability(self, data: Dict) -> int:
        """Add a new capability."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO capabilities 
            (swimlane, sl, maj, min, label, name, platform, odd, environment, 
             trailer, details, when_date, dependencies, dependents, start_date, 
             trl3_date, trl6_date, trl9_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('swimlane'), data.get('sl'), data.get('maj'), data.get('min'),
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('when_date'), data.get('dependencies'),
            data.get('dependents'), data.get('start_date'), data.get('trl3_date'),
            data.get('trl6_date'), data.get('trl9_date')
        ))
        self.connection.commit()
        return cursor.lastrowid
        
    def get_capabilities(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all capabilities with optional filters."""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM capabilities WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('platform'):
                # Hierarchical: Terberg-1.3 includes 1.2, 1.1, 1
                platform = filters['platform']
                if platform.startswith('Terberg-'):
                    # Extract versions: Terberg-1.3 includes Terberg-1.2, Terberg-1.1, Terberg-1
                    base = platform.split('-')[1]  # e.g., "1.3"
                    parts = base.split('.')
                    included = ['Terberg-' + parts[0]]  # Base version (Terberg-1)
                    
                    # Add intermediate versions
                    if len(parts) > 1:
                        for i in range(1, int(parts[1]) + 1):
                            included.append(f'Terberg-{parts[0]}.{i}')
                    
                    query += ' AND platform IN ({})'.format(','.join('?' * len(included)))
                    params.extend(included)
                else:
                    query += ' AND platform = ?'
                    params.append(platform)
                    
            if filters.get('swimlane'):
                query += ' AND swimlane = ?'
                params.append(filters['swimlane'])
                
            if filters.get('odd'):
                # Hierarchical: CFG-ODD-2 > CFG-ODD-1.1 > CFG-ODD-1
                odd = filters['odd']
                if odd.startswith('CFG-ODD-'):
                    version = odd.replace('CFG-ODD-', '')
                    included = ['CFG-ODD-1']  # Always include base
                    
                    if version == '1.1' or version == '2':
                        included.append('CFG-ODD-1.1')
                    if version == '2':
                        included.append('CFG-ODD-2')
                    elif '.' in version:
                        included.append(odd)
                    
                    query += ' AND odd IN ({})'.format(','.join('?' * len(included)))
                    params.extend(included)
                else:
                    query += ' AND odd = ?'
                    params.append(odd)
                    
            if filters.get('environment'):
                # CFG-ENV-2.1 includes CFG-ENV-1.1, so show both
                env = filters['environment']
                if env == 'CFG-ENV-2.1':
                    query += ' AND (environment = ? OR environment = ?)'
                    params.append('CFG-ENV-2.1')
                    params.append('CFG-ENV-1.1')
                else:
                    query += ' AND environment = ?'
                    params.append(env)
            if filters.get('trailer'):
                query += ' AND trailer = ?'
                params.append(filters['trailer'])
                
        query += ' ORDER BY label'
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def get_capability_by_id(self, cap_id: int) -> Optional[Dict]:
        """Get a capability by ID."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM capabilities WHERE id = ?', (cap_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def update_capability(self, cap_id: int, data: Dict):
        """Update a capability."""
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE capabilities 
            SET swimlane=?, sl=?, maj=?, min=?, label=?, name=?, platform=?, 
                odd=?, environment=?, trailer=?, details=?, when_date=?,
                dependencies=?, dependents=?, start_date=?, trl3_date=?,
                trl6_date=?, trl9_date=?, updated_at=CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('swimlane'), data.get('sl'), data.get('maj'), data.get('min'),
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('when_date'), data.get('dependencies'),
            data.get('dependents'), data.get('start_date'), data.get('trl3_date'),
            data.get('trl6_date'), data.get('trl9_date'), cap_id
        ))
        self.connection.commit()
        
    def delete_capability(self, cap_id: int):
        """Delete a capability."""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM capabilities WHERE id = ?', (cap_id,))
        self.connection.commit()
        
    # CRUD operations for Technical Functions
    def add_technical_function(self, data: Dict) -> int:
        """Add a new technical function."""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO technical_functions 
            (swimlane, sl, maj, min, label, name, platform, odd, environment, 
             trailer, details, next)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('swimlane'), data.get('sl'), data.get('maj'), data.get('min'),
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('next')
        ))
        self.connection.commit()
        return cursor.lastrowid
        
    def get_technical_functions(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all technical functions with optional filters."""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM technical_functions WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('platform'):
                query += ' AND platform = ?'
                params.append(filters['platform'])
            if filters.get('swimlane'):
                query += ' AND swimlane = ?'
                params.append(filters['swimlane'])
                
        query += ' ORDER BY label'
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def get_technical_function_by_id(self, tf_id: int) -> Optional[Dict]:
        """Get a technical function by ID."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM technical_functions WHERE id = ?', (tf_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def update_technical_function(self, tf_id: int, data: Dict):
        """Update a technical function."""
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE technical_functions 
            SET swimlane=?, sl=?, maj=?, min=?, label=?, name=?, platform=?,
                odd=?, environment=?, trailer=?, details=?, next=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('swimlane'), data.get('sl'), data.get('maj'), data.get('min'),
            data.get('label'), data.get('name'), data.get('platform'),
            data.get('odd'), data.get('environment'), data.get('trailer'),
            data.get('details'), data.get('next'), tf_id
        ))
        self.connection.commit()
        
    def delete_technical_function(self, tf_id: int):
        """Delete a technical function."""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM technical_functions WHERE id = ?', (tf_id,))
        self.connection.commit()
        
    # Relationship operations
    def link_pf_capability(self, pf_id: int, cap_id: int):
        """Link a product feature to a capability."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO pf_capabilities (product_feature_id, capability_id)
                VALUES (?, ?)
            ''', (pf_id, cap_id))
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass  # Link already exists
            
    def unlink_pf_capability(self, pf_id: int, cap_id: int):
        """Unlink a product feature from a capability."""
        cursor = self.connection.cursor()
        cursor.execute('''
            DELETE FROM pf_capabilities 
            WHERE product_feature_id = ? AND capability_id = ?
        ''', (pf_id, cap_id))
        self.connection.commit()
        
    def get_pf_capabilities(self, pf_id: int) -> List[Dict]:
        """Get all capabilities for a product feature."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT c.* FROM capabilities c
            JOIN pf_capabilities pc ON c.id = pc.capability_id
            WHERE pc.product_feature_id = ?
            ORDER BY c.label
        ''', (pf_id,))
        return [dict(row) for row in cursor.fetchall()]
        
    def link_cap_tf(self, cap_id: int, tf_id: int):
        """Link a capability to a technical function."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO cap_technical_functions (capability_id, technical_function_id)
                VALUES (?, ?)
            ''', (cap_id, tf_id))
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass  # Link already exists
            
    def unlink_cap_tf(self, cap_id: int, tf_id: int):
        """Unlink a capability from a technical function."""
        cursor = self.connection.cursor()
        cursor.execute('''
            DELETE FROM cap_technical_functions 
            WHERE capability_id = ? AND technical_function_id = ?
        ''', (cap_id, tf_id))
        self.connection.commit()
        
    def get_cap_technical_functions(self, cap_id: int) -> List[Dict]:
        """Get all technical functions for a capability."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT tf.* FROM technical_functions tf
            JOIN cap_technical_functions ctf ON tf.id = ctf.technical_function_id
            WHERE ctf.capability_id = ?
            ORDER BY tf.label
        ''', (cap_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_cap_product_features(self, cap_id: int) -> List[Dict]:
        """Get all product features for a capability."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT pf.* FROM product_features pf
            JOIN pf_capabilities pc ON pf.id = pc.product_feature_id
            WHERE pc.capability_id = ?
            ORDER BY pf.label
        ''', (cap_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_tf_capabilities(self, tf_id: int) -> List[Dict]:
        """Get all capabilities for a technical function."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT c.* FROM capabilities c
            JOIN cap_technical_functions ctf ON c.id = ctf.capability_id
            WHERE ctf.technical_function_id = ?
            ORDER BY c.label
        ''', (tf_id,))
        return [dict(row) for row in cursor.fetchall()]
        
    def get_unique_values(self, table: str, column: str) -> List[str]:
        """Get unique values from a column for filter dropdowns."""
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL ORDER BY {column}')
        return [row[0] for row in cursor.fetchall()]
