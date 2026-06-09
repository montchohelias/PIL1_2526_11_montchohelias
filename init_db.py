from app import app
from models import db, Competence

with app.app_context():
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
        existante = Competence.query.filter_by(nom=nom).first()
        if not existante:
            db.session.add(Competence(nom=nom, categorie=cat))
    
    db.session.commit()
    print('Base de donnees initialisee avec succes !')
