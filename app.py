from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'shopfinity_secret_key_2024'

# 50 Products Database
CATEGORIES = ["Electronics", "Fashion", "Home", "Sports", "Beauty"]

PRODUCTS = [
    # Electronics (1-10)
    {"id": 1, "name": "iPhone 15 Pro", "price": 999, "category": "Electronics", "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400", "description": "Latest Apple smartphone with A17 chip"},
    {"id": 2, "name": "Samsung Galaxy S24", "price": 849, "category": "Electronics", "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400", "description": "Premium Android smartphone"},
    {"id": 3, "name": "MacBook Pro 14\"", "price": 1999, "category": "Electronics", "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400", "description": "Powerful laptop for professionals"},
    {"id": 4, "name": "Sony WH-1000XM5", "price": 349, "category": "Electronics", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "description": "Premium noise-canceling headphones"},
    {"id": 5, "name": "iPad Air", "price": 599, "category": "Electronics", "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400", "description": "Versatile tablet for work and play"},
    {"id": 6, "name": "Apple Watch Series 9", "price": 399, "category": "Electronics", "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400", "description": "Advanced smartwatch with health features"},
    {"id": 7, "name": "Sony PlayStation 5", "price": 499, "category": "Electronics", "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400", "description": "Next-gen gaming console"},
    {"id": 8, "name": "Nintendo Switch OLED", "price": 349, "category": "Electronics", "image": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400", "description": "Portable gaming system"},
    {"id": 9, "name": "Canon EOS R6", "price": 2499, "category": "Electronics", "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400", "description": "Professional mirrorless camera"},
    {"id": 10, "name": "Bose SoundLink", "price": 129, "category": "Electronics", "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "description": "Portable Bluetooth speaker"},
    
    # Fashion (11-20)
    {"id": 11, "name": "Nike Air Max 90", "price": 130, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "description": "Classic sneakers with Air cushioning"},
    {"id": 12, "name": "Levi's 501 Jeans", "price": 89, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400", "description": "Original straight fit jeans"},
    {"id": 13, "name": "Ray-Ban Aviator", "price": 154, "category": "Fashion", "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400", "description": "Iconic sunglasses design"},
    {"id": 14, "name": "Gucci Belt", "price": 450, "category": "Fashion", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "description": "Luxury leather belt with GG buckle"},
    {"id": 15, "name": "Adidas Ultraboost", "price": 180, "category": "Fashion", "image": "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400", "description": "Premium running shoes"},
    {"id": 16, "name": "North Face Jacket", "price": 299, "category": "Fashion", "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "description": "Waterproof outdoor jacket"},
    {"id": 17, "name": "Cashmere Sweater", "price": 195, "category": "Fashion", "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400", "description": "Soft luxury sweater"},
    {"id": 18, "name": "Leather Handbag", "price": 320, "category": "Fashion", "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400", "description": "Elegant designer handbag"},
    {"id": 19, "name": "Silk Scarf", "price": 85, "category": "Fashion", "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400", "description": "Luxurious silk accessory"},
    {"id": 20, "name": "Wool Coat", "price": 450, "category": "Fashion", "image": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400", "description": "Classic winter overcoat"},
    
    # Home & Garden (21-30)
    {"id": 21, "name": "Dyson V15 Vacuum", "price": 749, "category": "Home", "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", "description": "Powerful cordless vacuum"},
    {"id": 22, "name": "KitchenAid Mixer", "price": 449, "category": "Home", "image": "https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?w=400", "description": "Professional stand mixer"},
    {"id": 23, "name": "Nespresso Machine", "price": 199, "category": "Home", "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400", "description": "Premium coffee maker"},
    {"id": 24, "name": "Le Creuset Dutch Oven", "price": 380, "category": "Home", "image": "https://images.unsplash.com/photo-1585442231657-6b0e73c86d7a?w=400", "description": "Cast iron cookware"},
    {"id": 25, "name": "Philips Hue Starter Kit", "price": 199, "category": "Home", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400", "description": "Smart lighting system"},
    {"id": 26, "name": "Roomba i7+", "price": 799, "category": "Home", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "description": "Self-emptying robot vacuum"},
    {"id": 27, "name": "Air Purifier", "price": 299, "category": "Home", "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400", "description": "HEPA air purifier"},
    {"id": 28, "name": "Memory Foam Pillow", "price": 79, "category": "Home", "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400", "description": "Ergonomic sleeping pillow"},
    {"id": 29, "name": "Instant Pot", "price": 119, "category": "Home", "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400", "description": "Multi-function pressure cooker"},
    {"id": 30, "name": "Plant Set (3 pcs)", "price": 65, "category": "Home", "image": "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=400", "description": "Indoor plant collection"},
    
    # Sports & Outdoors (31-40)
    {"id": 31, "name": "Yoga Mat Premium", "price": 68, "category": "Sports", "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400", "description": "Non-slip exercise mat"},
    {"id": 32, "name": "Dumbbell Set 50lb", "price": 199, "category": "Sports", "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400", "description": "Adjustable weight set"},
    {"id": 33, "name": "Camping Tent 4P", "price": 249, "category": "Sports", "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400", "description": "Waterproof family tent"},
    {"id": 34, "name": "Mountain Bike", "price": 899, "category": "Sports", "image": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=400", "description": "21-speed trail bike"},
    {"id": 35, "name": "Golf Club Set", "price": 599, "category": "Sports", "image": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=400", "description": "Complete beginner set"},
    {"id": 36, "name": "Tennis Racket Pro", "price": 189, "category": "Sports", "image": "https://images.unsplash.com/photo-1617083934555-ac7d4e7c6229?w=400", "description": "Professional grade racket"},
    {"id": 37, "name": "Running Watch", "price": 249, "category": "Sports", "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400", "description": "GPS fitness tracker"},
    {"id": 38, "name": "Kayak Single", "price": 549, "category": "Sports", "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400", "description": "Lightweight recreational kayak"},
    {"id": 39, "name": "Boxing Gloves", "price": 79, "category": "Sports", "image": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=400", "description": "Professional training gloves"},
    {"id": 40, "name": "Skateboard Pro", "price": 129, "category": "Sports", "image": "https://images.unsplash.com/photo-1547447134-cd3f5c716030?w=400", "description": "Complete pro skateboard"},
    
    # Beauty & Health (41-50)
    {"id": 41, "name": "Dyson Airwrap", "price": 599, "category": "Beauty", "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400", "description": "Multi-styler hair tool"},
    {"id": 42, "name": "La Mer Moisturizer", "price": 190, "category": "Beauty", "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400", "description": "Luxury face cream"},
    {"id": 43, "name": "Oral-B Electric", "price": 149, "category": "Beauty", "image": "https://images.unsplash.com/photo-1559591937-ecd93e55b013?w=400", "description": "Smart electric toothbrush"},
    {"id": 44, "name": "Perfume Gift Set", "price": 125, "category": "Beauty", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400", "description": "Designer fragrance collection"},
    {"id": 45, "name": "Skincare Kit", "price": 89, "category": "Beauty", "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400", "description": "Complete skincare routine"},
    {"id": 46, "name": "Massage Gun", "price": 199, "category": "Beauty", "image": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400", "description": "Deep tissue massager"},
    {"id": 47, "name": "Vitamin Set", "price": 59, "category": "Beauty", "image": "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=400", "description": "Daily wellness supplements"},
    {"id": 48, "name": "Hair Dryer Pro", "price": 299, "category": "Beauty", "image": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=400", "description": "Professional salon dryer"},
    {"id": 49, "name": "Makeup Palette", "price": 65, "category": "Beauty", "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400", "description": "18-shade eyeshadow palette"},
    {"id": 50, "name": "Essential Oils Set", "price": 45, "category": "Beauty", "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400", "description": "Aromatherapy collection"},
]

CATEGORIES = ["Electronics", "Fashion", "Home", "Sports", "Beauty"]

@app.route('/')
def home():
    featured = PRODUCTS[:8]
    return render_template('welcome.html', products=featured, categories=CATEGORIES)


@app.route('/product/<int:id>')
def product(id):
    product = next((p for p in PRODUCTS if p['id'] == id), None)
    if not product:
        return redirect(url_for('products'))
    return render_template('product.html', product=product, categories=CATEGORIES)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    items = []
    total = 0
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            items.append({**product, 'quantity': item['quantity']})
            total += product['price'] * item['quantity']
    return render_template('cart.html', items=items, total=total, categories=CATEGORIES)


@app.route('/remove-from-cart/<int:id>')
def remove_from_cart(id):
    cart = session.get('cart', [])
    cart = [i for i in cart if i['id'] != id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        return redirect(url_for('orderdetails'))

    cart_items = session.get('cart', [])
    items = []
    total = 0

    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            items.append({
                **product,
                'quantity': item['quantity']
            })
            total += product['price'] * item['quantity']

    return render_template(
        'checkout.html',
        items=items,
        total=total,
        categories=CATEGORIES
    )


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = [p for p in PRODUCTS if query in p['name'].lower() or query in p['description'].lower()]
    return render_template('products.html', products=results, categories=CATEGORIES, search=query)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # store user in session (basic demo)
        session['user'] = request.form['email']
        flash("Account created successfully!")
        return redirect(url_for('home'))

    return render_template('signup.html', categories=CATEGORIES)

@app.route('/cart/increase/<int:id>')
def cart_increase(id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == id:
            item['quantity'] += 1
            break
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart/decrease/<int:id>')
def cart_decrease(id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == id:
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                cart.remove(item)
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/add-to-cart/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', [])
    existing = next((i for i in cart if i['id'] == id), None)

    if existing:
        existing['quantity'] += 1
    else:
        cart.append({'id': id, 'quantity': 1})

    session['cart'] = cart
    flash("Added to cart!")

    # ALWAYS go back safely
    ref = request.headers.get("Referer")
    if ref:
        return redirect(ref)
    return redirect(url_for("products"))

@app.route('/products')
def products():
    return render_template('products.html', products=PRODUCTS, categories=CATEGORIES)

@app.route('/category/<category>')
def category(category):
    filtered = [p for p in PRODUCTS if p['category'] == category]
    return render_template(
        'category.html',
        products=filtered,
        category=category,
        categories=CATEGORIES
    )


@app.route('/thankyou')
def thankyou():
    import random
    order_id = random.randint(100000, 999999)
    
    return render_template(
        'thankyou.html',
        order_id=order_id,
        categories=CATEGORIES
    )

@app.route('/welcome')
def welcome():
    featured_products = PRODUCTS[:8]

    categories = [
        {
            "name": c,
            "slug": c.lower(),
            "image": f"https://via.placeholder.com/600x400?text={c}"
        }
        for c in CATEGORIES
    ]

    return render_template(
        'welcome.html',
        categories=categories,
        featured_products=featured_products
    )


    
@app.route('/orderdetails')
def orderdetails():
    cart_items = session.get('cart', [])
    items = []
    total = 0

    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            items.append({
                **product,
                'quantity': item['quantity']
            })
            total += product['price'] * item['quantity']

    import random
    order_id = random.randint(100000, 999999)

    # clear cart after order is confirmed
    session['cart'] = []

    return render_template(
        'orderdetails.html',
        items=items,
        total=total,
        order_id=order_id,
        categories=CATEGORIES
    )




if __name__ == '__main__':
    app.run(debug=True)
