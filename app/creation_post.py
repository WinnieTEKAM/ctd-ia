import edsnlp

# Chargement du modèle EDS-NLP
nlp = edsnlp.blank("fr")
nlp.add_pipe("eds.sentences")
nlp.add_pipe("eds.normalizer")
nlp.add_pipe("eds.dates")
nlp.add_pipe("eds.matcher", config={"terms": {}})

def extraire_infos(texte: str) -> dict:
    """Extrait les informations clés du texte médical"""
    doc = nlp(texte)
    
    # Récupère les entités détectées (dates, termes médicaux...)
    entites = [{"texte": ent.text, "type": ent.label_} for ent in doc.ents]
    
    return {
        "texte_original": texte,
        "entites_detectees": entites,
        "mots_cles": [ent.text for ent in doc.ents],
        "specialite": "à détecter",
        "titre": "à générer",
        "resume": "à générer"
    }
