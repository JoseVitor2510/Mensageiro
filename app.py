from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "segredo"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# MODELOS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    created_by = db.Column(db.Integer)

with app.app_context():
    db.create_all()

# ROTAS

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Usuário criado"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    if not user:
        return jsonify({"msg": "Credenciais inválidas"}), 401
    
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/templates", methods=["POST"])
@jwt_required()
def create_template():
    user_id = get_jwt_identity()
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
    templates = Template.query.all()
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
    data = request.json
    template = Template.query.get(data["template_id"])
    
    message = template.body.replace("{{nome}}", data["nome"])
    
    print("EMAIL ENVIADO")
    print("Assunto:", template.subject)
    print("Mensagem:", message)
    
    return jsonify({"msg": "Email enviado (simulado)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)