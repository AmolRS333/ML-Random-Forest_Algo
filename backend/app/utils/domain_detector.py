from typing import List, Dict  # Domain detection utility for datasets
#         """Generate confusion matrix plot for classification problems."""
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
    ],
    'agriculture': [
        'crop', 'yield', 'soil', 'temperature', 'rainfall', 'fertilizer',
        'farm', 'harvest', 'plant', 'agriculture', 'pesticide', 'irrigation',
        'humidity', 'moisture', 'climate'
    ],
    'transportation': [
        'vehicle', 'speed', 'traffic', 'route', 'distance', 'fuel', 'driver',
        'trip', 'accident', 'transport', 'road', 'logistics', 'shipment', 'travel'
    ],
    'environment': [
        'pollution', 'air', 'water', 'emission', 'carbon', 'climate', 'temperature',
        'weather', 'ozone', 'recycle', 'waste', 'green', 'energy', 'ecology'
    ],
    'sports': [
        'match', 'team', 'player', 'score', 'goal', 'tournament', 'win', 'lose',
        'stadium', 'coach', 'league', 'game', 'athlete', 'performance'
    ],
    'ecommerce': [
        'user', 'cart', 'checkout', 'payment', 'wishlist', 'delivery', 'return',
        'review', 'rating', 'browse', 'recommendation', 'seller', 'shipping'
    ],
    'real_estate': [
        'property', 'house', 'apartment', 'rent', 'buy', 'sell', 'price', 'location',
        'area', 'bedroom', 'bathroom', 'agent', 'mortgage', 'listing'
    ],
    'employment': [
        'job', 'employee', 'employer', 'salary', 'position', 'department',
        'resume', 'interview', 'hiring', 'contract', 'benefits', 'experience'
    ],
    'energy': [
        'electricity', 'power', 'solar', 'wind', 'generation', 'consumption',
        'renewable', 'grid', 'voltage', 'current', 'energy', 'unit', 'supply'
    ],
    'technology': [
        'device', 'software', 'hardware', 'update', 'bug', 'version', 'release',
        'system', 'application', 'performance', 'technology', 'tool', 'network'
    ],
    'tourism': [
        'destination', 'tourist', 'package', 'hotel', 'travel', 'flight', 'booking',
        'sightseeing', 'guide', 'trip', 'location', 'visa', 'itinerary'
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