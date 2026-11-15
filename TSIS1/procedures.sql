CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" does not exist', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE username = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" does not exist', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE (username VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.username, c.phone
    FROM contacts AS c
    WHERE c.username ILIKE '%' || pattern || '%'
       OR c.email ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%'
       OR EXISTS (
           SELECT 1
           FROM phones AS p
           WHERE p.contact_id = c.id
             AND p.phone ILIKE '%' || pattern || '%'
       )
    ORDER BY c.username;
END;
$$;