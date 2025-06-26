#!/usr/bin/env python3
"""
Migration script: Orders naar Database-Driven Prompts
Voegt thema_id toe aan bestaande orders voor database-gekoppelde promptgeneratie
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.db.session import SessionLocal
from app.models.order import Order
from app.models.thema import Thema
from app.services.thema_service import ThemaService

def migrate_orders_to_database_prompts():
    """Migreer bestaande orders naar database-driven prompt systeem"""
    db = SessionLocal()
    
    try:
        print("🔄 Migrating Orders to Database-Driven Prompts\n")
        
        # Statistics
        total_orders = db.query(Order).count()
        orders_without_thema_id = db.query(Order).filter(Order.thema_id.is_(None)).count()
        
        print(f"📊 Migration Statistics:")
        print(f"   Total orders: {total_orders}")
        print(f"   Orders without thema_id: {orders_without_thema_id}")
        print(f"   Orders to migrate: {orders_without_thema_id}\n")
        
        if orders_without_thema_id == 0:
            print("✅ All orders already have thema_id assigned!")
            return
        
        thema_service = ThemaService(db)
        
        # Get all available themas for reference
        available_themas = db.query(Thema).filter(Thema.is_active == True).all()
        print(f"🎵 Available themas in database:")
        for thema in available_themas:
            print(f"   - {thema.name} ({thema.display_name}) - ID: {thema.id}")
        print()
        
        # Migrate orders batch by batch
        batch_size = 100
        migrated_count = 0
        failed_count = 0
        
        orders_to_migrate = db.query(Order).filter(Order.thema_id.is_(None)).limit(batch_size)
        
        while True:
            batch = orders_to_migrate.all()
            if not batch:
                break
                
            print(f"🔄 Processing batch of {len(batch)} orders...")
            
            for order in batch:
                try:
                    # Try to find matching thema_id for the order's thema string
                    if order.thema:
                        thema_id = thema_service.find_thema_id_for_string(order.thema)
                        
                        if thema_id:
                            order.thema_id = thema_id
                            migrated_count += 1
                            print(f"   ✅ Order {order.order_id}: '{order.thema}' → thema_id {thema_id}")
                        else:
                            # No exact match found, try partial matching
                            fallback_thema_id = _find_fallback_thema(order.thema, available_themas)
                            if fallback_thema_id:
                                order.thema_id = fallback_thema_id
                                migrated_count += 1
                                print(f"   🔄 Order {order.order_id}: '{order.thema}' → fallback thema_id {fallback_thema_id}")
                            else:
                                failed_count += 1
                                print(f"   ❌ Order {order.order_id}: No match for '{order.thema}'")
                    else:
                        # No thema string, assign default
                        default_thema = db.query(Thema).filter(Thema.name == 'verjaardag').first()
                        if default_thema:
                            order.thema_id = default_thema.id
                            migrated_count += 1
                            print(f"   🔄 Order {order.order_id}: No thema → default thema_id {default_thema.id}")
                        else:
                            failed_count += 1
                            print(f"   ❌ Order {order.order_id}: No thema and no default available")
                            
                except Exception as e:
                    failed_count += 1
                    print(f"   ❌ Order {order.order_id}: Error - {str(e)}")
            
            # Commit batch changes
            try:
                db.commit()
                print(f"   💾 Batch committed successfully\n")
            except Exception as e:
                db.rollback()
                print(f"   ❌ Batch commit failed: {str(e)}\n")
                break
            
            # Get next batch
            orders_to_migrate = db.query(Order).filter(Order.thema_id.is_(None)).limit(batch_size)
        
        # Final statistics
        print(f"🎉 Migration completed!")
        print(f"   ✅ Successfully migrated: {migrated_count} orders")
        print(f"   ❌ Failed migrations: {failed_count} orders")
        
        # Verify results
        remaining_without_thema_id = db.query(Order).filter(Order.thema_id.is_(None)).count()
        print(f"   📊 Orders still without thema_id: {remaining_without_thema_id}")
        
        if remaining_without_thema_id == 0:
            print("   🎯 100% migration success!")
        else:
            print("   ⚠️ Some orders still need manual review")
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

def _find_fallback_thema(thema_string: str, available_themas: list) -> int:
    """Find fallback thema using fuzzy matching"""
    if not thema_string:
        return None
        
    thema_lower = thema_string.lower().strip()
    
    # Common mappings
    mappings = {
        'birthday': 'verjaardag',
        'love': 'liefde',
        'romance': 'liefde',
        'wedding': 'liefde',
        'goodbye': 'afscheid',
        'farewell': 'afscheid',
        'thank': 'bedankt',
        'thanks': 'bedankt',
        'appreciation': 'bedankt'
    }
    
    # Try direct mapping
    mapped_name = mappings.get(thema_lower)
    if mapped_name:
        for thema in available_themas:
            if thema.name == mapped_name:
                return thema.id
    
    # Try partial matching on any thema
    for thema in available_themas:
        if (thema_lower in thema.name.lower() or 
            thema.name.lower() in thema_lower or
            thema_lower in thema.display_name.lower()):
            return thema.id
    
    return None

def verify_database_prompt_readiness():
    """Verify that the system is ready for database-driven prompts"""
    db = SessionLocal()
    
    try:
        print("🔍 Verifying Database-Driven Prompt Readiness\n")
        
        # Check thema data
        thema_count = db.query(Thema).filter(Thema.is_active == True).count()
        print(f"Active themas: {thema_count}")
        
        if thema_count == 0:
            print("❌ No active themas found! Run seed_thema_database.py first")
            return False
        
        # Check orders with thema_id
        orders_with_thema_id = db.query(Order).filter(Order.thema_id.isnot(None)).count()
        total_orders = db.query(Order).count()
        coverage_percentage = (orders_with_thema_id / total_orders * 100) if total_orders > 0 else 0
        
        print(f"Orders with thema_id: {orders_with_thema_id}/{total_orders} ({coverage_percentage:.1f}%)")
        
        if coverage_percentage < 80:
            print(f"⚠️ Only {coverage_percentage:.1f}% of orders have thema_id. Consider running migration.")
        else:
            print("✅ Good thema_id coverage")
        
        # Test prompt generation
        test_order = db.query(Order).filter(Order.thema_id.isnot(None)).first()
        if test_order:
            print(f"✅ Found test order: {test_order.order_id} with thema_id: {test_order.thema_id}")
            return True
        else:
            print("❌ No orders with thema_id found for testing")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Migrate orders to database-driven prompts')
    parser.add_argument('--verify', action='store_true', help='Only verify readiness, don\'t migrate')
    parser.add_argument('--force', action='store_true', help='Force migration even if already done')
    
    args = parser.parse_args()
    
    if args.verify:
        verify_database_prompt_readiness()
    else:
        migrate_orders_to_database_prompts() 