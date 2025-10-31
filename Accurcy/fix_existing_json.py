#!/usr/bin/env python3
"""
Fix existing expenses_income_summary.json for website compatibility
"""

import json
import pandas as pd

def fix_existing_json():
    """Fix the existing JSON file format"""
    
    input_file = '/Users/kushal/Downloads/Major_project-main/Accurcy/expenses_income_summary.json'
    output_file = '/Users/kushal/Downloads/Major_project-main/Accurcy/website_ready_transactions.json'
    
    print("🔄 Reading existing JSON file...")
    
    # Read existing JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Found {len(data)} transactions")
    
    # Fix each transaction
    fixed_transactions = []
    skipped = 0
    
    for idx, transaction in enumerate(data):
        try:
            # 1. Fix date format and field name
            date_str = transaction.get('Date', '')
            if date_str:
                # Convert to ISO format with T and Z
                date_obj = pd.to_datetime(date_str)
                iso_date = date_obj.isoformat() + 'Z'
            else:
                print(f"⚠️ Skipping transaction {idx}: No date")
                skipped += 1
                continue
            
            # 2. Fix amount (string to number)
            amount_str = str(transaction.get('amount', '0')).replace(',', '').replace('"', '')
            try:
                amount = float(amount_str)
            except:
                print(f"⚠️ Skipping transaction {idx}: Invalid amount")
                skipped += 1
                continue
            
            # 3. Fix category mapping
            type_val = transaction.get('type', '').upper()
            if type_val == 'EXPENSE':
                category = 'Expense'
            elif type_val == 'INCOME':
                category = 'Revenue'
            else:
                category = 'Expense'  # Default
            
            # 4. Create fixed transaction with correct structure
            fixed_transaction = {
                'date': iso_date,                                    # ✅ Fixed field name & format
                'amount': amount,                                    # ✅ Fixed data type
                'category': category,                               # ✅ Fixed mapping
                'status': 'Paid',                                  # ✅ Added required field
                'description': transaction.get('title', ''),       # ✅ Map title to description
                'account': transaction.get('account', ''),         # ✅ Keep account
                'subcategory': transaction.get('category', ''),    # ✅ Map category to subcategory
                'id': transaction.get('id', f'fixed_{idx}')        # ✅ Keep ID
            }
            
            # 5. Remove empty fields to keep JSON clean
            fixed_transaction = {k: v for k, v in fixed_transaction.items() 
                               if v not in ['', 'nan', None, 'null']}
            
            fixed_transactions.append(fixed_transaction)
            
        except Exception as e:
            print(f"⚠️ Error fixing transaction {idx}: {e}")
            skipped += 1
            continue
    
    # Save fixed JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_transactions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ JSON Fixed Successfully!")
    print(f"📊 Fixed: {len(fixed_transactions)} transactions")
    print(f"⚠️ Skipped: {skipped} invalid transactions")
    print(f"📁 Saved to: {output_file}")
    
    # Show statistics
    expense_count = sum(1 for t in fixed_transactions if t['category'] == 'Expense')
    revenue_count = sum(1 for t in fixed_transactions if t['category'] == 'Revenue')
    total_expense = sum(t['amount'] for t in fixed_transactions if t['category'] == 'Expense')
    total_revenue = sum(t['amount'] for t in fixed_transactions if t['category'] == 'Revenue')
    
    print(f"\n📈 Statistics:")
    print(f"💰 Expenses: {expense_count} transactions, ₹{total_expense:.2f}")
    print(f"💵 Revenue: {revenue_count} transactions, ₹{total_revenue:.2f}")
    
    # Show before/after comparison
    print(f"\n🔄 CHANGES MADE:")
    print("=" * 60)
    print("❌ BEFORE                    → ✅ AFTER")
    print("=" * 60)
    print('"Date": "2024-08-11..."     → "date": "2024-08-11T...Z"')
    print('"amount": "45.00"           → "amount": 45.00')
    print('"type": "EXPENSE"           → "category": "Expense"')
    print('"category": "Bills & Fees"  → "subcategory": "Bills & Fees"')
    print('"title": "Karthik"          → "description": "Karthik"')
    print('[missing]                   → "status": "Paid"')
    print('Removed: transfer-*, currency, description: null')
    print("=" * 60)
    
    return fixed_transactions

if __name__ == "__main__":
    fixed_transactions = fix_existing_json()
    
    # Show sample
    print("\n📊 Sample fixed transaction:")
    if fixed_transactions:
        print(json.dumps(fixed_transactions[0], indent=2))
        
    print(f"\n🚀 Ready for website upload!")
    print(f"📁 Upload file: website_ready_transactions.json")
