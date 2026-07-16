"""
Script to add beauty products and tags to all products.
Run with: python manage.py shell < scripts/add_beauty_products.py
"""
import os, sys, django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product, ProductVariant

# ----------------------------
# 1. Add tags to existing products
# ----------------------------
existing_tags = {
    'Shoes': 'Trending, Premium Quality',
    'Clothing': 'Streetwear, Latest Collection',
    'Electronics': 'Best Seller, Fast Charging',
    'Accessories': 'Handcrafted, Unisex',
}

for product in Product.objects.all():
    category = product.category
    if category in existing_tags and not product.tags:
        product.tags = existing_tags[category]
        product.save()
        print(f"  Tagged: {product.name} -> {product.tags}")

print(f"\nExisting products tagged.\n")

# ----------------------------
# 2. Add Beauty Products
# ----------------------------
beauty_products = [
    {
        'name': 'Rose Gold Eyeshadow Palette',
        'description': 'A luxurious 12-shade eyeshadow palette featuring warm rose gold tones, from subtle mattes to dazzling shimmers. Highly pigmented, blendable formula that lasts all day. Perfect for everyday glam or bold evening looks.',
        'price': 1299.00,
        'category': 'Beauty',
        'tags': '12 Shades, Longwear Makeup, Cruelty Free',
        'variants': [
            {'size': 'Standard', 'color': 'Rose Gold', 'stock': 30},
        ],
    },
    {
        'name': 'Hydrating Lip Gloss Set',
        'description': 'A set of 6 hydrating lip glosses in nude to berry shades. Infused with vitamin E and hyaluronic acid for plump, moisturized lips. Non-sticky, mirror-shine finish with a subtle vanilla scent.',
        'price': 899.00,
        'category': 'Beauty',
        'tags': '6-in-1 Combo, Vitamin E Infused, Non-Sticky',
        'variants': [
            {'size': 'Set of 6', 'color': 'Nude', 'stock': 40},
            {'size': 'Set of 6', 'color': 'Berry', 'stock': 35},
        ],
    },
    {
        'name': 'Matte Foundation SPF 30',
        'description': 'A full-coverage matte foundation with SPF 30 sun protection. Lightweight, breathable formula that controls oil and blurs pores. Buildable coverage from medium to full. Available in 8 inclusive shades.',
        'price': 1599.00,
        'category': 'Beauty',
        'tags': 'SPF 30, Full Coverage, Oil Control',
        'variants': [
            {'size': '30ml', 'color': 'Ivory', 'stock': 25},
            {'size': '30ml', 'color': 'Beige', 'stock': 25},
            {'size': '30ml', 'color': 'Honey', 'stock': 20},
            {'size': '30ml', 'color': 'Mocha', 'stock': 20},
        ],
    },
    {
        'name': 'Vitamin C Brightening Serum',
        'description': 'A potent 20% Vitamin C serum with hyaluronic acid and niacinamide. Brightens dull skin, fades dark spots, and boosts collagen production. Dermatologist-tested, suitable for all skin types.',
        'price': 1199.00,
        'category': 'Beauty',
        'tags': 'Dermatologist Tested, Brightening, Anti-Aging',
        'variants': [
            {'size': '30ml', 'color': '', 'stock': 50},
            {'size': '50ml', 'color': '', 'stock': 30},
        ],
    },
    {
        'name': 'Velvet Matte Lipstick Collection',
        'description': 'A premium set of 4 velvet matte lipsticks in universally flattering shades — from classic reds to deep plums. Creamy, hydrating formula that glides on smoothly and stays put for 12+ hours.',
        'price': 1499.00,
        'category': 'Beauty',
        'tags': 'Longwear Makeup, 4-in-1 Set, 12hr Stay',
        'variants': [
            {'size': 'Set of 4', 'color': 'Red', 'stock': 35},
            {'size': 'Set of 4', 'color': 'Plum', 'stock': 30},
        ],
    },
    {
        'name': 'Charcoal Detox Face Mask',
        'description': 'An activated charcoal peel-off mask that deeply cleanses pores, removes blackheads, and detoxifies skin. Enriched with tea tree oil and aloe vera for a refreshed, smooth complexion. Use 2-3 times per week.',
        'price': 599.00,
        'category': 'Beauty',
        'tags': 'Pore Cleansing, Natural Ingredients, Detox',
        'variants': [
            {'size': '100ml', 'color': '', 'stock': 60},
            {'size': '200ml', 'color': '', 'stock': 40},
        ],
    },
]

for product_data in beauty_products:
    variants_data = product_data.pop('variants')
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults=product_data
    )
    if created:
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        print(f"  Created: {product.name} (tags: {product.tags})")
    else:
        print(f"  Skipped (exists): {product.name}")

print(f"\nDone! Beauty products added.")
print(f"Total products: {Product.objects.count()}")
print(f"Categories: {list(Product.objects.values_list('category', flat=True).distinct())}")
