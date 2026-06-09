from models import User, Competence, Matching, Offre, db
import json

class MatchingAlgorithm:
    """
    Algorithme de matching base sur :
    - Compatibilite competences (40%)
    - Compatibilite horaires (35%)
    - Proximite filieres (25%)
    """
    
    def __init__(self):
        self.poids_competences = 0.40
        self.poids_horaires = 0.35
        self.poids_filiere = 0.25
    
    def calculer_score_competences(self, mentor, mentore):
        competences_mentor = set(c.id for c in mentor.competences)
        lacunes_mentore = set(l.id for l in mentore.lacunes)
        
        if not lacunes_mentore:
            return 0.0
        
        intersection = competences_mentor.intersection(lacunes_mentore)
        score = len(intersection) / len(lacunes_mentore)
        return min(score, 1.0)
    
    def calculer_score_horaires(self, dispo_mentor, dispo_mentore):
        if not dispo_mentor or not dispo_mentore:
            return 0.0
        
        total_creneaux_mentor = 0
        total_creneaux_communs = 0
        
        for jour, creneaux in dispo_mentor.items():
            if jour in dispo_mentore:
                mentor_creneaux = set(creneaux)
                mentore_creneaux = set(dispo_mentore[jour])
                communs = mentor_creneaux.intersection(mentore_creneaux)
                total_creneaux_mentor += len(mentor_creneaux)
                total_creneaux_communs += len(communs)
        
        if total_creneaux_mentor == 0:
            return 0.0
        return min(total_creneaux_communs / total_creneaux_mentor, 1.0)
    
    def calculer_score_filiere(self, mentor, mentore):
        filieres_proches = {
            'IA': ['IM', 'SI'],
            'IM': ['IA', 'SI', 'GL'],
            'GL': ['IM', 'SI', 'SE&IoT'],
            'SE&IoT': ['GL', 'SI'],
            'SI': ['IA', 'IM', 'GL', 'SE&IoT']
        }
        
        score = 0.0
        if mentor.filiere == mentore.filiere:
            score += 0.6
        elif mentore.filiere in filieres_proches.get(mentor.filiere, []):
            score += 0.3
        
        niveaux = {'L1': 1, 'L2': 2, 'L3': 3, 'M1': 4, 'M2': 5}
        niv_mentor = niveaux.get(mentor.niveau, 0)
        niv_mentore = niveaux.get(mentore.niveau, 0)
        
        if niv_mentor > niv_mentore:
            score += 0.4
        elif niv_mentor == niv_mentore:
            score += 0.2
        
        return min(score, 1.0)
    
    def trouver_matchings(self, offre_demande, limite=10):
        results = []
        
        if offre_demande.type_offre == 'demande':
            mentors = User.query.filter(User.est_mentor == True, User.id != offre_demande.user_id).all()
            for mentor in mentors:
                score_comp = self.calculer_score_competences(mentor, offre_demande.auteur)
                score_horaire = self.calculer_score_horaires(
                    mentor.get_disponibilites(), offre_demande.auteur.get_disponibilites()
                )
                score_filiere = self.calculer_score_filiere(mentor, offre_demande.auteur)
                score_total = (score_comp * self.poids_competences + 
                             score_horaire * self.poids_horaires + 
                             score_filiere * self.poids_filiere)
                
                if score_total > 0.2:
                    results.append({
                        'user': mentor,
                        'score': round(score_total * 100, 1),
                        'details': {
                            'competences': round(score_comp * 100, 1),
                            'horaires': round(score_horaire * 100, 1),
                            'filiere': round(score_filiere * 100, 1)
                        }
                    })
        else:
            mentores = User.query.filter(User.est_mentore == True, User.id != offre_demande.user_id).all()
            for mentore in mentores:
                score_comp = self.calculer_score_competences(offre_demande.auteur, mentore)
                score_horaire = self.calculer_score_horaires(
                    offre_demande.auteur.get_disponibilites(), mentore.get_disponibilites()
                )
                score_filiere = self.calculer_score_filiere(offre_demande.auteur, mentore)
                score_total = (score_comp * self.poids_competences + 
                             score_horaire * self.poids_horaires + 
                             score_filiere * self.poids_filiere)
                
                if score_total > 0.2:
                    results.append({
                        'user': mentore,
                        'score': round(score_total * 100, 1),
                        'details': {
                            'competences': round(score_comp * 100, 1),
                            'horaires': round(score_horaire * 100, 1),
                            'filiere': round(score_filiere * 100, 1)
                        }
                    })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limite]
