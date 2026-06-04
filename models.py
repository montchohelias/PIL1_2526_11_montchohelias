from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Table pour les compétences d'un utilisateur
user_competences = db.Table('user_competences',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('competence_id', db.Integer, db.ForeignKey('competence.id'), primary_key=True)
)

# Table pour les lacunes d'un utilisateur
user_lacunes = db.Table('user_lacunes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('competence_id', db.Integer, db.ForeignKey('competence.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    photo_profil = db.Column(db.String(255), default='default.png')
    filiere = db.Column(db.String(50), nullable=False)
    niveau = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text)
    centres_interet = db.Column(db.String(255))
    disponibilites = db.Column(db.Text, default='{}')
    est_mentor = db.Column(db.Boolean, default=False)
    est_mentore = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    competences = db.relationship('Competence', secondary=user_competences, backref='experts')
    lacunes = db.relationship('Competence', secondary=user_lacunes, backref='demandeurs')
    offres = db.relationship('Offre', backref='auteur', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_disponibilites(self):
        import json
        try:
            return json.loads(self.disponibilites)
        except:
            return {}
    
    def set_disponibilites(self, dispo_dict):
        import json
        self.disponibilites = json.dumps(dispo_dict)

class Competence(db.Model):
    __tablename__ = 'competence'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    categorie = db.Column(db.String(50))

class Offre(db.Model):
    __tablename__ = 'offre'
    id = db.Column(db.Integer, primary_key=True)
    type_offre = db.Column(db.String(20), nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    competence_id = db.Column(db.Integer, db.ForeignKey('competence.id'))
    disponibilites = db.Column(db.Text, default='{}')
    format_session = db.Column(db.String(20), default='les_deux')
    statut = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    competence = db.relationship('Competence')

class Matching(db.Model):
    __tablename__ = 'matching'
    id = db.Column(db.Integer, primary_key=True)
    offre_id = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentore_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score_matching = db.Column(db.Float, default=0.0)
    statut = db.Column(db.String(20), default='propose')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    mentor = db.relationship('User', foreign_keys=[mentor_id])
    mentore = db.relationship('User', foreign_keys=[mentore_id])

class Conversation(db.Model):
    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)
    matching_id = db.Column(db.Integer, db.ForeignKey('matching.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

conversation_participants = db.Table('conversation_participants',
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    lu = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)