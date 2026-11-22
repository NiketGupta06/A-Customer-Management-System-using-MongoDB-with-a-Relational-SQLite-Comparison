import mongo_demo as m
import sql_demo as s

MENU = """
=============================================
  Document Data Model - Demo Project
=============================================
 1. Insert sample customer (from the paper)
 2. View customers
 3. Add a customer
 4. Find customers by city
 5. Add phone number to a customer
 6. Delete a customer
 7. Flexible schema demo
 8. Schema validation demo
 9. Query and aggregation demo
10. Indexing performance demo
11. ACID transaction demo
12. SQL (SQLite) comparison
 0. Exit
"""

def main():
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                m.insert_sample()
            elif choice == "2":
                m.view_customers()
            elif choice == "3":
                m.add_customer(
                    int(input("Customer ID: ")), input("First name: "), input("Last name: "),
                    input("Email: "), input("City: "), float(input("Annual spend: ")),
                )
            elif choice == "4":
                m.find_by_city(input("City: "))
            elif choice == "5":
                m.add_phone(int(input("Customer ID: ")), input("Phone number: "))
            elif choice == "6":
                m.delete_customer(int(input("Customer ID: ")))
            elif choice == "7":
                m.flexible_schema_demo()
            elif choice == "8":
                m.validation_demo()
            elif choice == "9":
                m.query_demo()
                m.aggregation_demo()
            elif choice == "10":
                m.index_demo()
            elif choice == "11":
                m.transaction_demo()
            elif choice == "12":
                s.run_sql_demo()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
