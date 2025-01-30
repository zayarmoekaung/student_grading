from flask_seeder import Seeder, Faker, generator
from werkzeug.security import generate_password_hash
from model.user import User

class AdminSeeder(Seeder):
    """Seeder class for creating an Admin user."""

    def run(self):
        admin_email = "zayarmoekaung0@gmail.com"
        print(f"Running Admin user Seeder")
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin = User(
                name="Admin",
                email=admin_email,
                password=generate_password_hash("admin123", method="pbkdf2:sha256"),
                role="ADMIN",
                active=True
            )
            print(f"Seeding Admin user: {admin.email}")
            self.db.session.add(admin)
        else:
            print("Admin user already exists.")

        self.db.session.commit()
