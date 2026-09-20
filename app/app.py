from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Métricas propias
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total de requests recibidos',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Latencia de los requests',
    ['endpoint']
)

PRODUCTS_CREATED = Counter(
    'products_created_total',
    'Total de productos creados'
)

# Base de datos en memoria
products = [
    {"id": 1, "name": "Laptop", "price": 1200.00, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 25.00, "stock": 50},
    {"id": 3, "name": "Teclado", "price": 45.00, "stock": 30},
]
next_id = 4

@app.route("/")
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    return jsonify({"message": "🚀 Products API funcionando!", "version": "1.0.0"})

@app.route("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status='200').inc()
    return jsonify({"status": "ok"}), 200

@app.route("/info")
def info():
    REQUEST_COUNT.labels(method='GET', endpoint='/info', status='200').inc()
    return jsonify({
        "app": "products-api",
        "version": "1.0.0",
        "author": "Edwin",
        "endpoints": ["/products", "/products/<id>", "/health", "/metrics"]
    }), 200

@app.route("/products", methods=["GET"])
def get_products():
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/products', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/products').observe(time.time() - start)
    return jsonify({"products": products, "total": len(products)}), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        REQUEST_COUNT.labels(method='GET', endpoint='/products/id', status='404').inc()
        return jsonify({"error": "Producto no encontrado"}), 404
    REQUEST_COUNT.labels(method='GET', endpoint='/products/id', status='200').inc()
    return jsonify(product), 200

@app.route("/products", methods=["POST"])
def create_product():
    global next_id
    data = request.get_json()
    if not data or not data.get("name") or not data.get("price"):
        REQUEST_COUNT.labels(method='POST', endpoint='/products', status='400').inc()
        return jsonify({"error": "name y price son requeridos"}), 400
    product = {
        "id": next_id,
        "name": data["name"],
        "price": data["price"],
        "stock": data.get("stock", 0)
    }
    products.append(product)
    next_id += 1
    PRODUCTS_CREATED.inc()
    REQUEST_COUNT.labels(method='POST', endpoint='/products', status='201').inc()
    return jsonify(product), 201

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        REQUEST_COUNT.labels(method='DELETE', endpoint='/products/id', status='404').inc()
        return jsonify({"error": "Producto no encontrado"}), 404
    products = [p for p in products if p["id"] != product_id]
    REQUEST_COUNT.labels(method='DELETE', endpoint='/products/id', status='200').inc()
    return jsonify({"message": "Producto eliminado"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
