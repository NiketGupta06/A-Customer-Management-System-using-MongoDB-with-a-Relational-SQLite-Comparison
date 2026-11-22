import time
import random
from pymongo import ASCENDING
from pymongo.errors import PyMongoError
from db import client, db

# ---------- Sample document from the paper (page 5) ----------
SAMPLE_CUSTOMER = {
    "customerID": 12345,
    "name": {"first": "John", "last": "Doe"},
    "address": [
        {
            "location": "work",
            "address": {"street": "16 Hatfields", "city": "London", "postal_code": "SE1 8DJ"},
            "country": "United Kingdom",
            "geo": {"type": "Point", "coord": [51.5065752, -0.109081]},
        }
    ],
    "email": "john.doe@acme.com",
    "phone": [{"location": "work", "number": "+44-1234567890"}],
    "dob": "1977-04-01T05:00:00Z",
    "interests": ["devops", "data science"],
    "annualSpend": 1292815.75,
}

def insert_sample():
    db.customers.delete_many({"customerID": 12345})
    result = db.customers.insert_one(dict(SAMPLE_CUSTOMER))
    print("Inserted sample customer with _id:", result.inserted_id)

# ---------- CREATE ----------
def add_customer(customer_id, first, last, email, city, spend):
    doc = {
        "customerID": customer_id,
        "name": {"first": first, "last": last},
        "email": email,
        "address": [{"location": "home", "address": {"city": city}}],
        "annualSpend": spend,
    }
    db.customers.insert_one(doc)
    print("Customer added.")

# ---------- READ ----------
def view_customers(limit=10):
    for c in db.customers.find().limit(limit):
        print(c)

def find_by_city(city):
    # Query a field nested inside an array of subdocuments
    for c in db.customers.find({"address.address.city": city}):
        print(c["name"], "-", c.get("email"))

# ---------- UPDATE ----------
def add_phone(customer_id, number):
    # Adds one element to an array without rewriting the whole document
    db.customers.update_one(
        {"customerID": customer_id},
        {"$push": {"phone": {"location": "mobile", "number": number}}},
    )
    print("Phone number added.")

def update_spend(customer_id, new_spend):
    db.customers.update_one({"customerID": customer_id}, {"$set": {"annualSpend": new_spend}})

# ---------- DELETE ----------
def delete_customer(customer_id):
    result = db.customers.delete_one({"customerID": customer_id})
    print("Deleted:", result.deleted_count)

# ---------- FLEXIBLE SCHEMA ----------
def flexible_schema_demo():
    db.flex_demo.drop()
    db.flex_demo.insert_many([
        {"customerID": 1, "name": "Asha", "email": "asha@mail.com"},
        {"customerID": 2, "name": "Ravi", "email": "ravi@mail.com",
         "twitter_handle": "@ravi_dev"},                      # extra field
        {"customerID": 3, "name": "Meera", "email": "meera@mail.com",
         "interests": ["music", "travel"],                    # different extra fields
         "loyalty": {"tier": "gold", "points": 1200}},
    ])
    print("Three customers with three different structures, stored in ONE collection:")
    for d in db.flex_demo.find({}, {"_id": 0}):
        print(d)

# ---------- SCHEMA VALIDATION ----------
def create_validated_collection():
    db.validated_customers.drop()
    db.create_collection(
        "validated_customers",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["customerID", "name", "email"],
                "properties": {
                    "customerID": {"bsonType": "int"},
                    "name": {"bsonType": "string"},
                    "email": {"bsonType": "string", "pattern": "^.+@.+\\..+$"},
                    "annualSpend": {"bsonType": ["double", "int"], "minimum": 0},
                },
            }
        },
        validationAction="error",
    )
    print("Collection with validation rules created.")

def validation_demo():
    create_validated_collection()
    good = {"customerID": 1, "name": "Asha", "email": "asha@mail.com", "annualSpend": 500.0}
    bad = {"customerID": 2, "name": "Ravi"}   # missing required email

    for label, doc in [("VALID", good), ("INVALID", bad)]:
        try:
            db.validated_customers.insert_one(doc)
            print(f"{label} document -> accepted")
        except PyMongoError as e:
            print(f"{label} document -> REJECTED by schema validation")

# ---------- QUERIES & AGGREGATION ----------
def query_demo():
    print("\n1) Customers with annual spend > 1,000,000:")
    for c in db.customers.find({"annualSpend": {"$gt": 1000000}}, {"name": 1, "annualSpend": 1, "_id": 0}):
        print(c)

    print("\n2) Customers interested in 'devops':")
    for c in db.customers.find({"interests": "devops"}, {"name": 1, "_id": 0}):
        print(c)

def aggregation_demo():
    # Count customers by city and compute min / max / average spend
    pipeline = [
        {"$unwind": "$address"},
        {"$group": {
            "_id": "$address.address.city",
            "customers": {"$sum": 1},
            "avg_spend": {"$avg": "$annualSpend"},
            "min_spend": {"$min": "$annualSpend"},
            "max_spend": {"$max": "$annualSpend"},
        }},
        {"$sort": {"customers": -1}},
    ]
    print("\nCustomers by city (aggregation pipeline):")
    for row in db.customers.aggregate(pipeline):
        print(row)

# ---------- INDEXING PERFORMANCE ----------
CITIES = ["London", "Delhi", "Mumbai", "Paris", "Berlin", "Tokyo", "Sydney", "Toronto"]

def load_big_data(n=100000):
    db.big_customers.drop()
    batch = []
    for i in range(n):
        batch.append({
            "customerID": i,
            "name": f"User{i}",
            "email": f"user{i}@mail.com",
            "city": random.choice(CITIES),
            "annualSpend": round(random.uniform(100, 100000), 2),
        })
        if len(batch) == 5000:
            db.big_customers.insert_many(batch)
            batch = []
    if batch:
        db.big_customers.insert_many(batch)
    print(f"Inserted {n} customers.")

def time_query():
    start = time.perf_counter()
    result = db.big_customers.find_one({"email": "user49999@mail.com"})
    return (time.perf_counter() - start) * 1000   # milliseconds

def index_demo():
    if db.big_customers.count_documents({}) == 0:
        load_big_data(100000)
    db.big_customers.drop_indexes()

    t1 = min(time_query() for _ in range(5))
    print(f"Without index (total time incl. network): {t1:.2f} ms")
    explain_query("WITHOUT index:")

    db.big_customers.create_index([("email", ASCENDING)])

    t2 = min(time_query() for _ in range(5))
    print(f"\nWith index (total time incl. network): {t2:.2f} ms")
    explain_query("WITH index:")
    print(f"\nSpeed-up (total time): about {t1 / t2:.1f}x faster")

# ---------- ACID TRANSACTIONS ----------
def setup_stock():
    db.stock.drop()
    db.orders.drop()
    db.stock.insert_one({"item": "laptop", "quantity": 5})
    print("Stock created: laptop = 5")

def place_order(item, qty, customer_id):
    with client.start_session() as session:
        try:
            with session.start_transaction():
                result = db.stock.update_one(
                    {"item": item, "quantity": {"$gte": qty}},
                    {"$inc": {"quantity": -qty}},
                    session=session,
                )
                if result.modified_count == 0:
                    raise ValueError("Not enough stock")
                db.orders.insert_one(
                    {"customerID": customer_id, "item": item, "qty": qty},
                    session=session,
                )
            print(f"Order placed: {qty} x {item}")
        except Exception as e:
            print("Transaction ABORTED, nothing was changed:", e)

def transaction_demo():
    setup_stock()
    place_order("laptop", 2, 12345)    # succeeds
    place_order("laptop", 10, 12345)   # fails, rolled back
    print("Final stock:", db.stock.find_one({}, {"_id": 0}))
    print("Orders     :", list(db.orders.find({}, {"_id": 0})))

def _find_stage(plan, target):
    """Search the explain plan for a stage whose name contains the target text."""
    if isinstance(plan, dict):
        stage = plan.get("stage")
        if isinstance(stage, str) and target in stage:
            return True
        return any(_find_stage(v, target) for v in plan.values())
    if isinstance(plan, list):
        return any(_find_stage(v, target) for v in plan)
    return False

def explain_query(label):
    query = {"email": "user99999@mail.com"}
    info = db.big_customers.find(query).limit(1).explain()
    stats = info["executionStats"]
    plan = info["queryPlanner"]["winningPlan"]
    scan = "IXSCAN (index)" if _find_stage(plan, "IXSCAN") else "COLLSCAN (full scan)"
    print(f"{label}")
    print(f"   Plan used          : {scan}")
    print(f"   Documents examined : {stats['totalDocsExamined']}")
    print(f"   Server time        : {stats['executionTimeMillis']} ms")