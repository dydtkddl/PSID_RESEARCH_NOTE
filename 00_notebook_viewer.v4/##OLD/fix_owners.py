"""Script to fix document owner IDs - assign all documents to dydtkddl user."""
from app.database import SessionLocal
from app.models.user import User
from app.models.document import Document

db = SessionLocal()

# Find the dydtkddl user (try by username or email containing dydtkddl)
target_user = db.query(User).filter(User.username == "dydtkddl").first()
if not target_user:
    target_user = db.query(User).filter(User.email.contains("dydtkddl")).first()
if not target_user:
    # Get the first active user as fallback
    target_user = db.query(User).filter(User.is_active == True).first()

if not target_user:
    print("ERROR: No user found!")
    db.close()
    exit(1)

print(f"Target user: {target_user.username} (ID: {target_user.id})")

# Count documents before fix
total_docs = db.query(Document).count()
print(f"Total documents: {total_docs}")

# Update all documents to be owned by target user
updated = db.query(Document).update({Document.owner_id: target_user.id})
db.commit()

print(f"Updated {updated} documents to owner: {target_user.username}")

# Verify
docs_by_owner = db.query(Document).filter(Document.owner_id == target_user.id).count()
print(f"Documents now owned by {target_user.username}: {docs_by_owner}")

db.close()
print("Done!")
