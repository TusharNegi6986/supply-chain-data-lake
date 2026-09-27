from dotenv import load_dotenv
import os
load_dotenv(".env")
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("DATA_CSV   :", os.getenv("DATA_CSV"))
