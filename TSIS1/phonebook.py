import csv
import json
from pathlib import Path
import psycopg2
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
                "SELECT id, phone FROM contacts WHERE username = %s FOR UPDATE",
                (name,),
            )
            contact = cur.fetchone()
            if contact is None:
                print("Contact not found!")
                return

            contact_id, old_phone = contact

            if new_phone != old_phone:
                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, type)
                    SELECT %s, %s, COALESCE(
                        (SELECT type FROM phones WHERE contact_id = %s AND phone = %s),
                        'mobile'
                    )
                    ON CONFLICT (contact_id, phone) DO NOTHING
                    """,
                    (contact_id, new_phone, contact_id, old_phone),
                )
                cur.execute(
                    "DELETE FROM phones WHERE contact_id = %s AND phone = %s",
                    (contact_id, old_phone),
                )

            cur.execute(
                "UPDATE contacts SET phone = %s WHERE id = %s",
                (new_phone, contact_id),
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
    print("1. Delete by username")
    print("2. Delete by phone")

    choice = input("Choose option: ")

    if choice == "1":
        username = input("Enter username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        params = (username, None)

    elif choice == "2":
        phone = input("Enter phone: ").strip()

        if not phone:
            print("Phone cannot be empty.")
            return

        params = (None, phone)

    else:
        print("Invalid choice.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL delete_contact(%s, %s)", params)
        conn.commit()
        print("Delete operation completed.")

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
    path = Path(__file__).with_name("contacts.csv")
    imported = 0
    skipped = 0

    conn = connect()
    try:
        with conn, conn.cursor() as cur, path.open(
            encoding="utf-8-sig", newline=""
        ) as file:
            for row in csv.DictReader(file):
                username = row["username"].strip()
                phone = row["phone"].strip()
                email = (row.get("email") or "").strip() or None
                birthday = (row.get("birthday") or "").strip() or None
                group = (row.get("group") or "").strip()
                phone_type = (row.get("phone_type") or "").strip() or "mobile"

                cur.execute(
                    """
                    INSERT INTO contacts (username, phone, email, birthday)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING id
                    """,
                    (username, phone, email, birthday),
                )
                if cur.fetchone() is None:
                    skipped += 1
                    continue

                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (username, phone, phone_type),
                )
                if group:
                    cur.execute("CALL move_to_group(%s, %s)", (username, group))

                imported += 1
    except (OSError, KeyError) as error:
        print(f"CSV import failed: {error}")
        return
    except psycopg2.Error as error:
        print(f"CSV import failed: {error}")
        return
    finally:
        conn.close()

    print(f"Imported: {imported}, skipped: {skipped}")


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
        if limit <= 0:
            raise ValueError
    except ValueError:
        print("Enter a positive whole number.")
        return

    conn = connect()
    try:
        page = 1
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, 0))
            rows = cur.fetchall()

            if not rows:
                print("PhoneBook is empty!")
                return

            while True:
                print(f"\n--- Page {page} ---")
                for username, phone in rows:
                    print(f"{username}: {phone}")

                command = input("next / prev / quit: ").strip().lower()
                if command == "quit":
                    return
                if command not in ("next", "prev"):
                    print("Enter next, prev, or quit.")
                    continue

                target_page = page + 1 if command == "next" else page - 1
                if target_page < 1:
                    print("You are already on the first page.")
                    continue

                offset = (target_page - 1) * limit
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s)",
                    (limit, offset),
                )
                new_rows = cur.fetchall()

                if new_rows:
                    page = target_page
                    rows = new_rows
                else:
                    print("You are already on the last page.")
    finally:
        conn.close()



def filter_contacts():
    group = input("Group (Enter for all): ").strip()
    email = input("Part of email (Enter for all): ").strip()
    sort = input("Sort by 1) name, 2) birthday, 3) date added: ").strip()

    sort_options = {
        "1": "c.username",
        "2": "c.birthday ASC NULLS LAST",
        "3": "c.created_at DESC NULLS LAST",
    }
    order_by = sort_options.get(sort, "c.username")

    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT c.username, c.email, c.birthday, g.name
                FROM contacts AS c
                LEFT JOIN groups AS g ON g.id = c.group_id
                WHERE (%s = '' OR lower(g.name) = lower(%s))
                  AND (%s = '' OR strpos(lower(c.email), lower(%s)) > 0)
                ORDER BY {order_by}, c.id
                """,
                (group, group, email, email),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        print("No contacts found.")
        return

    for username, email, birthday, group in rows:
        print(f"{username} | {email or '-'} | {birthday or '-'} | {group or '-'}")



def export_json():
    path = Path(__file__).with_name("contacts.json")
    conn = connect()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.username, c.phone, c.email, c.birthday, g.name,
                       ARRAY(
                           SELECT json_build_object('phone', p.phone, 'type', p.type)
                           FROM phones AS p
                           WHERE p.contact_id = c.id
                           ORDER BY p.id
                       ) AS phones
                FROM contacts AS c
                LEFT JOIN groups AS g ON g.id = c.group_id
                ORDER BY c.id
                """
            )
            rows = cur.fetchall()

        contacts = []
        for username, phone, email, birthday, group, phones in rows:
            if not any(item["phone"] == phone for item in phones):
                phones.insert(0, {"phone": phone, "type": "mobile"})

            contacts.append({
                "username": username,
                "primary_phone": phone,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group,
                "phones": phones,
            })

        with path.open("w", encoding="utf-8") as file:
            json.dump(contacts, file, ensure_ascii=False, indent=2)

        print(f"Exported {len(contacts)} contacts to {path.name}.")
    except (OSError, psycopg2.Error) as error:
        print(f"JSON export failed: {error}")
    finally:
        conn.close()



def import_json():
    path = Path(__file__).with_name("contacts.json")
    conn = connect()
    imported = 0
    skipped = 0

    try:
        with path.open(encoding="utf-8") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            raise ValueError("JSON must contain a list of contacts.")

        with conn, conn.cursor() as cur:
            for contact in contacts:
                username = contact["username"]

                cur.execute(
                    "SELECT id FROM contacts WHERE username = %s FOR UPDATE",
                    (username,),
                )
                existing = cur.fetchone()

                if existing is not None:
                    while True:
                        action = input(
                            f"{username} already exists. skip / overwrite: "
                        ).strip().lower()
                        if action in ("skip", "overwrite"):
                            break
                        print("Enter skip or overwrite.")

                    if action == "skip":
                        skipped += 1
                        continue

                phone = contact["primary_phone"]
                email = contact.get("email")
                birthday = contact.get("birthday")
                group = contact.get("group")
                phones = contact["phones"]

                if not any(item["phone"] == phone for item in phones):
                    raise ValueError(f"{username}: primary phone is missing from phones.")

                if existing is None:
                    cur.execute(
                        """
                        INSERT INTO contacts (username, phone, email, birthday)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (username, phone, email, birthday),
                    )
                else:
                    contact_id = existing[0]
                    cur.execute(
                        """
                        UPDATE contacts
                        SET phone = %s, email = %s, birthday = %s, group_id = NULL
                        WHERE id = %s
                        """,
                        (phone, email, birthday, contact_id),
                    )
                    cur.execute(
                        "DELETE FROM phones WHERE contact_id = %s",
                        (contact_id,),
                    )

                if group:
                    cur.execute("CALL move_to_group(%s, %s)", (username, group))

                for item in phones:
                    cur.execute(
                        "CALL add_phone(%s, %s, %s)",
                        (username, item["phone"], item["type"]),
                    )

                imported += 1

        print(f"Imported or updated: {imported}, skipped: {skipped}")
    except (OSError, ValueError, KeyError, TypeError, psycopg2.Error) as error:
        print(f"JSON import failed: {error}")
    finally:
        conn.close()



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
    print("10. Filter and sort contacts")
    print("11. Export to JSON")
    print("12. Import from JSON")
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

    elif choice == "10":
        filter_contacts() 

    elif choice == "11":
        export_json() 

    elif choice == "12":
        import_json() 

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
