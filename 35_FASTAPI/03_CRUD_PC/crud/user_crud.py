from sqlalchemy import text

def get_all_users(db):
    result = db.execute(text('SELECT * FROM "b_users"'))

    users = []
    for row in result.mappings():
        users.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "age": row["age"]
        })

    return users