# $0 - username
# $1 - user_token

SELECT *
FROM users
WHERE
      username = $0 AND
      user_token = $1;
