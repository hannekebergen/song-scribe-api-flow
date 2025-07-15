#!/usr/bin/env python3
"""
Deploy Thema Data to Production
Script om lokale thema database naar productie te deployen
"""

import os
import sys
import json
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Voor lokale database query
from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaElement, ThemaRhymeSet

def get_production_connection():
    """Get production database connection"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print("Set it to your production database URL:")
        print("export DATABASE_URL='postgresql://user:password@host:port/database'")
        return None
    
    try:
        # Parse database URL
        if not database_url.startswith('postgresql://'):
            raise ValueError("DATABASE_URL must start with postgresql://")
        
        url_parts = database_url[13:]  # Remove 'postgresql://'
        auth_part, host_part = url_parts.split('@', 1)
        user, password = auth_part.split(':', 1)
        host_port, database = host_part.rsplit('/', 1)
        
        if ':' in host_port:
            host, port = host_port.split(':', 1)
            port = int(port)
        else:
            host = host_port
            port = 5432
        
        conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        
        # Test connection
        conn = psycopg2.connect(**conn_params)
        conn.close()
        
        return conn_params
    except Exception as e:
        print(f"❌ Error connecting to production database: {e}")
        return None

def export_local_thema_data():
    """Export all thema data from local database"""
    print("📊 Exporting local thema data...")
    
    db = SessionLocal()
    data = {
        'themas': [],
        'elements': [],
        'rhyme_sets': [],
        'export_date': datetime.now().isoformat()
    }
    
    try:
        # Export themas
        themas = db.query(Thema).all()
        for thema in themas:
            data['themas'].append({
                'name': thema.name,
                'display_name': thema.display_name,
                'description': thema.description,
                'is_active': thema.is_active,
            })
        
        # Export elements
        elements = db.query(ThemaElement).all()
        for element in elements:
            data['elements'].append({
                'thema_name': element.thema.name,
                'element_type': element.element_type,
                'content': element.content,
                'usage_context': element.usage_context,
                'weight': element.weight,
                'suno_format': element.suno_format,
            })
        
        # Export rhyme sets
        rhyme_sets = db.query(ThemaRhymeSet).all()
        for rhyme_set in rhyme_sets:
            data['rhyme_sets'].append({
                'thema_name': rhyme_set.thema.name,
                'rhyme_pattern': rhyme_set.rhyme_pattern,
                'words': rhyme_set.words,
                'difficulty_level': rhyme_set.difficulty_level,
            })
        
        print(f"✅ Exported {len(data['themas'])} themas")
        print(f"✅ Exported {len(data['elements'])} elements")
        print(f"✅ Exported {len(data['rhyme_sets'])} rhyme sets")
        
        return data
        
    except Exception as e:
        print(f"❌ Error exporting local data: {e}")
        return None
    finally:
        db.close()

def clear_production_thema_data(conn_params):
    """Clear existing thema data in production"""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("🗑️ Clearing existing production thema data...")
        
        # Delete in correct order (respect foreign keys)
        cursor.execute("DELETE FROM thema_rhyme_sets")
        cursor.execute("DELETE FROM thema_elements")
        cursor.execute("DELETE FROM themas")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Production thema data cleared")
        return True
        
    except Exception as e:
        print(f"❌ Error clearing production data: {e}")
        return False

def import_thema_data_to_production(conn_params, data):
    """Import thema data to production database"""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("⬆️ Importing thema data to production...")
        
        # Import themas first
        thema_id_map = {}
        for thema in data['themas']:
            cursor.execute("""
                INSERT INTO themas (name, display_name, description, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (
                thema['name'],
                thema['display_name'],
                thema['description'],
                thema['is_active']
            ))
            
            thema_id = cursor.fetchone()[0]
            thema_id_map[thema['name']] = thema_id
        
        print(f"✅ Imported {len(data['themas'])} themas")
        
        # Import elements
        for element in data['elements']:
            thema_id = thema_id_map.get(element['thema_name'])
            if thema_id:
                cursor.execute("""
                    INSERT INTO thema_elements (thema_id, element_type, content, usage_context, weight, suno_format, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (
                    thema_id,
                    element['element_type'],
                    element['content'],
                    element['usage_context'],
                    element['weight'],
                    element['suno_format']
                ))
        
        print(f"✅ Imported {len(data['elements'])} elements")
        
        # Import rhyme sets
        for rhyme_set in data['rhyme_sets']:
            thema_id = thema_id_map.get(rhyme_set['thema_name'])
            if thema_id:
                cursor.execute("""
                    INSERT INTO thema_rhyme_sets (thema_id, rhyme_pattern, words, difficulty_level, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (
                    thema_id,
                    rhyme_set['rhyme_pattern'],
                    rhyme_set['words'],
                    rhyme_set['difficulty_level']
                ))
        
        print(f"✅ Imported {len(data['rhyme_sets'])} rhyme sets")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing to production: {e}")
        return False

def verify_production_data(conn_params):
    """Verify the imported data in production"""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("🔍 Verifying production data...")
        
        # Count themas
        cursor.execute("SELECT COUNT(*) FROM themas")
        thema_count = cursor.fetchone()[0]
        
        # Count elements
        cursor.execute("SELECT COUNT(*) FROM thema_elements")
        element_count = cursor.fetchone()[0]
        
        # Count rhyme sets  
        cursor.execute("SELECT COUNT(*) FROM thema_rhyme_sets")
        rhyme_count = cursor.fetchone()[0]
        
        # Get thema details
        cursor.execute("SELECT name, display_name, (SELECT COUNT(*) FROM thema_elements WHERE thema_id = themas.id) as element_count FROM themas ORDER BY name")
        themas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"\n📊 PRODUCTION DATA VERIFICATION:")
        print(f"Total themas: {thema_count}")
        print(f"Total elements: {element_count}")
        print(f"Total rhyme sets: {rhyme_count}")
        print(f"\n📋 THEMAS:")
        
        for thema in themas:
            print(f"  • {thema[1]} ({thema[0]}) - {thema[2]} elements")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying production data: {e}")
        return False

def save_backup_file(data):
    """Save data to backup file"""
    filename = f"thema_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Backup saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving backup: {e}")
        return None

def main():
    """Main deployment function"""
    print("🚀 THEMA DATA DEPLOYMENT TO PRODUCTION")
    print("=" * 50)
    
    # Step 1: Export local data
    local_data = export_local_thema_data()
    if not local_data:
        print("❌ Failed to export local data")
        return
    
    # Step 2: Save backup
    backup_file = save_backup_file(local_data)
    if not backup_file:
        print("❌ Failed to save backup")
        return
    
    # Step 3: Get production connection
    conn_params = get_production_connection()
    if not conn_params:
        print("❌ Failed to connect to production database")
        return
    
    # Step 4: Confirm deployment
    print(f"\n⚠️  DEPLOYMENT CONFIRMATION")
    print(f"   Local data: {len(local_data['themas'])} themas, {len(local_data['elements'])} elements")
    print(f"   Backup file: {backup_file}")
    print(f"   Production: {conn_params['host']}")
    
    confirm = input(f"\n❓ Deploy to production? This will REPLACE all existing thema data! (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Deployment cancelled")
        return
    
    # Step 5: Clear production data
    if not clear_production_thema_data(conn_params):
        print("❌ Failed to clear production data")
        return
    
    # Step 6: Import to production
    if not import_thema_data_to_production(conn_params, local_data):
        print("❌ Failed to import to production")
        return
    
    # Step 7: Verify
    if not verify_production_data(conn_params):
        print("❌ Failed to verify production data")
        return
    
    print(f"\n🎉 DEPLOYMENT SUCCESSFUL!")
    print(f"   • {len(local_data['themas'])} themas deployed")
    print(f"   • {len(local_data['elements'])} elements deployed")
    print(f"   • {len(local_data['rhyme_sets'])} rhyme sets deployed")
    print(f"   • Backup saved: {backup_file}")
    
    print(f"\n🔄 NEXT STEPS:")
    print(f"   1. Test the production frontend")
    print(f"   2. Verify thema data appears correctly")
    print(f"   3. Test AI prompt generation with new data")

if __name__ == "__main__":
    main() 