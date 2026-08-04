from app.database.session import engine

try:
    with engine.connect() as connection:
        print("Database connected successfully!")

except Exception as e:
    print(e)