# Script pour créer les templates HTML
import os

# Contenu du template base.html
template_base = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}MentorLink IFRI{% endblock %}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #818cf8;
            --secondary: #ec4899;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1e293b;
            --gray-50: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-300: #cbd5e1;
            --gray-400: #94a3b8;
            --gray-500: #64748b;
            --gray-600: #475569;
            --gray-700: #334155;
            --gray-800: #1e293b;
            --gray-900: #0f172a;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
            --radius: 12px;
            --radius-sm: 8px;
            --radius-lg: 16px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: var(--gray-800);
            line-height: 1.6;
        }
        .app-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            overflow: hidden;
        }
        .card {
            background: white;
            border-radius: var(--radius);
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-100);
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--radius-lg);
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 20px;
            z-index: 100;
        }
        .nav-brand {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .nav-links {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .nav-link {
            padding: 0.5rem 1rem;
            border-radius: var(--radius-sm);
            text-decoration: none;
            color: var(--gray-600);
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            position: relative;
        }
        .nav-link:hover {
            background: var(--gray-100);
            color: var(--primary);
        }
        .nav-link.active {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
        }
        .nav-link .badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: var(--danger);
            color: white;
            font-size: 0.7rem;
            padding: 0.15rem 0.4rem;
            border-radius: 10px;
            font-weight: 600;
        }
        .btn {
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-sm);
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
            font-size: 0.95rem;
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }
        .btn-secondary {
            background: var(--gray-100);
            color: var(--gray-700);
        }
        .btn-secondary:hover {
            background: var(--gray-200);
        }
        .btn-success {
            background: linear-gradient(135deg, var(--success), #059669);
            color: white;
        }
        .btn-danger {
            background: linear-gradient(135deg, var(--danger), #dc2626);
            color: white;
        }
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--gray-700);
        }
        .form-input, .form-select, .form-textarea {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-sm);
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            background: white;
        }
        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        .form-textarea {
            resize: vertical;
            min-height: 120px;
        }
        .grid {
            display: grid;
            gap: 1.5rem;
        }
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
        }
        .alert {
            padding: 1rem 1.5rem;
            border-radius: var(--radius-sm);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 500;
        }
        .alert-success {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #a7f3d0;
        }
        .alert-danger {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        .alert-warning {
            background: #fef3c7;
            color: #92400e;
            border: 1px solid #fde68a;
        }
        .avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            flex-shrink: 0;
        }
        .avatar-lg {
            width: 64px;
            height: 64px;
            font-size: 1.5rem;
        }
        .avatar-sm {
            width: 36px;
            height: 36px;
            font-size: 0.9rem;
        }
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        .status-online {
            background: #d1fae5;
            color: #065f46;
        }
        .status-offline {
            background: var(--gray-100);
            color: var(--gray-500);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .slide-in {
            animation: slideIn 0.3s ease forwards;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .typing-indicator {
            display: flex;
            gap: 0.25rem;
            padding: 0.5rem 1rem;
        }
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: var(--gray-400);
            border-radius: 50%;
            animation: pulse 1.4s infinite;
        }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--gray-300);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--gray-400);
        }
        .page-header {
            margin-bottom: 2rem;
        }
        .page-header h1 {
            font-size: 2rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .page-header p {
            color: rgba(255,255,255,0.8);
            font-size: 1.1rem;
        }
        .content-wrapper {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--radius-lg);
            padding: 2rem;
            box-shadow: var(--shadow-xl);
        }
        @media (max-width: 768px) {
            .app-container {
                padding: 10px;
            }
            .navbar {
                flex-direction: column;
                gap: 1rem;
                padding: 1rem;
            }
            .nav-links {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if current_user.is_authenticated %}
    <nav class="navbar">
        <div class="nav-brand">
            <i class="fas fa-graduation-cap"></i>
            MentorLink
        </div>
        <div class="nav-links">
            <a href="{{ url_for('dashboard') }}" class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}">
                <i class="fas fa-home"></i> Tableau de bord
            </a>
            <a href="{{ url_for('messages_list') }}" class="nav-link {% if request.endpoint == 'messages_list' or request.endpoint == 'messages' %}active{% endif %}">
                <i class="fas fa-comments"></i> Messages
                <span class="badge" id="msg-badge" style="display: none;">0</span>
            </a>
            <a href="{{ url_for('profile') }}" class="nav-link {% if request.endpoint == 'profile' %}active{% endif %}">
                <i class="fas fa-user"></i> Profil
            </a>
            <a href="{{ url_for('logout') }}" class="nav-link">
                <i class="fas fa-sign-out-alt"></i> Deconnexion
            </a>
        </div>
    </nav>
    {% endif %}

    <div class="app-container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} fade-in">
                        <i class="fas fa-{% if category == 'success' %}check-circle{% elif category == 'danger' %}exclamation-circle{% else %}info-circle{% endif %}"></i>
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script>
        {% if current_user.is_authenticated %}
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connecte au serveur');
        });
        
        socket.on('notification', function(data) {
            showToast(data.message, data.contenu);
            
            const badge = document.getElementById('msg-badge');
            if (badge) {
                badge.style.display = 'inline';
                let count = parseInt(badge.textContent) || 0;
                badge.textContent = count + 1;
            }
        });
        
        function showToast(title, message) {
            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                z-index: 1000;
                max-width: 300px;
                animation: slideIn 0.3s ease;
                border-left: 4px solid var(--primary);
            `;
            toast.innerHTML = `
                <div style="font-weight: 600; color: var(--gray-800); margin-bottom: 0.25rem;">${title}</div>
                <div style="color: var(--gray-500); font-size: 0.9rem;">${message}</div>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 5000);
        }
        {% endif %}
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
"""
template_dashboard = """{% extends "base.html" %}

{% block title %}Tableau de bord - MentorLink{% endblock %}

{% block content %}
<div class="page-header">
    <h1><i class="fas fa-home"></i> Tableau de bord</h1>
    <p>Bienvenue, {{ current_user.prenom }} ! Voici votre espace personnel.</p>
</div>

<div class="grid grid-3">
    <div class="glass-card" style="padding: 1.5rem; text-align: center;">
        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 0.5rem;">
            <i class="fas fa-handshake"></i>
        </div>
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--gray-800);">
            {{ matchings|length }}
        </div>
        <div style="color: var(--gray-500);">Matchings</div>
    </div>
    
    <div class="glass-card" style="padding: 1.5rem; text-align: center;">
        <div style="font-size: 2.5rem; color: var(--secondary); margin-bottom: 0.5rem;">
            <i class="fas fa-bullhorn"></i>
        </div>
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--gray-800);">
            {{ offres|length }}
        </div>
        <div style="color: var(--gray-500);">Offres publiees</div>
    </div>
    
    <div class="glass-card" style="padding: 1.5rem; text-align: center;">
        <div style="font-size: 2.5rem; color: var(--success); margin-bottom: 0.5rem;">
            <i class="fas fa-comments"></i>
        </div>
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--gray-800);">
            {{ conversations|length }}
        </div>
        <div style="color: var(--gray-500);">Conversations</div>
    </div>
</div>

<div class="grid grid-2" style="margin-top: 2rem;">
    <div class="content-wrapper">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.25rem; font-weight: 700; color: var(--gray-800);">
                <i class="fas fa-bullhorn" style="color: var(--primary); margin-right: 0.5rem;"></i>
                Mes Offres
            </h2>
            <button onclick="document.getElementById('modal-offre').style.display='flex'" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Nouvelle offre
            </button>
        </div>
        
        {% if offres %}
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            {% for offre in offres %}
            <div class="card" style="padding: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <div>
                        <span class="status-badge" style="background: {% if offre.type_offre == 'demande' %}#fef3c7; color: #92400e;{% else %}#d1fae5; color: #065f46;{% endif %} margin-bottom: 0.5rem;">
                            {{ offre.type_offre|capitalize }}
                        </span>
                        <h3 style="font-weight: 600; color: var(--gray-800); margin-top: 0.5rem;">{{ offre.titre }}</h3>
                    </div>
                    <a href="{{ url_for('matching', offre_id=offre.id) }}" class="btn btn-primary btn-sm">
                        <i class="fas fa-search"></i> Matching
                    </a>
                </div>
                <p style="color: var(--gray-500); font-size: 0.9rem; margin-bottom: 0.75rem;">{{ offre.description[:100] }}...</p>
                <div style="display: flex; gap: 0.5rem; font-size: 0.85rem; color: var(--gray-400);">
                    <span><i class="fas fa-calendar"></i> {{ offre.created_at.strftime('%d/%m/%Y') }}</span>
                    <span><i class="fas fa-tag"></i> {{ offre.format_session }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div style="text-align: center; padding: 2rem; color: var(--gray-400);">
            <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem;"></i>
            <p>Aucune offre pour le moment</p>
        </div>
        {% endif %}
    </div>
    
    <div class="content-wrapper">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: var(--gray-800); margin-bottom: 1.5rem;">
            <i class="fas fa-handshake" style="color: var(--secondary); margin-right: 0.5rem;"></i>
            Mes Matchings
        </h2>
        
        {% if matchings %}
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            {% for matching in matchings %}
            <div class="card" style="padding: 1.25rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div class="avatar">
                        {% if current_user.id == matching.mentor_id %}
                            {{ matching.mentore.prenom[0] }}{{ matching.mentore.nom[0] }}
                        {% else %}
                            {{ matching.mentor.prenom[0] }}{{ matching.mentor.nom[0] }}
                        {% endif %}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: var(--gray-800);">
                            {% if current_user.id == matching.mentor_id %}
                                {{ matching.mentore.prenom }} {{ matching.mentore.nom }}
                            {% else %}
                                {{ matching.mentor.prenom }} {{ matching.mentor.nom }}
                            {% endif %}
                        </div>
                        <div style="font-size: 0.85rem; color: var(--gray-500);">
                            Score: <span style="color: var(--primary); font-weight: 600;">{{ matching.score_matching }}%</span>
                        </div>
                    </div>
                    <span class="status-badge" style="background: {% if matching.statut == 'accepte' %}#d1fae5; color: #065f46;{% elif matching.statut == 'propose' %}#fef3c7; color: #92400e;{% else %}#fee2e2; color: #991b1b;{% endif %}">
                        {{ matching.statut|capitalize }}
                    </span>
                </div>
                
                {% if matching.statut == 'propose' %}
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                    <form action="{{ url_for('accepter_matching', matching_id=matching.id) }}" method="POST" style="flex: 1;">
                        <button type="submit" class="btn btn-success btn-sm" style="width: 100%;">
                            <i class="fas fa-check"></i> Accepter
                        </button>
                    </form>
                    <button class="btn btn-danger btn-sm" style="flex: 1;">
                        <i class="fas fa-times"></i> Refuser
                    </button>
                </div>
                {% elif matching.statut == 'accepte' %}
                <a href="{{ url_for('messages', conversation_id=matching.conversation.id) }}" class="btn btn-primary btn-sm" style="margin-top: 1rem; width: 100%; text-align: center; text-decoration: none;">
                    <i class="fas fa-comments"></i> Discuter
                </a>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div style="text-align: center; padding: 2rem; color: var(--gray-400);">
            <i class="fas fa-handshake" style="font-size: 3rem; margin-bottom: 1rem;"></i>
            <p>Aucun matching pour le moment</p>
        </div>
        {% endif %}
    </div>
</div>

<div id="modal-offre" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
    <div class="glass-card" style="width: 90%; max-width: 500px; padding: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h2 style="font-weight: 700; color: var(--gray-800);">Nouvelle Offre</h2>
            <button onclick="document.getElementById('modal-offre').style.display='none'" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--gray-400);">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <form action="{{ url_for('nouvelle_offre') }}" method="POST">
            <div class="form-group">
                <label class="form-label">Type d'offre</label>
                <select name="type_offre" class="form-select" required>
                    <option value="demande">Demande de mentorat</option>
                    <option value="proposition">Proposition de mentorat</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">Titre</label>
                <input type="text" name="titre" class="form-input" placeholder="Ex: Aide en Python" required>
            </div>
            
            <div class="form-group">
                <label class="form-label">Description</label>
                <textarea name="description" class="form-textarea" placeholder="Decrivez votre besoin ou votre offre..." required></textarea>
            </div>
            
            <div class="form-group">
                <label class="form-label">Competence concernee</label>
                <select name="competence_id" class="form-select">
                    <option value="">-- Selectionner --</option>
                    {% for comp in competences %}
                    <option value="{{ comp.id }}">{{ comp.nom }} ({{ comp.categorie }})</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">Format de session</label>
                <select name="format_session" class="form-select" required>
                    <option value="presentiel">Presentiel</option>
                    <option value="distance">Distance</option>
                    <option value="les_deux">Les deux</option>
                </select>
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%;">
                <i class="fas fa-paper-plane"></i> Publier l'offre
            </button>
        </form>
    </div>
</div>
{% endblock %}
"""

template_messages_list = """{% extends "base.html" %}

{% block title %}Messages - MentorLink{% endblock %}

{% block content %}
<div class="page-header">
    <h1><i class="fas fa-comments"></i> Messagerie</h1>
    <p>Discutez avec vos mentors et mentores</p>
</div>

<div class="content-wrapper">
    {% if conversations %}
    <div style="display: flex; flex-direction: column; gap: 1rem;">
        {% for conv_data in conversations %}
        <a href="{{ url_for('messages', conversation_id=conv_data.conversation.id) }}" 
           class="conversation-card card" 
           style="display: flex; align-items: center; gap: 1rem; padding: 1.25rem; text-decoration: none; color: inherit;">
            
            <div class="avatar avatar-lg">
                {{ conv_data.other_user.prenom[0] }}{{ conv_data.other_user.nom[0] }}
            </div>
            
            <div style="flex: 1; min-width: 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <h3 style="font-weight: 600; color: var(--gray-800);">
                        {{ conv_data.other_user.prenom }} {{ conv_data.other_user.nom }}
                        <span class="status-badge status-online" style="margin-left: 0.5rem;">
                            <i class="fas fa-circle" style="font-size: 0.5rem;"></i> En ligne
                        </span>
                    </h3>
                    <span style="color: var(--gray-400); font-size: 0.85rem;">
                        {% if conv_data.last_message %}
                            {{ conv_data.last_message.created_at.strftime('%H:%M') }}
                        {% endif %}
                    </span>
                </div>
                
                <p style="color: var(--gray-500); font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {% if conv_data.last_message %}
                        {% if conv_data.last_message.expediteur_id == current_user.id %}
                            <span style="color: var(--primary); font-weight: 500;">Vous:</span>
                        {% endif %}
                        {{ conv_data.last_message.contenu }}
                    {% else %}
                        <em>Aucun message encore. Commencez la conversation !</em>
                    {% endif %}
                </p>
            </div>
            
            {% if conv_data.unread_count > 0 %}
            <div style="background: linear-gradient(135deg, var(--danger), #dc2626); color: white; 
                        width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; font-weight: 700; font-size: 0.8rem; flex-shrink: 0;">
                {{ conv_data.unread_count }}
            </div>
            {% endif %}
            
            <i class="fas fa-chevron-right" style="color: var(--gray-300);"></i>
        </a>
        {% endfor %}
    </div>
    {% else %}
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; color: var(--gray-300); margin-bottom: 1rem;">
            <i class="fas fa-inbox"></i>
        </div>
        <h3 style="color: var(--gray-600); margin-bottom: 0.5rem;">Aucune conversation</h3>
        <p style="color: var(--gray-400);">Acceptez un matching pour commencer a discuter.</p>
        <a href="{{ url_for('dashboard') }}" class="btn btn-primary" style="margin-top: 1rem;">
            <i class="fas fa-arrow-left"></i> Retour au tableau de bord
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}
"""

template_messages = """{% extends "base.html" %}

{% block title %}Chat avec {{ other_user.prenom }} - MentorLink{% endblock %}

{% block extra_css %}
<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 200px);
        min-height: 500px;
    }
    .chat-header {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--gray-200);
        display: flex;
        align-items: center;
        gap: 1rem;
        background: white;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        background: var(--gray-50);
    }
    .message {
        display: flex;
        gap: 0.75rem;
        max-width: 70%;
        animation: fadeIn 0.3s ease;
    }
    .message.sent {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    .message.received {
        align-self: flex-start;
    }
    .message-content {
        padding: 0.875rem 1.25rem;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .message.sent .message-content {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border-bottom-right-radius: 4px;
    }
    .message.received .message-content {
        background: white;
        color: var(--gray-800);
        border-bottom-left-radius: 4px;
        box-shadow: var(--shadow-sm);
    }
    .message-time {
        font-size: 0.75rem;
        color: var(--gray-400);
        margin-top: 0.25rem;
        text-align: right;
    }
    .message.received .message-time {
        text-align: left;
    }
    .chat-input-area {
        padding: 1rem 1.5rem;
        border-top: 1px solid var(--gray-200);
        background: white;
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .chat-input {
        flex: 1;
        padding: 0.875rem 1.25rem;
        border: 2px solid var(--gray-200);
        border-radius: 24px;
        font-family: inherit;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        resize: none;
        max-height: 120px;
    }
    .chat-input:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    .btn-send {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }
    .btn-send:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    .typing-status {
        padding: 0.5rem 1.5rem;
        color: var(--gray-400);
        font-size: 0.85rem;
        font-style: italic;
        min-height: 30px;
    }
</style>
{% endblock %}

{% block content %}
<div class="content-wrapper" style="padding: 0; overflow: hidden;">
    <div class="chat-container">
        <div class="chat-header">
            <a href="{{ url_for('messages_list') }}" class="btn btn-secondary btn-sm" style="text-decoration: none;">
                <i class="fas fa-arrow-left"></i>
            </a>
            <div class="avatar">
                {{ other_user.prenom[0] }}{{ other_user.nom[0] }}
            </div>
            <div>
                <div style="font-weight: 600; color: var(--gray-800);">
                    {{ other_user.prenom }} {{ other_user.nom }}
                </div>
                <div style="font-size: 0.85rem; color: var(--gray-400);">
                    {{ other_user.filiere }} - {{ other_user.niveau }}
                </div>
            </div>
            <div style="margin-left: auto;">
                <span class="status-badge status-online">
                    <i class="fas fa-circle" style="font-size: 0.5rem;"></i> En ligne
                </span>
            </div>
        </div>
        
        <div class="chat-messages" id="chat-messages">
            {% for msg in messages %}
                {% if msg.expediteur_id == current_user.id %}
                <div class="message sent" data-message-id="{{ msg.id }}">
                    <div class="avatar avatar-sm" style="background: linear-gradient(135deg, var(--success), #059669);">
                        {{ current_user.prenom[0] }}{{ current_user.nom[0] }}
                    </div>
                    <div>
                        <div class="message-content">{{ msg.contenu }}</div>
                        <div class="message-time">
                            {{ msg.created_at.strftime('%H:%M') }}
                            <i class="fas fa-check-double" style="margin-left: 0.25rem; color: var(--primary-light);"></i>
                        </div>
                    </div>
                </div>
                {% else %}
                <div class="message received" data-message-id="{{ msg.id }}">
                    <div class="avatar avatar-sm">
                        {{ other_user.prenom[0] }}{{ other_user.nom[0] }}
                    </div>
                    <div>
                        <div class="message-content">{{ msg.contenu }}</div>
                        <div class="message-time">{{ msg.created_at.strftime('%H:%M') }}</div>
                    </div>
                </div>
                {% endif %}
            {% endfor %}
            
            <div class="typing-status" id="typing-status"></div>
        </div>
        
        <div class="chat-input-area">
            <textarea class="chat-input" id="message-input" placeholder="Ecrivez votre message..." rows="1"></textarea>
            <button class="btn-send" id="btn-send">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    const conversationId = {{ conversation.id }};
    const currentUserId = {{ current_user.id }};
    
    socket.emit('join_conversation', { conversation_id: conversationId });
    
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    function sendMessage() {
        const input = document.getElementById('message-input');
        const contenu = input.value.trim();
        
        if (!contenu) return;
        
        socket.emit('send_message', {
            conversation_id: conversationId,
            contenu: contenu
        });
        
        input.value = '';
        input.style.height = 'auto';
    }
    
    document.getElementById('btn-send').addEventListener('click', sendMessage);
    
    document.getElementById('message-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    document.getElementById('message-input').addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        socket.emit('typing', { conversation_id: conversationId });
    });
    
    socket.on('new_message', function(data) {
        const isSent = data.expediteur_id === currentUserId;
        const messageHtml = `
            <div class="message ${isSent ? 'sent' : 'received'} slide-in">
                <div class="avatar avatar-sm" style="${isSent ? 'background: linear-gradient(135deg, var(--success), #059669);' : ''}">
                    ${isSent ? '{{ current_user.prenom[0] }}{{ current_user.nom[0] }}' : '{{ other_user.prenom[0] }}{{ other_user.nom[0] }}'}
                </div>
                <div>
                    <div class="message-content">${escapeHtml(data.contenu)}</div>
                    <div class="message-time">
                        ${data.created_at}
                        ${isSent ? '<i class="fas fa-check" style="margin-left: 0.25rem; color: var(--primary-light);"></i>' : ''}
                    </div>
                </div>
            </div>
        `;
        
        const typingStatus = document.getElementById('typing-status');
        typingStatus.textContent = '';
        
        typingStatus.insertAdjacentHTML('beforebegin', messageHtml);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
    
    let typingTimeout;
    socket.on('user_typing', function(data) {
        if (data.user_id !== currentUserId) {
            const typingStatus = document.getElementById('typing-status');
            typingStatus.textContent = data.user_name + ' est en train d\\'ecrire...';
            
            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(() => {
                typingStatus.textContent = '';
            }, 3000);
        }
    });
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    socket.on('error', function(data) {
        console.error('Erreur Socket.IO:', data.message);
    });
</script>
{% endblock %}
"""

template_login = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion - MentorLink IFRI</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --gray-50: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-300: #cbd5e1;
            --gray-400: #94a3b8;
            --gray-500: #64748b;
            --gray-600: #475569;
            --gray-700: #334155;
            --gray-800: #1e293b;
            --radius: 12px;
            --radius-lg: 16px;
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-container {
            width: 100%;
            max-width: 420px;
        }
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--radius-lg);
            padding: 2.5rem;
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            color: white;
            font-size: 2.5rem;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
        }
        .logo h1 {
            font-size: 1.75rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo p {
            color: var(--gray-500);
            margin-top: 0.5rem;
            font-size: 0.95rem;
        }
        .form-group {
            margin-bottom: 1.25rem;
        }
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--gray-700);
            font-size: 0.9rem;
        }
        .input-group {
            position: relative;
        }
        .input-group i {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray-400);
            font-size: 1rem;
        }
        .form-input {
            width: 100%;
            padding: 0.875rem 1rem 0.875rem 2.75rem;
            border: 2px solid var(--gray-200);
            border-radius: var(--radius);
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            background: white;
        }
        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        .btn {
            width: 100%;
            padding: 1rem;
            border-radius: var(--radius);
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-size: 1rem;
            font-family: inherit;
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }
        .divider {
            display: flex;
            align-items: center;
            margin: 1.5rem 0;
            color: var(--gray-400);
            font-size: 0.85rem;
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--gray-200);
        }
        .divider span {
            padding: 0 1rem;
        }
        .register-link {
            text-align: center;
            margin-top: 1.5rem;
            color: var(--gray-500);
            font-size: 0.95rem;
        }
        .register-link a {
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
        }
        .register-link a:hover {
            text-decoration: underline;
        }
        .alert {
            padding: 1rem;
            border-radius: var(--radius);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.9rem;
        }
        .alert-danger {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-card fade-in">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <h1>MentorLink</h1>
                <p>Plateforme de mentorat IFRI</p>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            <i class="fas fa-exclamation-circle"></i>
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <form method="POST" action="{{ url_for('login') }}">
                <div class="form-group">
                    <label class="form-label">Email ou Telephone</label>
                    <div class="input-group">
                        <i class="fas fa-user"></i>
                        <input type="text" name="identifiant" class="form-input" placeholder="votre@email.com" required>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Mot de passe</label>
                    <div class="input-group">
                        <i class="fas fa-lock"></i>
                        <input type="password" name="password" class="form-input" placeholder="••••••••" required>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-sign-in-alt"></i> Se connecter
                </button>
            </form>

            <div class="divider">
                <span>ou</span>
            </div>

            <div class="register-link">
                Pas encore de compte ? <a href="{{ url_for('register') }}">S'inscrire</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Creer le dossier templates
templates_dir = r'H:\IFRI_MentorLink\templates'
os.makedirs(templates_dir, exist_ok=True)

# Ecrire les fichiers
files = {
    'base.html': template_base,
    'login.html': template_login,
    'dashboard.html': template_dashboard,
    'messages_list.html': template_messages_list,
    'messages.html': template_messages,
    'profile.html': template_profile,
}
for filename, content in files.items():
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fichier cree: {filename}')

print('\nTous les templates ont ete crees avec succes!')