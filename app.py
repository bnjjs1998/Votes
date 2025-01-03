from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Changez cette clé pour sécuriser votre application

# Configuration MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('login.html')



@app.route('/dashboard')
@login_required
def dashboard():
    # Vous pouvez ici ajouter des informations à transmettre au template (comme l'utilisateur connecté)
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET'])
@login_required  # Assure que seul un utilisateur connecté peut accéder à cette route
def profile():
    # Récupération des informations de l'utilisateur depuis MongoDB
    user_data = mongo.db.users.find_one({"_id": current_user.id})
    if not user_data:
        return jsonify({"message": "User not found"}), 404

    # Création de la réponse avec les données de l'utilisateur
    user_profile = {
        "username": user_data["username"],
        "email": user_data["email"],
    }
    return jsonify(user_profile), 200


# Routes
@app.route('/register', methods=['POST'])
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

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": f"Welcome {current_user.username}"})

if __name__ == '__main__':
    app.run(debug=True)
