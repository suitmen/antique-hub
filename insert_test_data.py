import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend import models, database
from backend.schemas import UserCreate, LotCreate
import bcrypt

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test_user:password@213.165.55.132:5432/antique_hub")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def insert_test_data():
    """Insert test data into the database"""
    db = SessionLocal()
    
    try:
        # Clear existing data (optional, uncomment if needed)
        # db.query(models.SupportTicket).delete()
        # db.query(models.Order).delete()
        # db.query(models.Lot).delete()
        # db.query(models.User).delete()
        # db.commit()
        
        # Create test users
        users_data = [
            {
                "email": "buyer1@example.com",
                "password": "password123",
                "is_seller": False,
                "verified": True,
                "role": "buyer"
            },
            {
                "email": "buyer2@example.com",
                "password": "password123",
                "is_seller": False,
                "verified": True,
                "role": "buyer"
            },
            {
                "email": "seller1@example.com",
                "password": "password123",
                "is_seller": True,
                "verified": True,
                "role": "seller"
            },
            {
                "email": "seller2@example.com",
                "password": "password123",
                "is_seller": True,
                "verified": True,
                "role": "seller"
            },
            {
                "email": "admin@example.com",
                "password": "password123",
                "is_seller": False,
                "verified": True,
                "role": "admin"
            }
        ]
        
        # Insert users
        users = []
        for user_data in users_data:
            user = models.User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_seller=user_data["is_seller"],
                verified=user_data["verified"],
                role=user_data["role"]
            )
            print(user.hashed_password)
            db.add(user)
            db.flush()  # Get the ID without committing
            users.append(user)
        
        db.commit()
        
        # Get seller IDs for lots
        seller1_id = users[2].id  # seller1@example.com
        seller2_id = users[3].id  # seller2@example.com
        
        # Create test lots
        lots_data = [
            {
                "title": "Antique Wooden Chair",
                "description": "Beautiful antique wooden chair from the 18th century, excellent condition.",
                "price": 12000.00,
                "currency": "RUB",
                "category": "Furniture",
                "era": "18th Century",
                "material": "Wood",
                "image_urls": ["/images/chair1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller1_id
            },
            {
                "title": "Vintage Silver Necklace",
                "description": "Elegant silver necklace with intricate design, circa 1920s.",
                "price": 8500.00,
                "currency": "RUB",
                "category": "Jewelry",
                "era": "1920s",
                "material": "Silver",
                "image_urls": ["/images/necklace1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller1_id
            },
            {
                "title": "Classic Oil Painting",
                "description": "Original oil painting by a lesser-known artist from the 19th century.",
                "price": 45000.00,
                "currency": "RUB",
                "category": "Art",
                "era": "19th Century",
                "material": "Canvas",
                "image_urls": ["/images/painting1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller2_id
            },
            {
                "title": "Antique Porcelain Vase",
                "description": "Delicate porcelain vase with hand-painted flowers, Qing Dynasty.",
                "price": 32000.00,
                "currency": "RUB",
                "category": "Decorative",
                "era": "Qing Dynasty",
                "material": "Porcelain",
                "image_urls": ["/images/vase1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller2_id
            },
            {
                "title": "Vintage Leather Armchair",
                "description": "Luxurious leather armchair from the 1950s, recently restored.",
                "price": 18000.00,
                "currency": "RUB",
                "category": "Furniture",
                "era": "1950s",
                "material": "Leather",
                "image_urls": ["/images/armchair1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller1_id
            },
            {
                "title": "Antique Bronze Statue",
                "description": "Small bronze statue from the Art Deco period, excellent condition.",
                "price": 25000.00,
                "currency": "RUB",
                "category": "Sculpture",
                "era": "Art Deco",
                "material": "Bronze",
                "image_urls": ["/images/statue1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller2_id
            },
            {
                "title": "Vintage Wooden Desk",
                "description": "Magnificent wooden desk from the early 20th century, solid oak construction.",
                "price": 35000.00,
                "currency": "RUB",
                "category": "Furniture",
                "era": "Early 1900s",
                "material": "Oak",
                "image_urls": ["/images/desk1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller1_id
            },
            {
                "title": "Antique Clock",
                "description": "Ornate grandfather clock from the Victorian era, still functional.",
                "price": 55000.00,
                "currency": "RUB",
                "category": "Decorative",
                "era": "Victorian Era",
                "material": "Wood",
                "image_urls": ["/images/clock1.jpg"],
                "is_approved": True,
                "status": "approved",
                "seller_id": seller2_id
            }
        ]
        
        # Insert lots
        lots = []
        for lot_data in lots_data:
            lot = models.Lot(**lot_data)
            db.add(lot)
            lots.append(lot)
        
        db.commit()
        
        print(f"Inserted {len(users)} users and {len(lots)} lots successfully!")
        
        # Print user credentials for testing
        print("\nTest user credentials:")
        for user_data in users_data:
            print(f"Email: {user_data['email']}, Password: {user_data['password']}, Role: {user_data['role']}")
            
    except Exception as e:
        print(f"Error inserting test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()