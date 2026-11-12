# Ward Supplies

An ordering site where hospital wards order medical supplies, running on Cloud Run. All data is fictional.

## What's in here

| Path | What it is |
|---|---|
| `main.py` | Flask app: ordering page, product API, orders, spend report, admin endpoints |
| `templates/index.html` | The ordering page |
| `static/cart.js` | Client-side order basket |
| `data/products.json` | Product catalog |
| `Dockerfile` | Container image used by Cloud Run |

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Ordering page |
| GET | `/health` | Health check |
| GET | `/api/products` | Product catalog |
| POST | `/api/orders` | Place an order: `{"items": [{"id": "...", "quantity": 1}]}` |
| GET | `/api/reports/spend` | Spend per category over the last year |
| GET | `/admin/orders` | All orders (admin only) |

## How it runs

- Cloud Run service `ward-supplies`, region `europe-west4`.
- Runs as the service account `app-runtime@<project>.iam.gserviceaccount.com`.
- The supplier's API key comes from Secret Manager (`supplier-api-key`).

## Run it locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
SUPPLIERS_API_KEY=local-test python main.py
```
