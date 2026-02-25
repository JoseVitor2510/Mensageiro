from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "segredo"

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# MODELOS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    created_by = db.Column(db.Integer)

class EmailSent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


with app.app_context():
    db.create_all()

# ROTAS

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(email=data["email"], password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Credenciais inválidas"}), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    user_id = int(get_jwt_identity())
    users = User.query.filter(User.id != user_id).all()
    return jsonify([{"id": u.id, "email": u.email} for u in users])


@app.route("/templates", methods=["POST"])
@jwt_required()
def create_template():
    user_id = int(get_jwt_identity())
    data = request.json
    
    template = Template(
        title=data["title"],
        subject=data["subject"],
        body=data["body"],
        created_by=user_id
    )
    
    db.session.add(template)
    db.session.commit()
    
    return jsonify({"msg": "Template criado"})

@app.route("/templates", methods=["GET"])
@jwt_required()
def list_templates():
    user_id = int(get_jwt_identity())

    templates = Template.query.filter_by(created_by=user_id).all()

    result = []
    for t in templates:
        result.append({
            "id": t.id,
            "title": t.title,
            "subject": t.subject,
            "body": t.body
        })
    return jsonify(result)

@app.route("/send-email", methods=["POST"])
@jwt_required()
def send_email():
    sender_id = int(get_jwt_identity())
    data = request.json

    template = Template.query.get(data["template_id"])
    receiver = User.query.get(data["receiver_id"])

    if not template:
        return jsonify({"msg": "Template não encontrado"}), 404

    if not receiver:
        return jsonify({"msg": "Usuário destinatário não encontrado"}), 404

    message = template.body.replace("{{nome}}", data.get("nome", ""))

    email_record = EmailSent(
        sender_id=sender_id,
        receiver_id=receiver.id,
        template_id=template.id,
        subject=template.subject,
        body=message
    )

    db.session.add(email_record)
    db.session.commit()

    return jsonify({"msg": "Email registrado com sucesso"})

@app.route("/emails", methods=["GET"])
@jwt_required()
def list_emails():
    user_id = int(get_jwt_identity())

    emails = EmailSent.query.filter(
        (EmailSent.sender_id == user_id) |
        (EmailSent.receiver_id == user_id)
    ).all()

    result = []

    for e in emails:
        result.append({
            "id": e.id,
            "sender_id": e.sender_id,
            "receiver_id": e.receiver_id,
            "subject": e.subject,
            "body": e.body,
            "created_at": e.created_at
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)