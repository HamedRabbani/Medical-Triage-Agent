from infrastructure.database.connection import engine


try:
    with engine.connect() as connection:
        print("Connected to Supabase")

except Exception as e:
    print(e)