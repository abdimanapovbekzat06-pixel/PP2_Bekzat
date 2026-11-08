
import csv
from pathlib import Path
from connect import connect



def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL upsert_contact(%s, %s)",
            (name, phone)
        )

        conn.commit()
        print("Contact added or updated successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def show_contacts():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM contacts ORDER BY id")
        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("PhoneBook is empty!")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def update_contact():
    name = input("Enter username: ")

    print("1. Change name")
    print("2. Change phone")
    choice = input("Choose: ")

    if choice not in ("1", "2"):
        print("Invalid choice!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_name = input("Enter new name: ").strip()

            if not new_name:
                print("Name cannot be empty!")
                return

            cur.execute(
                """
                UPDATE contacts
                SET username = %s
                WHERE username = %s
                """,
                (new_name, name)
            )

        elif choice == "2":
            new_phone = input("Enter new phone: ").strip()

            if not new_phone:
                print("Phone cannot be empty!")
                return

            cur.execute(
                """
                UPDATE contacts
                SET phone = %s
                WHERE username = %s
                """,
                (new_phone, name)
            )

        if cur.rowcount > 0:
            print("Contact updated successfully!")
        else:
            print("Contact not found!")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()



def delete_contact():
    value = input("Enter username or phone: ").strip()

    if not value:
        print("Input cannot be empty!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL delete_contact(%s, %s)",
            (value, None)
            if not value.isdigit()
            else (None, value)
        )

        conn.commit()
        print("Delete procedure executed successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def search_contact():
    print("1. Search by name")
    print("2. Search by phone prefix")

    choice = input("Choose: ")

    if choice not in ("1", "2"):
        print("Invalid choice!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter name: ")

            cur.execute(
                """
                SELECT * FROM contacts
                WHERE username ILIKE %s
                """,
                ("%" + name + "%",)
            )

        elif choice == "2":
            phone = input("Enter phone prefix: ")

            cur.execute(
                """
                SELECT * FROM contacts
                WHERE phone LIKE %s
                """,
                (phone + "%",)
            )

        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found!")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def import_csv():
    file_path = Path(__file__).with_name("contacts.csv")

    conn = connect()
    cur = conn.cursor()

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            count = 0

            for row in reader:
                name = row["username"].strip()
                phone = row["phone"].strip()

                if not name or not phone:
                    continue

                cur.execute(
                    """
                    INSERT INTO contacts (username, phone)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (name, phone)
                )

                count += cur.rowcount

        conn.commit()
        print(f"Successfully imported {count} contacts!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def search_contacts():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM search_contacts(%s)",
            (pattern,)
        )

        results = cur.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print("No contacts found!")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def bulk_insert_contacts():
    names = []
    phones = []

    n = int(input("How many contacts? "))

    for i in range(n):
        print(f"\nContact {i + 1}")

        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()

        names.append(name)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL bulk_insert(%s::TEXT[], %s::TEXT[], NULL)",
            (names, phones)
        )

        incorrect = cur.fetchone()[0]
        conn.commit()

        print("\nBulk insert completed!")

        if incorrect:
            print("Incorrect contacts:")
            for contact in incorrect:
                print(contact)
        else:
            print("All contacts inserted successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def show_contacts_page():
    try:
        limit = int(input("How many contacts per page? "))
        page = int(input("Enter page number: "))

        if limit <= 0 or page <= 0:
            print("Numbers must be positive!")
            return

        offset = (page - 1) * limit

        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )

            contacts = cur.fetchall()

            if contacts:
                for contact in contacts:
                    print(contact)
            else:
                print("No contacts on this page!")

        except Exception as e:
            print("Error:", e)

        finally:
            cur.close()
            conn.close()

    except ValueError:
        print("Please enter valid numbers!")



while True:
    print("\n--- PHONEBOOK ---")
    print("1. Add contact")
    print("2. Show contacts")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Search contact")
    print("6. Import CSV")
    print("7. Search contacts by pattern")
    print("8. Bulk insert contacts")
    print("9. Show contacts with pagination")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_contact()

    elif choice == "2":
        show_contacts()

    elif choice == "3":
        update_contact()

    elif choice == "4":
        delete_contact()

    elif choice == "5":
        search_contact()

    elif choice == "6":
        import_csv()

    elif choice == "7":
        search_contacts()

    elif choice == "8":
        bulk_insert_contacts()

    elif choice == "9":
        show_contacts_page()    

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
