#!/usr/bin/env python3
"""
Fix JSON format to match website requirements
"""

import json
import pandas as pd
from datetime import datetime

def fix_json_format(input_json_path, output_json_path):
    """Fix JSON format to match website expectations"""
    
    print("🔄 Reading existing JSON...")
    
    # Read existing JSON
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Found {len(data)} transactions")
    
    # Convert to correct format
    fixed_transactions = []
    skipped = 0
    
    for idx, transaction in enumerate(data):
        try:
            # Fix date format
            date_str = transaction.get('Date', '')
            if date_str:
                # Convert to ISO format with Z
                date_obj = pd.to_datetime(date_str)
                iso_date = date_obj.isoformat() + 'Z'
            else:
                skipped += 1
                continue
            
            # Fix amount (string to number)
            amount_str = str(transaction.get('amount', '0')).replace(',', '').replace('"', '')
            amount = float(amount_str)
            
            # Fix category mapping
            type_val = transaction.get('type', '').upper()
            if type_val == 'EXPENSE':
                category = 'Expense'
            elif type_val == 'INCOME':
                category = 'Revenue'
            else:
                category = 'Expense'  # Default
            
            # Create fixed transaction
            fixed_transaction = {
                'date': iso_date,  # Fixed field name
                'amount': amount,  # Fixed data type
                'category': category,  # Fixed mapping
                'status': 'Paid',  # Added required field
                'description': transaction.get('title', ''),
                'account': transaction.get('account', ''),
                'subcategory': transaction.get('category', ''),
                'id': transaction.get('id', f'fixed_{idx}')
            }
            
            # Remove empty fields
            fixed_transaction = {k: v for k, v in fixed_transaction.items() 
                               if v not in ['', 'nan', None, 'null']}
            
            fixed_transactions.append(fixed_transaction)
            
        except Exception as e:
            print(f"⚠️ Error fixing transaction {idx}: {e}")
            skipped += 1
            continue
    
    # Save fixed JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_transactions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ JSON Fixed Successfully!")
    print(f"📊 Fixed: {len(fixed_transactions)} transactions")
    print(f"⚠️ Skipped: {skipped} invalid transactions")
    print(f"📁 Saved to: {output_json_path}")
    
    # Show statistics
    expense_count = sum(1 for t in fixed_transactions if t['category'] == 'Expense')
    revenue_count = sum(1 for t in fixed_transactions if t['category'] == 'Revenue')
    total_expense = sum(t['amount'] for t in fixed_transactions if t['category'] == 'Expense')
    total_revenue = sum(t['amount'] for t in fixed_transactions if t['category'] == 'Revenue')
    
    print(f"\n📈 Statistics:")
    print(f"💰 Expenses: {expense_count} transactions, ₹{total_expense:.2f}")
    print(f"💵 Revenue: {revenue_count} transactions, ₹{total_revenue:.2f}")
    
    return fixed_transactions

def show_changes():
    """Show what changes were made"""
    print("\n🔧 CHANGES MADE:")
    print("=" * 50)
    print("❌ OLD FORMAT → ✅ NEW FORMAT")
    print("=" * 50)
    print('"Date": "2024-08-11..." → "date": "2024-08-11T...Z"')
    print('"amount": "45.00" → "amount": 45.00')
    print('"type": "EXPENSE" → "category": "Expense"')
    print('"type": "INCOME" → "category": "Revenue"')
    print('[missing] → "status": "Paid"')
    print('"category": "Bills" → "subcategory": "Bills"')
    print('Removed: transfer-*, receive-*, due-date, currency')
    print("=" * 50)

if __name__ == "__main__":
    show_changes()
    
    # Fix your JSON file
    input_file = '/Users/kushal/Downloads/Major_project-main/Accurcy/expenses_income_summary.json'
    output_file = '/Users/kushal/Downloads/Major_project-main/Accurcy/website_ready_transactions.json'
    
    fixed_transactions = fix_json_format(input_file, output_file)
    
    # Show sample
    print("\n📊 Sample fixed transaction:")
    if fixed_transactions:
        print(json.dumps(fixed_transactions[0], indent=2))
        
    print(f"\n🚀 Ready for website upload!")
    print(f"📁 Upload this file: {output_file}")
