from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__)

# ✅ Replace these with your real Stripe API keys
STRIPE_PUBLIC_KEY = "pk_test_51Qw2JTPGYbHY59lZ6xogTD8Vp3RKM0X88qX150uxNEMpF41xfRIcXs0D46WBmU45QQUihbYuLmuxDNneAymRGzE700aD9EfLmn"
STRIPE_SECRET_KEY = "sk_test_51Qw2JTPGYbHY59lZmJjtc5OIKNQ4C9fsq242G47622r1VFauVsBVZ81T90MGesIZFzsK9BUXJcI5YmJnI826xpPe00cTRRuKTh"
stripe.api_key = STRIPE_SECRET_KEY

# 🏠 Serve the homepage
@app.route("/")
def index():
    return render_template("index.html")

# 🛒 Serve the cart page
@app.route("/cart")
def cart():
    return render_template("cart.html")

# 💳 Serve the checkout page
@app.route("/checkout")
def checkout():
    cart = [
        {"name": "Speedster Longboard", "price": 799, "quantity": 1},
        {"name": "RC Racing Car", "price": 299, "quantity": 2}
    ]
    total_price = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("checkout.html", cart=cart, total_price=total_price, public_key=STRIPE_PUBLIC_KEY)

# ✅ Stripe Checkout Session
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        cart = [
            {"name": "Speedster Longboard", "price": 799, "quantity": 1},
            {"name": "RC Racing Car", "price": 299, "quantity": 2}
        ]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100),
                    },
                    "quantity": item["quantity"],
                }
                for item in cart
            ],
            mode="payment",
            success_url="http://127.0.0.1:5000/success",
            cancel_url="http://127.0.0.1:5000/cancel",
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Start Flask on a specific port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
