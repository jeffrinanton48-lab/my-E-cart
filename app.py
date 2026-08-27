from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(
    __name__,
    static_folder="statics",
    template_folder="templates"
)

app.secret_key = "cartnova-secret-key"


PRODUCTS = {
    "Smartphone": 19999,
    "Laptop": 49999,
    "Headphones": 2499,
    "Smart Watch": 3999
}


@app.route("/")
def home():
    cart = session.get("cart", [])
    cart_count = len(cart)

    return render_template(
        "index.html",
        cart_count=cart_count
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@cartnova.com" and password == "123456":
            session["user"] = email
            return redirect(url_for("home"))

        return "Invalid email or password"

    return render_template("login.html")

@app.route("/add-to-cart/<product>")
def add_to_cart(product):
    cart = session.get("cart", [])

    cart.append(product)

    session["cart"] = cart

    return redirect(url_for("home"))


@app.route("/remove-from-cart/<product>")
def remove_from_cart(product):
    cart = session.get("cart", [])

    if product in cart:
        cart.remove(product)

    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart = session.get("cart", [])

    cart_items = []

    for product in cart:
        cart_items.append({
            "name": product,
            "price": PRODUCTS.get(product, 0)
        })

    total = sum(item["price"] for item in cart_items)

    return render_template(
        "cart.html",
        cart=cart_items,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True)