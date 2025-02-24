from flask import Flask, render_template, request, jsonify
import stripe

# 🔹 Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# 🔹 Stripe API Keys (Replace with your own test keys from Stripe Dashboard)
STRIPE_PUBLIC_KEY = "pk_test_your_public_key"
STRIPE_SECRET_KEY = "sk_test_your_secret_key"

stripe.api_key = STRIPE_SECRET_KEY

# 🔹 Sample cart (Replace with a database in production)
cart = [
    {"name": "Speedster Longboard", "price": 799, "quantity": 1},
    {"name": "RC Racing Car", "price": 299, "quantity": 2}
]

@app.route("/")
def index():
    total_price = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("checkout.html", cart=cart, total_price=total_price, public_key=STRIPE_PUBLIC_KEY)

@app.route("/checkout")
def checkout():
    total_price = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("checkout.html", cart=cart, total_price=total_price, public_key=STRIPE_PUBLIC_KEY)

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        print("Received checkout request!")  # Debug log
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100),  # Convert price to cents
                    },
                    "quantity": item["quantity"],
                }
                for item in cart
            ],
            mode="payment",
            success_url="http://127.0.0.1:5000/success",
            cancel_url="http://127.0.0.1:5000/cancel",
        )
        print("Stripe session created:", session.url)  # Debug log
        return jsonify({"url": session.url})
    except Exception as e:
        print("Error:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 400

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

if __name__ == "__main__":
    app.run(debug=True)
