#!/usr/bin/env python3
"""
Performance Monitor voor Database-Driven Prompts
Vergelijkt performance en kwaliteit tussen static en database prompts
"""

import sys
import os
import time
import statistics
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.order import Order
from app.templates.prompt_templates import generate_prompt, generate_enhanced_prompt

def monitor_prompt_performance(sample_size: int = 10):
    """Monitor prompt generation performance"""
    db = SessionLocal()
    
    try:
        print("📊 Prompt Generation Performance Monitor\n")
        
        # Get sample orders with thema_id
        sample_orders = (db.query(Order)
                        .filter(Order.thema_id.isnot(None))
                        .limit(sample_size)
                        .all())
        
        if not sample_orders:
            print("❌ No orders with thema_id found!")
            return
        
        print(f"🎯 Testing with {len(sample_orders)} orders\n")
        
        # Performance metrics
        static_times = []
        enhanced_times = []
        suno_times = []
        
        static_lengths = []
        enhanced_lengths = []
        suno_lengths = []
        
        print("🔍 Performance Tests:")
        print("-" * 60)
        
        for i, order in enumerate(sample_orders, 1):
            print(f"Order {i}/{len(sample_orders)}: {order.order_id}")
            
            # Prepare song data
            song_data = {
                "ontvanger": order.voornaam or "Test",
                "van": order.klant_naam or "Test",
                "beschrijving": order.beschrijving or "Test beschrijving",
                "stijl": order.thema or "verjaardag",
                "extra_wens": getattr(order, 'persoonlijk_verhaal', None) or "Geen extra wensen"
            }
            
            # Test 1: Static template
            start_time = time.time()
            static_prompt = generate_prompt(song_data)
            static_time = time.time() - start_time
            static_times.append(static_time)
            static_lengths.append(len(static_prompt))
            
            # Test 2: Enhanced database prompt
            start_time = time.time()
            enhanced_prompt = generate_enhanced_prompt(
                song_data=song_data,
                db=db,
                use_suno=False,
                thema_id=order.thema_id
            )
            enhanced_time = time.time() - start_time
            enhanced_times.append(enhanced_time)
            enhanced_lengths.append(len(enhanced_prompt))
            
            # Test 3: Suno.ai optimized prompt
            start_time = time.time()
            suno_prompt = generate_enhanced_prompt(
                song_data=song_data,
                db=db,
                use_suno=True,
                thema_id=order.thema_id
            )
            suno_time = time.time() - start_time
            suno_times.append(suno_time)
            suno_lengths.append(len(suno_prompt))
            
            print(f"   Static: {static_time*1000:.1f}ms ({len(static_prompt)} chars)")
            print(f"   Enhanced: {enhanced_time*1000:.1f}ms ({len(enhanced_prompt)} chars)")
            print(f"   Suno: {suno_time*1000:.1f}ms ({len(suno_prompt)} chars)")
            print()
        
        # Calculate statistics
        print("📈 Performance Statistics:")
        print("=" * 60)
        
        print(f"⏱️ Average Generation Time:")
        print(f"   Static Template:    {statistics.mean(static_times)*1000:.1f}ms")
        print(f"   Enhanced Database:  {statistics.mean(enhanced_times)*1000:.1f}ms")
        print(f"   Suno.ai Optimized:  {statistics.mean(suno_times)*1000:.1f}ms")
        
        print(f"\n📏 Average Prompt Length:")
        print(f"   Static Template:    {statistics.mean(static_lengths):.0f} characters")
        print(f"   Enhanced Database:  {statistics.mean(enhanced_lengths):.0f} characters")
        print(f"   Suno.ai Optimized:  {statistics.mean(suno_lengths):.0f} characters")
        
        # Performance ratios
        db_overhead = (statistics.mean(enhanced_times) / statistics.mean(static_times) - 1) * 100
        suno_overhead = (statistics.mean(suno_times) / statistics.mean(static_times) - 1) * 100
        
        print(f"\n⚡ Performance Overhead:")
        print(f"   Database queries:   {db_overhead:+.1f}%")
        print(f"   Suno optimization:  {suno_overhead:+.1f}%")
        
        # Quality indicators
        print(f"\n🎯 Quality Indicators:")
        enhanced_with_elements = sum(1 for i in range(len(sample_orders)) 
                                   if "THEMA-SPECIFIEKE ELEMENTEN:" in 
                                   generate_enhanced_prompt(
                                       {"ontvanger": "Test", "van": "Test", "beschrijving": "Test", 
                                        "stijl": "verjaardag", "extra_wens": "Test"},
                                       db, False, sample_orders[i].thema_id))
        
        suno_with_tags = sum(1 for i in range(len(sample_orders)) 
                           if "[intro]" in generate_enhanced_prompt(
                               {"ontvanger": "Test", "van": "Test", "beschrijving": "Test", 
                                "stijl": "verjaardag", "extra_wens": "Test"},
                               db, True, sample_orders[i].thema_id))
        
        print(f"   Enhanced prompts with DB elements: {enhanced_with_elements}/{len(sample_orders)} ({enhanced_with_elements/len(sample_orders)*100:.0f}%)")
        print(f"   Suno prompts with music tags:       {suno_with_tags}/{len(sample_orders)} ({suno_with_tags/len(sample_orders)*100:.0f}%)")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if db_overhead < 50:
            print("   ✅ Database overhead is acceptable (<50%)")
        else:
            print("   ⚠️ Consider caching thema data to reduce database overhead")
        
        if enhanced_with_elements / len(sample_orders) > 0.8:
            print("   ✅ Good database element coverage")
        else:
            print("   ⚠️ Some themas may need more database elements")
        
        if statistics.mean(enhanced_lengths) > statistics.mean(static_lengths):
            print("   ✅ Enhanced prompts are more detailed")
        else:
            print("   ⚠️ Enhanced prompts should be longer than static ones")
        
    except Exception as e:
        print(f"❌ Monitoring failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def benchmark_database_queries():
    """Benchmark database query performance"""
    db = SessionLocal()
    
    try:
        print("🚀 Database Query Benchmark\n")
        
        from app.services.thema_service import ThemaService
        thema_service = ThemaService(db)
        
        # Test different query patterns
        test_cases = [
            ("get_thema_by_name", lambda: thema_service.get_thema_by_name("verjaardag")),
            ("generate_thema_data", lambda: thema_service.generate_thema_data(thema_id=4)),
            ("get_random_elements", lambda: thema_service.get_random_elements(4, 'keyword', count=5)),
            ("get_random_rhyme_set", lambda: thema_service.get_random_rhyme_set(4, 'AABB')),
        ]
        
        iterations = 100
        
        for test_name, test_func in test_cases:
            times = []
            
            for _ in range(iterations):
                start_time = time.time()
                test_func()
                times.append(time.time() - start_time)
            
            avg_time = statistics.mean(times) * 1000
            min_time = min(times) * 1000
            max_time = max(times) * 1000
            
            print(f"{test_name:20}: {avg_time:.2f}ms avg (min: {min_time:.2f}ms, max: {max_time:.2f}ms)")
        
        print(f"\n✅ Database queries are {'fast' if avg_time < 10 else 'acceptable' if avg_time < 50 else 'slow'}")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Monitor prompt generation performance')
    parser.add_argument('--sample-size', type=int, default=10, help='Number of orders to test')
    parser.add_argument('--benchmark', action='store_true', help='Run database query benchmark')
    
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark_database_queries()
    else:
        monitor_prompt_performance(args.sample_size) 