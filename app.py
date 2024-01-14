from flask import Flask, request, render_template,  redirect, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

############

@app.route('/')
def home_page():
    """Homepage listing Pets"""
    
    pets = Pet.query.all()
    return render_template("home_pet_list.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Render add pet form (GET) or handles add pet form submission"""
    form = AddPetForm()
    if form.validate_on_submit():
        
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
    
        age = form.age.data
        notes = form.notes.data
        
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=True)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("pet_add_form.html", form=form)
    

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet form (GET) or handles update pet form submission"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        return redirect('/')
    else:
        return render_template("pet_edit_form.html", form=form, pet=pet)