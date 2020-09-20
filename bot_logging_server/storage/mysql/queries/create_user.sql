# $0 - username
# $1 - tel_id
# $2 - user_token

INSERT INTO users
    (username, tel_id, user_token)
    VALUES ($0, $1, $2)
