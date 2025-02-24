from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks in the templates folder

# Stripe API Keys (Replace with your own test keys)
STRIPE_PUBLIC_KEY = "pk_test_your_public_key"
STRIPE_SECRET_KEY = "sk_test_your_secret_key"

stripe.api_key = STRIPE_SECRET_KEY

# Sample cart (for testing)
cart = [
    {"name": "Speedster Longboard", "price": 799, "quantity": 1},
    {"name": "RC Racing Car", "price": 299, "quantity": 2}
]

@app.route("/")
def index():
    return render_template("checkout.html", cart=cart, total_price=sum(item["price"] * item["quantity"] for item in cart), public_key=STRIPE_PUBLIC_KEY)

@app.route("/checkout")
def checkout():
    total_price = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("checkout.html", cart=cart, total_price=total_price, public_key=STRIPE_PUBLIC_KEY)

if __name__ == "__main__":
    app.run(debug=True)
