# Customer Management System — Document Data Model Demo

A Python command-line application that stores customer data using **MongoDB (document model)** and **SQLite (relational model)** to demonstrate the advantages described in the MongoDB white paper *"Why the Document Data Model"*.

---

## Requirements

- Python 3.9 or newer
- A free **MongoDB Atlas** account with an M0 cluster
- Internet connection

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the connection string:**
   Open `config.py` and replace the placeholder with your MongoDB Atlas connection string:
   ```python
   MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   ```

3. **Test the connection:**
   ```bash
   python db.py
   ```
   You should see: `Connected to MongoDB Atlas successfully!`

## How to Run

```bash
python main.py
```

## Menu Options

| Option | Description | Paper Concept |
|--------|-------------|---------------|
| 1 | Insert the sample customer from the paper | Intuitive data model |
| 2 | View all customers | CRUD — Read |
| 3 | Add a new customer | CRUD — Create |
| 4 | Find customers by city | Nested document queries |
| 5 | Add a phone number to a customer | Fine-grained array update (`$push`) |
| 6 | Delete a customer | CRUD — Delete |
| 7 | Flexible schema demo | Polymorphic documents |
| 8 | Schema validation demo | JSON Schema governance |
| 9 | Query and aggregation demo | Powerful queries & aggregation pipeline |
| 10 | Indexing performance demo | Index speed-up comparison |
| 11 | ACID transaction demo | Multi-document transactions |
| 12 | SQL (SQLite) comparison | Object-relational impedance mismatch |

## Project Structure

```
2_Code/
├── config.py          # MongoDB Atlas connection string
├── db.py              # Database connection and test
├── mongo_demo.py      # All MongoDB demonstrations
├── sql_demo.py        # SQLite relational comparison
├── main.py            # Interactive menu
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Security Note

Before submitting, replace your real password in `config.py` with a placeholder like `<password>`.

## References

- *Why the Document Data Model* — MongoDB White Paper (2020)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
