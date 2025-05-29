import click
from datetime import date
from sqlalchemy.exc import IntegrityError
from database.session import get_db, init_db
from models.pet import Pet
from models.adopter import Adopter
from models.adoption import Adoption

@click.group()
def cli():
    """Pet Adoption Agency CLI"""
    pass

@cli.command()
def setup():
    """Initialize the database"""
    init_db()
    click.echo("Database initialized successfully!")

@cli.command()
@click.option('--name', prompt='Pet name', help='Name of the pet')
@click.option('--species', prompt='Species', type=click.Choice(['dog', 'cat', 'bird', 'rabbit', 'other']), help='Species of the pet')
@click.option('--breed', prompt='Breed', help='Breed of the pet')
@click.option('--age', prompt='Age', type=int, help='Age of the pet in years')
def add_pet(name, species, breed, age):
    """Add a new pet to the database"""
    db = next(get_db())
    try:
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
        click.echo(f"Pet {name} added successfully with ID {pet.id}!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error adding pet: {str(e)}")

@cli.command()
@click.option('--name', prompt='Adopter name', help='Name of the adopter')
@click.option('--email', prompt='Email', help='Email of the adopter')
@click.option('--phone', prompt='Phone', help='Phone number of the adopter')
@click.option('--address', prompt='Address', help='Address of the adopter')
def register_adopter(name, email, phone, address):
    """Register a new adopter"""
    db = next(get_db())
    try:
        adopter = Adopter(
            name=name,
            email=email,
            phone=phone,
            address=address,
            registration_date=date.today()
        )
        db.add(adopter)
        db.commit()
        click.echo(f"Adopter {name} registered successfully with ID {adopter.id}!")
    except IntegrityError:
        db.rollback()
        click.echo("Error: An adopter with this email already exists.")
    except Exception as e:
        db.rollback()
        click.echo(f"Error registering adopter: {str(e)}")

@cli.command()
@click.option('--pet-id', prompt='Pet ID', type=int, help='ID of the pet to adopt')
@click.option('--adopter-id', prompt='Adopter ID', type=int, help='ID of the adopter')
def process_adoption(pet_id, adopter_id):
    """Process a pet adoption"""
    db = next(get_db())
    try:
        # Check if pet exists and is available
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.adopted == 0).first()
        if not pet:
            click.echo("Error: Pet not found or already adopted")
            return
        
        # Check if adopter exists
        adopter = db.query(Adopter).filter(Adopter.id == adopter_id).first()
        if not adopter:
            click.echo("Error: Adopter not found")
            return
        
        # Create adoption record
        adoption = Adoption(
            pet_id=pet_id,
            adopter_id=adopter_id,
            adoption_date=date.today()
        )
        
        # Mark pet as adopted
        pet.adopted = 1
        
        db.add(adoption)
        db.commit()
        click.echo(f"Adoption processed successfully! Pet {pet.name} adopted by {adopter.name}")
    except Exception as e:
        db.rollback()
        click.echo(f"Error processing adoption: {str(e)}")

@cli.command()
def list_pets():
    """List all available pets"""
    db = next(get_db())
    pets = db.query(Pet).filter(Pet.adopted == 0).all()
    
    if not pets:
        click.echo("No available pets found.")
        return
    
    click.echo("\nAvailable Pets:")
    click.echo("ID  Name      Species  Breed          Age")
    click.echo("-----------------------------------------")
    for pet in pets:
        click.echo(f"{pet.id:3} {pet.name:9} {pet.species:7} {pet.breed:14} {pet.age}")

@cli.command()
def list_adopters():
    """List all registered adopters"""
    db = next(get_db())
    adopters = db.query(Adopter).all()
    
    if not adopters:
        click.echo("No adopters registered yet.")
        return
    
    click.echo("\nRegistered Adopters:")
    click.echo("ID  Name            Email                  Phone")
    click.echo("------------------------------------------------")
    for adopter in adopters:
        click.echo(f"{adopter.id:3} {adopter.name:15} {adopter.email:22} {adopter.phone}")

@cli.command()
def list_adoptions():
    """List all adoption records"""
    db = next(get_db())
    adoptions = db.query(Adoption).join(Pet).join(Adopter).all()
    
    if not adoptions:
        click.echo("No adoptions recorded yet.")
        return
    
    click.echo("\nAdoption Records:")
    click.echo("ID  Pet Name      Adopter Name      Date")
    click.echo("-----------------------------------------")
    for adoption in adoptions:
        click.echo(f"{adoption.id:3} {adoption.pet.name:13} {adoption.adopter.name:17} {adoption.adoption_date}")

if __name__ == '__main__':
    cli()