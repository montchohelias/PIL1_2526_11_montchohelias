from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Competence, Offre, Matching, Conversation, Message, conversation_participants
from matching_algorithm import MatchingAlgorithm
import json

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== AUTHENTIFICATION ==========

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            email=request.form['email'],
            telephone=request.form['telephone'],
            filiere=request.form['filiere'],
            niveau=request.form['niveau']
        )
        user.set_password(request.form['password'])
        user.est_mentor = 'est_mentor' in request.form
        user.est_mentore = 'est_mentore' in request.form
        
        db.session.add(user)
        db.session.commit()
        
        for cid in request.form.getlist('competences'):
            comp = Competence.query.get(int(cid))
            if comp:
                user.competences.append(comp)
        
        for lid in request.form.getlist('lacunes'):
            lac = Competence.query.get(int(lid))
            if lac:
                user.lacunes.append(lac)
        
        jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
        dispo = {}
        for jour in jours:
            creneaux = request.form.getlist(f'dispo_{jour}')
            if creneaux:
                dispo[jour] = creneaux
        user.set_disponibilites(dispo)
        db.session.commit()
        
        flash('Inscription reussie !', 'success')
        return redirect(url_for('login'))
    
    competences = Competence.query.all()
    return render_template('register.html', competences=competences)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        user = User.query.filter((User.email == identifiant) | (User.telephone == identifiant)).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Identifiants incorrects', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ========== DASHBOARD & PROFIL ==========

@app.route('/dashboard')
@login_required
def dashboard():
    mes_offres = Offre.query.filter_by(user_id=current_user.id).all()
    mes_matchings = Matching.query.filter(
        (Matching.mentor_id == current_user.id) | (Matching.mentore_id == current_user.id)
    ).all()
    competences = Competence.query.all()
    return render_template('dashboard.html', offres=mes_offres, matchings=mes_matchings, competences=competences)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.nom = request.form['nom']
        current_user.prenom = request.form['prenom']
        current_user.bio = request.form['bio']
        current_user.competences = []
        current_user.lacunes = []
        for cid in request.form.getlist('competences'):
            comp = Competence.query.get(int(cid))
            if comp:
                current_user.competences.append(comp)
        for lid in request.form.getlist('lacunes'):
            lac = Competence.query.get(int(lid))
            if lac:
                current_user.lacunes.append(lac)
        db.session.commit()
        flash('Profil mis a jour', 'success')
        return redirect(url_for('profile'))
    
    competences = Competence.query.all()
    return render_template('profile.html', competences=competences)

# ========== OFFRES & MATCHING ==========

@app.route('/offre/nouvelle', methods=['POST'])
@login_required
def nouvelle_offre():
    offre = Offre(
        type_offre=request.form['type_offre'],
        titre=request.form['titre'],
        description=request.form['description'],
        user_id=current_user.id,
        competence_id=request.form.get('competence_id') or None,
        format_session=request.form['format_session']
    )
    db.session.add(offre)
    db.session.commit()
    flash('Offre publiee !', 'success')
    return redirect(url_for('dashboard'))

@app.route('/matching/<int:offre_id>')
@login_required
def matching(offre_id):
    offre = Offre.query.get_or_404(offre_id)
    if offre.user_id != current_user.id:
        flash('Acces non autorise', 'danger')
        return redirect(url_for('dashboard'))
    
    algo = MatchingAlgorithm()
    resultats = algo.trouver_matchings(offre)
    return render_template('matching.html', offre=offre, resultats=resultats)

# ========== MESSAGERIE ==========

@app.route('/messages')
@login_required
def messages_list():
    conversations = Conversation.query.join(conversation_participants).filter(
        conversation_participants.c.user_id == current_user.id
    ).all()
    return render_template('messages_list.html', conversations=conversations)

@app.route('/messages/<int:conversation_id>')
@login_required
def messages(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    if current_user not in conversation.participants:
        flash('Acces non autorise', 'danger')
        return redirect(url_for('messages_list'))
    
    msgs = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    return render_template('messages.html', conversation=conversation, messages=msgs)

# ========== RAPPORT ==========

@app.route('/rapport')
def rapport():
    return render_template('rapport.html')

# ========== INITIALISATION BDD ==========

@app.cli.command('init-db')
def init_db():
    db.create_all()
    competences_default = [
        ('Algorithmique', 'Programmation'), ('Python', 'Programmation'),
        ('Java', 'Programmation'), ('JavaScript', 'Programmation'),
        ('HTML/CSS', 'Developpement Web'), ('SQL', 'Base de donnees'),
        ('Machine Learning', 'Intelligence Artificielle'),
        ('Reseaux', 'Systemes'), ('Linux', 'Systemes'),
        ('Mathematiques', 'Sciences'), ('Statistiques', 'Sciences'),
        ('Gestion de projet', 'Soft Skills'), ('Communication', 'Soft Skills')
    ]
    for nom, cat in competences_default:
        if not Competence.query.filter_by(nom=nom).first():
            db.session.add(Competence(nom=nom, categorie=cat))
    db.session.commit()
    print('Base de donnees initialisee !')

if __name__ == '__main__':
    app.run(debug=True)