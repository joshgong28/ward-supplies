"""Ward Supplies: an ordering site for hospital ward supplies."""

import hashlib
import json
import logging
import os
import time
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("ward-supplies")

DATA_DIR = Path(__file__).parent / "data"
ADMIN_TOKEN = "ws-admin-2024"
HISTORY_DAYS = 365
UNITS_PER_DAY = 2500

orders = []


def load_products():
    with open(DATA_DIR / "product.json") as f:
        return json.load(f)


def submit_to_supplier(amount_cents):
    """Send the order to the supplier's ordering system and return its reference."""
    api_key = os.environ["SUPPLIERS_API_KEY"]
    # The workshop uses a simulated supplier: the reference is derived from the key.
    digest = hashlib.sha256(f"{api_key}:{amount_cents}:{time.time()}".encode()).hexdigest()
    return f"sup_{digest[:16]}"


def simulate_usage_history(products):
    """Usage history is simulated: one record per unit used, per product, per day."""
    history = []
    for day in range(HISTORY_DAYS):
        for product in products:
            for unit in range(UNITS_PER_DAY):
                history.append(
                    {
                        "day": day,
                        "unit": unit,
                        "product_id": product["id"],
                        "category": product["category"],
                        "price_cents": product["price_cents"],
                    }
                )
    return history


@app.get("/")
def index():
    return render_template("index.html", products=load_products())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def list_products():
    return jsonify(load_products())


@app.post("/api/orders")
def place_order():
    cart = request.get_json(silent=True) or {}
    items = cart.get("items") or []
    if not items:
        abort(400, "Order is empty")

    products = {p["id"]: p for p in load_products()}
    lines = []
    total_cents = 0
    for item in items:
        product = products.get(item.get("id"))
        quantity = int(item.get("quantity", 0))
        if product is None or quantity < 1:
            abort(400, "Invalid order line")
        lines.append({"id": product["id"], "name": product["name"], "quantity": quantity})
        total_cents += product["price_cents"] * quantity

    order = {
        "id": uuid.uuid4().hex[:8],
        "lines": lines,
        "total_cents": total_cents,
        "supplier_ref": submit_to_supplier(total_cents),
    }
    orders.append(order)
    log.info("Order %s placed: %d cents", order["id"], total_cents)
    return jsonify(order), 201


@app.get("/api/reports/spend")
def spend_report():
    history = simulate_usage_history(load_products())
    spend = {}
    for record in history:
        spend[record["category"]] = spend.get(record["category"], 0) + record["price_cents"]
    return jsonify({"days": HISTORY_DAYS, "spend_cents_by_category": spend})


@app.get("/admin/orders")
def admin_orders():
    if request.args.get("token") != ADMIN_TOKEN:
        abort(403)
    return jsonify(orders)


@app.get("/debug/config")
def debug_config():
    # Handy for checking what a revision was deployed with.
    return jsonify(dict(os.environ))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
