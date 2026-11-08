CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts
        WHERE username = p_username
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO contacts(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;

CALL upsert_contact('Bekzat', '87071234567');

SELECT * FROM contacts
WHERE username = 'Bekzat';

CALL upsert_contact('Bekzat', '87775554433');

SELECT * FROM contacts
WHERE username = 'Bekzat';



CREATE OR REPLACE PROCEDURE bulk_insert(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    OUT incorrect_data TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    incorrect_data := ARRAY[]::TEXT[];

    IF COALESCE(array_length(p_names, 1), 0)
       <> COALESCE(array_length(p_phones, 1), 0) THEN
        RAISE EXCEPTION 'Names and phones must have the same length';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_names, 1), 0) LOOP

        IF p_names[i] IS NULL
           OR TRIM(p_names[i]) = ''
           OR p_phones[i] IS NULL
           OR p_phones[i] !~ '^87[0-9]{9}$'
           OR EXISTS (
               SELECT 1 FROM contacts
               WHERE phone = p_phones[i]
                 AND username IS DISTINCT FROM p_names[i]
           )
        THEN
            incorrect_data := array_append(
                incorrect_data,
                COALESCE(p_names[i], 'NULL') || ': ' ||
                COALESCE(p_phones[i], 'NULL')
            );

        ELSE
            UPDATE contacts
            SET phone = p_phones[i]
            WHERE username = p_names[i];

            IF NOT FOUND THEN
                INSERT INTO contacts(username, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        END IF;

    END LOOP;
END;
$$;



CALL bulk_insert(
    ARRAY['Ali', 'Dana', 'Arman'],
    ARRAY['87071112233', '12345', '87775554433'],
    NULL
);

SELECT * FROM contacts
WHERE username IN ('Ali', 'Arman');


CREATE OR REPLACE PROCEDURE delete_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE (p_username IS NOT NULL AND username = p_username)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;

CALL upsert_contact('TestUser', '87070001122');

CALL delete_contact('TestUser', NULL);      

SELECT * FROM contacts
WHERE username = 'TestUser';

CALL upsert_contact('TestUser', '87070001122');

CALL delete_contact(NULL, '87070001122');

SELECT * FROM contacts
WHERE username = 'TestUser';

SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name IN (
    'search_contacts',
    'upsert_contact',
    'bulk_insert',
    'get_contacts_page',
    'delete_contact'
);