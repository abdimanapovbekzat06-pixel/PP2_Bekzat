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
            """
            INSERT INTO contacts (username, phone)
            VALUES (%s, %s)
            """,
            (name, phone)
        )

        conn.commit()
        print("Contact added successfully!")

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
    value = input("Enter username or phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            DELETE FROM contacts
            WHERE username = %s OR phone = %s
            """,
            (value, value)
        )

        if cur.rowcount > 0:
            print("Contact deleted successfully!")
        else:
            print("Contact not found!")

        conn.commit()

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


while True:
    print("\n--- PHONEBOOK ---")
    print("1. Add contact")
    print("2. Show contacts")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Search contact")
    print("6. Import CSV")
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

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
