from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required
from app import *
from app import app
from app import mongo

# User Model
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": user_id})
    if user_data:
        return User(user_id, user_data["username"], user_data["email"])
    return None


# Routes pour le systeme de log


# le systeme des identications des users pages
@app.route('/me')
@login_required
def me():
    return current_user.username



@app.route("/substcription", methods=["GET", "POST"])
def subscription():
    return render_template('register.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if mongo.db.users.find_one({"email": email}):
            return jsonify({"message": "User already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = str(uuid.uuid4())
        mongo.db.users.insert_one({
            "_id": user_id,
            "username": username,
            "email": email,
            "password": hashed_password
        })
        return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérifier si l'utilisateur existe dans la base de données
        user_data = mongo.db.users.find_one({"email": email})
        if not user_data or not bcrypt.check_password_hash(user_data["password"], password):
            return jsonify({"message": "Invalid email or password"}), 401

        # Créer l'objet utilisateur et connecter l'utilisateur
        user = User(user_data["_id"], user_data["username"], user_data["email"])
        login_user(user, remember=True)  # Crée un cookie persistant avec remember=True

        # Rediriger vers le tableau de bord
        return redirect(url_for('dashboard'))

    # Afficher le formulaire de connexion pour les requêtes GET
    return render_template('login.html')
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

