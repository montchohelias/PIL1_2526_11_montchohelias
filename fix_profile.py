import os

templates_dir = r'H:\IFRI_MentorLink\templates'
os.makedirs(templates_dir, exist_ok=True)

template_profile = '''{% extends \"base.html\" %}

{% block title %}Mon Profil - MentorLink{% endblock %}

{% block content %}
<div class=\"page-header\">
    <h1><i class=\"fas fa-user-circle\"></i> Mon Profil</h1>
    <p>Gerez vos informations personnelles</p>
</div>

<div class=\"grid grid-2\">
    <div class=\"content-wrapper\" style=\"text-align: center;\">
        <div style=\"position: relative; display: inline-block; margin-bottom: 1.5rem;\">
            <div class=\"avatar\" style=\"width: 120px; height: 120px; font-size: 3rem; margin: 0 auto;\">
                {{ current_user.prenom[0] }}{{ current_user.nom[0] }}
            </div>
            <div style=\"position: absolute; bottom: 5px; right: 5px; width: 32px; height: 32px; 
                        background: var(--success); border-radius: 50%; display: flex; 
                        align-items: center; justify-content: center; color: white; 
                        border: 3px solid white; font-size: 0.8rem;\">
                <i class=\"fas fa-check\"></i>
            </div>
        </div>
        
        <h2 style=\"font-size: 1.5rem; font-weight: 700; color: var(--gray-800); margin-bottom: 0.25rem;\">
            {{ current_user.prenom }} {{ current_user.nom }}
        </h2>
        <p style=\"color: var(--gray-500); margin-bottom: 1rem;\">
            <i class=\"fas fa-graduation-cap\" style=\"color: var(--primary);\"></i> 
            {{ current_user.filiere }} - {{ current_user.niveau }}
        </p>
        
        <div style=\"display: flex; gap: 0.5rem; justify-content: center; margin-bottom: 1.5rem;\">
            {% if current_user.est_mentor %}
            <span class=\"status-badge\" style=\"background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: white;\">
                <i class=\"fas fa-chalkboard-teacher\"></i> Mentor
            </span>
            {% endif %}
            {% if current_user.est_mentore %}
            <span class=\"status-badge\" style=\"background: linear-gradient(135deg, var(--secondary), #f472b6); color: white;\">
                <i class=\"fas fa-user-graduate\"></i> Mentore
            </span>
            {% endif %}
        </div>
        
        <div style=\"background: var(--gray-50); border-radius: var(--radius); padding: 1rem; text-align: left;\">
            <h4 style=\"font-size: 0.9rem; color: var(--gray-600); margin-bottom: 0.5rem;\">
                <i class=\"fas fa-info-circle\"></i> Bio
            </h4>
            <p style=\"color: var(--gray-500); font-size: 0.95rem;\">
                {{ current_user.bio or \"Aucune bio renseignee.\" }}
            </p>
        </div>
        
        <div style=\"margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center;\">
            <div style=\"text-align: center; padding: 0.75rem; background: var(--gray-50); border-radius: var(--radius); flex: 1;\">
                <div style=\"font-size: 1.25rem; font-weight: 700; color: var(--primary);\">
                    {{ current_user.competences|length }}
                </div>
                <div style=\"font-size: 0.8rem; color: var(--gray-500);\">Competences</div>
            </div>
            <div style=\"text-align: center; padding: 0.75rem; background: var(--gray-50); border-radius: var(--radius); flex: 1;\">
                <div style=\"font-size: 1.25rem; font-weight: 700; color: var(--secondary);\">
                    {{ current_user.lacunes|length }}
                </div>
                <div style=\"font-size: 0.8rem; color: var(--gray-500);\">Lacunes</div>
            </div>
        </div>
    </div>

    <div class=\"content-wrapper\">
        <h2 style=\"font-size: 1.25rem; font-weight: 700; color: var(--gray-800); margin-bottom: 1.5rem;\">
            <i class=\"fas fa-edit\" style=\"color: var(--primary); margin-right: 0.5rem;\"></i>
            Modifier mon profil
        </h2>
        
        <form method=\"POST\" action=\"{{ url_for('profile') }}\">
            <div style=\"display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;\">
                <div class=\"form-group\">
                    <label class=\"form-label\">Nom</label>
                    <input type=\"text\" name=\"nom\" class=\"form-input\" value=\"{{ current_user.nom }}\" required>
                </div>
                
                <div class=\"form-group\">
                    <label class=\"form-label\">Prenom</label>
                    <input type=\"text\" name=\"prenom\" class=\"form-input\" value=\"{{ current_user.prenom }}\" required>
                </div>
            </div>
            
            <div class=\"form-group\">
                <label class=\"form-label\">Bio</label>
                <textarea name=\"bio\" class=\"form-textarea\" placeholder=\"Parlez-nous de vous...\">{{ current_user.bio or '' }}</textarea>
            </div>
            
            <div class=\"form-group\">
                <label class=\"form-label\">Mes competences</label>
                <div style=\"display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem; max-height: 150px; overflow-y: auto; padding: 0.5rem; border: 2px solid var(--gray-200); border-radius: var(--radius);\">
                    {% for comp in competences %}
                    <label style=\"display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem; cursor: pointer; border-radius: 4px; transition: all 0.2s;\">
                        <input type=\"checkbox\" name=\"competences\" value=\"{{ comp.id }}\" 
                               {% if comp in current_user.competences %}checked{% endif %}>
                        <span style=\"font-size: 0.9rem;\">{{ comp.nom }}</span>
                    </label>
                    {% endfor %}
                </div>
            </div>
            
            <div class=\"form-group\">
                <label class=\"form-label\">Mes lacunes</label>
                <div style=\"display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem; max-height: 150px; overflow-y: auto; padding: 0.5rem; border: 2px solid var(--gray-200); border-radius: var(--radius);\">
                    {% for comp in competences %}
                    <label style=\"display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem; cursor: pointer; border-radius: 4px; transition: all 0.2s;\">
                        <input type=\"checkbox\" name=\"lacunes\" value=\"{{ comp.id }}\" 
                               {% if comp in current_user.lacunes %}checked{% endif %}>
                        <span style=\"font-size: 0.9rem;\">{{ comp.nom }}</span>
                    </label>
                    {% endfor %}
                </div>
            </div>
            
            <div style=\"display: flex; gap: 1rem; margin-top: 1.5rem;\">
                <button type=\"submit\" class=\"btn btn-primary\" style=\"flex: 1;\">
                    <i class=\"fas fa-save\"></i> Enregistrer
                </button>
                <a href=\"{{ url_for('dashboard') }}\" class=\"btn btn-secondary\" style=\"flex: 1; text-decoration: none; text-align: center;\">
                    <i class=\"fas fa-times\"></i> Annuler
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
'''

filepath = os.path.join(templates_dir, 'profile.html')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(template_profile)

print('Fichier profile.html cree avec succes!')
