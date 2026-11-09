import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from decouple import config
from pymongo import MongoClient

def main() -> int:
    uri = config("MONGO_URI")
    db_name = config("MONGO_DB_NAME", default="airline_saas")

    safe_uri = uri.split("@")[-1] if "@" in uri else uri
    print(f"Connecting to: ...@{safe_uri}")

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=8000)
        pong = client.admin.command("ping")
        print(f"✅ Ping OK: {pong}")

        db = client[db_name]
        db["_healthcheck"].insert_one({"msg": "hello", "from": "test_mongo.py"})
        count = db["_healthcheck"].count_documents({})
        print(f"✅ Write OK: {db_name}._healthcheck has {count} doc(s)")

        db["_healthcheck"].delete_many({})
        print("✅ Cleanup OK")
        return 0
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())