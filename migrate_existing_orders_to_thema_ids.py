#!/usr/bin/env python3
"""
Migration script voor het koppelen van bestaande orders aan thema_id's

Dit script:
1. Haalt alle orders op die een thema string hebben maar geen thema_id
2. Probeert voor elke order de juiste thema_id te vinden
3. Update de order met de gevonden thema_id
4. Rapporteert statistieken over de migratie
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.order import Order
from app.services.thema_service import get_thema_service
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_orders_to_thema_ids():
    """Migreer bestaande orders naar thema_id systeem"""
    db = SessionLocal()
    
    try:
        print("🔄 Starting migration: Orders → Thema IDs")
        print("=" * 50)
        
        # Haal alle orders op die een thema hebben maar geen thema_id
        orders_to_migrate = db.query(Order).filter(
            Order.thema.isnot(None),  # Heeft een thema string
            Order.thema != '',        # Niet leeg
            Order.thema != '-',       # Niet placeholder
            Order.thema_id.is_(None)  # Nog geen thema_id
        ).all()
        
        print(f"📊 Found {len(orders_to_migrate)} orders to migrate")
        
        if len(orders_to_migrate) == 0:
            print("✅ No orders need migration")
            return
        
        # Initialize thema service
        thema_service = get_thema_service(db)
        
        # Statistics
        stats = {
            'total': len(orders_to_migrate),
            'matched': 0,
            'not_matched': 0,
            'errors': 0,
            'thema_counts': {}
        }
        
        print("\n🔍 Processing orders...")
        
        for i, order in enumerate(orders_to_migrate, 1):
            try:
                thema_string = order.thema.strip()
                
                # Track thema string frequency
                if thema_string not in stats['thema_counts']:
                    stats['thema_counts'][thema_string] = {'count': 0, 'matched': 0}
                stats['thema_counts'][thema_string]['count'] += 1
                
                # Try to find matching thema_id
                thema_id = thema_service.find_thema_id_for_string(thema_string)
                
                if thema_id:
                    order.thema_id = thema_id
                    stats['matched'] += 1
                    stats['thema_counts'][thema_string]['matched'] += 1
                    logger.info(f"Order {order.order_id}: '{thema_string}' → thema_id {thema_id}")
                else:
                    stats['not_matched'] += 1
                    logger.warning(f"Order {order.order_id}: No match found for '{thema_string}'")
                
                # Progress indicator
                if i % 100 == 0 or i == len(orders_to_migrate):
                    print(f"  Processed {i}/{len(orders_to_migrate)} orders...")
                    
            except Exception as e:
                stats['errors'] += 1
                logger.error(f"Error processing order {order.order_id}: {str(e)}")
        
        # Commit all changes
        print("\n💾 Saving changes to database...")
        db.commit()
        
        # Print detailed statistics
        print("\n📈 Migration Results:")
        print("=" * 50)
        print(f"✅ Successfully matched: {stats['matched']}")
        print(f"❌ No match found: {stats['not_matched']}")
        print(f"🚫 Errors: {stats['errors']}")
        print(f"📊 Total processed: {stats['total']}")
        
        # Show thema string breakdown
        print("\n📋 Thema String Analysis:")
        print("-" * 30)
        for thema_str, counts in sorted(stats['thema_counts'].items(), 
                                       key=lambda x: x[1]['count'], reverse=True):
            match_rate = (counts['matched'] / counts['count']) * 100 if counts['count'] > 0 else 0
            print(f"'{thema_str}': {counts['matched']}/{counts['count']} matched ({match_rate:.1f}%)")
        
        # Success summary
        success_rate = (stats['matched'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
        
        if stats['not_matched'] > 0:
            print(f"\n💡 Tip: Consider adding missing themas to the database:")
            unmatched_themas = [thema for thema, counts in stats['thema_counts'].items() 
                              if counts['matched'] == 0]
            for thema in unmatched_themas[:10]:  # Show first 10
                print(f"   - '{thema}'")
            if len(unmatched_themas) > 10:
                print(f"   ... and {len(unmatched_themas) - 10} more")
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Migration failed: {str(e)}")
        print(f"\n❌ Migration failed: {str(e)}")
        raise
    finally:
        db.close()

def preview_migration():
    """Preview wat de migratie zou doen zonder wijzigingen"""
    db = SessionLocal()
    
    try:
        print("👁️  Migration Preview (No Changes)")
        print("=" * 40)
        
        # Get sample of orders to migrate
        orders_sample = db.query(Order).filter(
            Order.thema.isnot(None),
            Order.thema != '',
            Order.thema != '-',  
            Order.thema_id.is_(None)
        ).limit(20).all()
        
        if not orders_sample:
            print("No orders found for migration")
            return
            
        thema_service = get_thema_service(db)
        
        print(f"Sample of {len(orders_sample)} orders:")
        print("-" * 40)
        
        for order in orders_sample:
            thema_string = order.thema.strip()
            thema_id = thema_service.find_thema_id_for_string(thema_string)
            
            if thema_id:
                print(f"✅ Order {order.order_id}: '{thema_string}' → thema_id {thema_id}")
            else:
                print(f"❌ Order {order.order_id}: '{thema_string}' → NO MATCH")
        
        # Get total count
        total_count = db.query(Order).filter(
            Order.thema.isnot(None),
            Order.thema != '',
            Order.thema != '-',
            Order.thema_id.is_(None)
        ).count()
        
        print(f"\nTotal orders to migrate: {total_count}")
        
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        preview_migration()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage:")
        print("  python migrate_existing_orders_to_thema_ids.py          # Run migration")
        print("  python migrate_existing_orders_to_thema_ids.py --preview # Preview only")
        print("  python migrate_existing_orders_to_thema_ids.py --help   # Show this help")
    else:
        migrate_orders_to_thema_ids() 