from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo

class User(UserMixin):
    def __init__(self, id, username, email=None):
        self.id = id
        self.username = username
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    # Rechercher l'utilisateur dans la base de données par son ID
    user_data = mongo.db.users.find_one({"_id": user_id})
    if user_data:
        # Utilisez `.get()` pour éviter les KeyErrors si une clé est absente
        return User(user_id, user_data["username"], user_data.get("email"))
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

        if mongo.db.users.find_one({"username": username}):
            return jsonify({"message": "User already exists"}), 400

        if mongo.db.Profil_close.find_one({"username": username}):
            return jsonify({"message": "User already exists"}), 400

            # Déterminer le rôle
        role = "admin" if username.lower() == "admin" else "utilisateur"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = str(uuid.uuid4())
        mongo.db.users.insert_one({
            "_id": user_id,
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": role
        })
        flash("Utilisateur enregistré avec succès.", "success")
        # return redirect('login.html'), 201
        return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifier si l'utilisateur existe dans la base de données
        user_data = mongo.db.users.find_one({"username": username})
        if not user_data or not bcrypt.check_password_hash(user_data["password"], password):
            return jsonify({"message": "Invalid email or password"}), 401

        # Créer l'objet utilisateur et connecter l'utilisateur
        user = User(user_data["_id"], user_data["username"], user_data["email"])
        login_user(user, remember=True)  # Crée un cookie persistant avec remember=True

        # Rediriger vers le tableau de bord
        return redirect(url_for('dashboard'))

    # Afficher le formulaire de connexion pour les requêtes GET
    return render_template('dashboard.html')
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Déconnecté avec succès.", "success")
    return render_template('login.html'),200
    # return jsonify({"message": "Logged out successfully"})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
