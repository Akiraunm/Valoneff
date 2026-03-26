from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
from flask import render_template


app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
# подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["valoneff"]
users = db["users"]

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

# регистрация
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    email = data.get("email")
    password = data.get("password")  

    if not email or not password:
        return jsonify({"error": "Заполни все поля"}), 400

    # проверка на существование
    if users.find_one({"email": email}):
        return jsonify({"error": "Пользователь уже есть"}), 400

    # хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Регистрация успешна"}), 201


# логин
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})

    # проверка через bcrypt
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    return jsonify({"message": "Вход выполнен"}), 200


# просмотр пользователей (для теста)
@app.route("/users", methods=["GET"])
def get_users():
    all_users = []

    for user in users.find():
        all_users.append({
            "email": user["email"],
            "password": str(user["password"])
        })

    return jsonify(all_users)
agents = [
    {
        "name": "Jett",
        "role": "Duelist",
        "abilities": ["Dash", "Updraft", "Smoke"]
    },
    {
        "name": "Sova",
        "role": "Initiator",
        "abilities": ["Recon Bolt", "Drone", "Shock Dart"]
    },
    {
        "name": "Sage",
        "role": "Sentinel",
        "abilities": ["Heal", "Wall", "Slow Orb"]
    }
]
@app.route("/agents", methods=["GET"])
def get_agents():
    return jsonify(agents)
maps = [
    {"name": "Ascent"},
    {"name": "Bind"},
    {"name": "Split"},
    {"name": "Lotus"}
]

@app.route("/maps", methods=["GET"])
def get_maps():
    return jsonify(maps)
updates = [
    {"agent": "Jett", "change": "Nerf dash cooldown"},
    {"agent": "Sage", "change": "Buff heal speed"}
]

@app.route("/updates", methods=["GET"])
def get_updates():
    return jsonify(updates)

if __name__ == "__main__":
    app.run(debug=True)