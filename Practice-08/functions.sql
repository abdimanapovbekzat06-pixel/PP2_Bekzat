CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.username, c.phone
    FROM contacts c
    WHERE c.username ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

SELECT * FROM search_contacts('8707');


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.username, c.phone
    FROM contacts c
    ORDER BY c.username
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_contacts_page(5, 0);

SELECT * FROM get_contacts_page(5, 5);

SELECT * FROM get_contacts_page(5, 10);
