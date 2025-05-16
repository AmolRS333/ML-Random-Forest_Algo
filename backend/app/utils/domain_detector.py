from typing import List, Dict
import re

# Domain-specific keywords
DOMAIN_KEYWORDS = {
    'healthcare': [
        'patient', 'diagnosis', 'treatment', 'disease', 'symptom', 'medical',
        'health', 'hospital', 'doctor', 'blood', 'pressure', 'heart', 'cancer',
        'diabetes', 'bmi', 'age', 'gender', 'weight', 'height'
    ],
    'finance': [
        'price', 'cost', 'revenue', 'profit', 'loss', 'income', 'expense',
        'balance', 'account', 'transaction', 'stock', 'market', 'investment',
        'interest', 'rate', 'loan', 'credit', 'debit', 'bank'
    ],
    'education': [
        'student', 'grade', 'score', 'exam', 'test', 'course', 'class',
        'school', 'university', 'college', 'education', 'learning', 'study',
        'attendance', 'performance', 'teacher', 'subject'
    ],
    'retail': [
        'product', 'customer', 'sale', 'purchase', 'order', 'item', 'price',
        'quantity', 'store', 'shop', 'retail', 'inventory', 'stock', 'discount',
        'category', 'brand'
    ]
}

def detect_domain(columns: List[str]) -> str:
    """
    Detect the domain of the dataset based on column names.
    Returns the most likely domain or 'unknown' if no clear match.
    """
    # Convert all column names to lowercase for matching
    columns_lower = [col.lower() for col in columns]
    
    # Count matches for each domain
    domain_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for keyword in keywords if any(keyword in col for col in columns_lower))
        domain_scores[domain] = score
    
    # Find domain with highest score
    max_score = max(domain_scores.values())
    if max_score == 0:
        return 'unknown'
    
    # Return domain with highest score
    return max(domain_scores.items(), key=lambda x: x[1])[0] 