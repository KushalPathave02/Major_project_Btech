# 🔍 System Analysis: CSV to JSON Conversion Issues

## 📊 **Current CSV Structure:**
```csv
vnfjDate,title,category,account,amount,currency,type,transfer-amount,transfer-currency,to-account,receive-amount,receive-currency,description,due-date,id
```

## 🎯 **Website Expected JSON Structure:**
```json
{
  "date": "2024-01-15T08:34:12Z",
  "amount": 1500.00,
  "category": "Revenue/Expense",
  "status": "Paid"
}
```

## ❌ **CRITICAL ISSUES:**

### 1. **Column Name Mismatch:**
- CSV: `vnfjDate` ❌ (corrupted)
- Expected: `Date` ✅
- **Fix**: Change `vnfjDate` → `Date`

### 2. **Field Mapping Issues:**
- CSV `type` (EXPENSE/INCOME) → Website `category` (Expense/Revenue)
- CSV `category` (Bills & Fees) → Website `subcategory`

### 3. **Missing Required Fields:**
- Website needs `status` field (not in CSV)
- Website expects ISO date format with 'Z'

## 🗑️ **UNUSED PARAMETERS (Can Remove):**
- `transfer-amount` (empty)
- `transfer-currency` (empty) 
- `to-account` (empty)
- `receive-amount` (empty)
- `receive-currency` (empty)
- `due-date` (empty)
- `currency` (always INR)

## ✅ **USEFUL PARAMETERS (Keep):**
- `Date` (fix name)
- `amount` 
- `type` (map to category)
- `title` (use as description)
- `category` (use as subcategory)
- `account`
- `id`

## 🛠️ **REQUIRED CHANGES:**

### A. **CSV File Changes:**
1. Fix header: `vnfjDate` → `Date`

### B. **Converter Script Changes:**
1. Handle corrupted date column
2. Add status field (default "Paid")
3. Map fields correctly
4. Remove unused parameters

### C. **Website Backend Changes:**
1. Update field mapping in `transactions.py`
2. Handle CSV format in upload route
3. Update forecast model field references

## 📝 **DETAILED MAPPING:**
```
CSV Field          → Website Field
vnfjDate           → date (fix + format)
amount             → amount (clean commas)
type               → category (EXPENSE→Expense, INCOME→Revenue)
title              → description
category           → subcategory
account            → account
id                 → id
[missing]          → status ("Paid")
```
