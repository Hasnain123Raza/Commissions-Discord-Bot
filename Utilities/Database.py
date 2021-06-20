from tinydb import TinyDB

db = TinyDB("db.json")

commissionsTable = db.table("commissions")
configurationsTable = db.table("configurations")
