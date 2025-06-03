from datetime import date
from sqlalchemy.exc import IntegrityError
from database.session import get_db, init_db
from models.pet import Pet
from models.adopter import Adopter
from models.adoption import Adoption

def setup():
    init_db()
    print("✅ Database initialized successfully!")

def add_pet():
    db = next(get_db())
    try:
        name = input("Pet name: ")
        species = input("Species (dog/cat/bird/rabbit/other): ").lower()
        breed = input("Breed: ")
        age = int(input("Age in years: "))

        pet = Pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            arrival_date=date.today(),
            adopted=0
        )
        db.add(pet)
        db.commit()
        print(f"✅ Pet {name} added successfully with ID {pet.id}!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding pet: {str(e)}")

def register_adopter():
    db = next(get_db())
    try:
        name = input("Adopter name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        address = input("Address: ")

        adopter = Adopter(
            name=name,
            email=email,
            phone=phone,
            address=address,
            registration_date=date.today()
        )
        db.add(adopter)
        db.commit()
        print(f"✅ Adopter {name} registered successfully with ID {adopter.id}!")
    except IntegrityError:
        db.rollback()
        print("❌ Error: An adopter with this email already exists.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error registering adopter: {str(e)}")

def process_adoption():
    db = next(get_db())
    try:
        pet_id = int(input("Pet ID: "))
        adopter_id = int(input("Adopter ID: "))

        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.adopted == 0).first()
        if not pet:
            print("❌ Pet not found or already adopted")
            return

        adopter = db.query(Adopter).filter(Adopter.id == adopter_id).first()
        if not adopter:
            print("❌ Adopter not found")
            return

        adoption = Adoption(
            pet_id=pet_id,
            adopter_id=adopter_id,
            adoption_date=date.today()
        )
        pet.adopted = 1
        db.add(adoption)
        db.commit()
        print(f"🎉 Adoption successful! {adopter.name} adopted {pet.name}.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error processing adoption: {str(e)}")

def list_pets():
    db = next(get_db())
    pets = db.query(Pet).filter(Pet.adopted == 0).all()

    if not pets:
        print("😿 No available pets found.")
        return

    print("\n🐾 Available Pets 🐾")
    print("ID  Name       Species  Breed          Age")
    print("---------------------------------------------")
    for pet in pets:
        print(f"{pet.id:3} {pet.name:10} {pet.species:8} {pet.breed:14} {pet.age}")

def list_adopters():
    db = next(get_db())
    adopters = db.query(Adopter).all()

    if not adopters:
        print("🙈 No adopters registered yet.")
        return

    print("\n👥 Registered Adopters")
    print("ID  Name             Email                   Phone")
    print("---------------------------------------------------------")
    for adopter in adopters:
        print(f"{adopter.id:3} {adopter.name:16} {adopter.email:23} {adopter.phone}")

def list_adoptions():
    db = next(get_db())
    adoptions = db.query(Adoption).join(Pet).join(Adopter).all()

    if not adoptions:
        print("😢 No adoptions recorded yet.")
        return

    print("\n📜 Adoption Records")
    print("ID  Pet Name      Adopter Name     Date")
    print("---------------------------------------------")
    for adoption in adoptions:
        print(f"{adoption.id:3} {adoption.pet.name:13} {adoption.adopter.name:16} {adoption.adoption_date}")

def main_menu():
    while True:
        print("\n🐾 Pet Adoption Agency CLI 🐾")
        print("""
1. Initialize Database
2. Add New Pet
3. Register New Adopter
4. Process Adoption
5. List Available Pets
6. List Registered Adopters
7. List Adoption Records
8. Exit
""")
        choice = input("Please enter the number of your choice: ").strip()

        if choice == '1':
            setup()
        elif choice == '2':
            add_pet()
        elif choice == '3':
            register_adopter()
        elif choice == '4':
            process_adoption()
        elif choice == '5':
            list_pets()
        elif choice == '6':
            list_adopters()
        elif choice == '7':
            list_adoptions()
        elif choice == '8':
            print(" Have a fluffful day!")
            break
        else:
            print("❗ Invalid choice. Please enter a number from 1 to 8.")

if __name__ == '__main__':
    main_menu()
