from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__)

# Stripe API Keys (Replace with your own)
STRIPE_PUBLIC_KEY = "pk_test_your_public_key"
STRIPE_SECRET_KEY = "sk_test_your_secret_key"

stripe.api_key = STRIPE_SECRET_KEY

# Sample cart (in a real app, you'd use a database)
cart = [
    {"name": "Speedster Longboard", "price": 799, "quantity": 1},
    {"name": "RC Racing Car", "price": 299, "quantity": 2}
]

@app.route("/")
def index():
    return render_template("checkout.html", cart=cart, public_key=STRIPE_PUBLIC_KEY)

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100),  # Convert to cents
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

@app.route("/success")
def success():
    return "<h1>Payment Successful! 🎉</h1>"

@app.route("/cancel")
def cancel():
    return "<h1>Payment Cancelled! ❌</h1>"

if __name__ == "__main__":
    app.run(debug=True)

