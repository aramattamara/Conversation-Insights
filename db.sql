SELECT CONCAT(extract(YEAR FROM to_timestamp(date)),
              '-',
              extract(MONTH FROM to_timestamp(date))
           )    AS per_day,
       member_id,
       COUNT(*) AS cnt
FROM messages
WHERE member_id IN (388268832)
GROUP BY member_id, per_day;


SELECT COUNT(*)                      cnt,
       to_timestamp("date")::DATE AS day,
       member_id
FROM messages
GROUP BY day, member_id;

COPY members
    FROM '/home/toma/Downloads/t/members.csv'
    DELIMITER ','
    CSV HEADER;

DELETE
FROM messages
WHERE TRUE;
DELETE
FROM members
WHERE TRUE;

SELECT members.member_id   AS members_member_id,
       members.member_name AS members_member_name,
       members.first_name  AS members_first_name,
       members.last_name   AS members_last_name
FROM members
WHERE members.member_id IN (88111010);


SELECT members.*, COUNT(*) total, SUM(LENGTH(m.content)) total_length
FROM members
         INNER JOIN messages m ON members.member_id = m.member_id
WHERE m.chat_id = 1420590782
-- AND member_name ilike 'sdf'
GROUP BY members.member_id
ORDER BY total DESC
;

SELECT m., COUNT(DISTINCT m.member_id) AS total_members
FROM messages m
GROUP BY m.chat_id
ORDER BY m.chat_id

SELECT COUNT(*)
FROM members;

DELETE
FROM chats
WHERE chat_id < 0