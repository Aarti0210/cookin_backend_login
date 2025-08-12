from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_HOST, DB_USER, DB_NAME]):
    print("Warning: One or more DB environment variables are not set.")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST or "localhost",
        user=DB_USER or "root",
        password=DB_PASSWORD or "$EAWjfg56K$yc7C",
        database=DB_NAME or "myappdb",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        connect_timeout=10,
    )

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, hashed_password))
            conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except pymysql.err.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/dbtest', methods=['GET'])
def dbtest():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
            _ = cursor.fetchone()
        return jsonify({'db': 'ok'})
    except Exception as e:
        return jsonify({'db': 'error', 'details': str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == '__main__':
    port = int(os.getenv('PORT',3306))
    app.run(host='0.0.0.0', port=port)
