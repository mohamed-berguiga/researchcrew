from agents import Agent

MAX_REVISIONS = 2  # garde-fou : nombre maximum de corrections

# ---------- Les agents ----------
planificateur = Agent(
    "Planificateur",
    "Tu découpes un sujet de recherche en exactement 3 sous-questions précises. "
    "Réponds UNIQUEMENT avec les 3 questions, une par ligne, sans introduction ni conclusion.",
)

chercheur = Agent(
    "Chercheur",
    "Tu es un chercheur rigoureux. Réponds à la question avec des faits clairs, "
    "en 100 mots maximum. Si tu n'es pas sûr d'une information, dis-le.",
)

redacteur = Agent(
    "Rédacteur",
    "Tu rédiges un rapport en français, en Markdown, à partir de notes de recherche. "
    "Structure : un titre, une introduction, une section par question, une conclusion. "
    "Si des critiques sont fournies, corrige le rapport en en tenant compte.",
)

critique = Agent(
    "Critique",
    "Tu es un relecteur exigeant mais juste. Tu relis un rapport. "
    "S'il est clair, bien structuré et cohérent, réponds seulement : APPROUVÉ. "
    "Sinon, donne au maximum 3 corrections précises, en liste.",
)


# ---------- Fonction utilitaire ----------
def extraire_questions(texte):
    questions = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        ligne = ligne.lstrip("0123456789.-*) ")
        if ligne.endswith("?"):
            questions.append(ligne)
    return questions[:3]


# ---------- Le pipeline ----------
def research_crew(sujet, max_revisions=MAX_REVISIONS):
    """Fait travailler l'équipe d'agents sur un sujet.

    C'est un *générateur* : au lieu de tout renvoyer à la fin, il envoie
    (avec `yield`) un événement à chaque étape. Le terminal (main.py) et
    l'interface web (app.py) affichent ces événements chacun à leur façon.
    """
    # Étape A : planification
    yield ("debut", "Planificateur", "Découpage du sujet en sous-questions")
    plan = planificateur.run(f"Sujet : {sujet}")
    questions = extraire_questions(plan)
    yield ("plan", questions)

    # Étape B : recherche
    notes = ""
    for q in questions:
        yield ("debut", "Chercheur", q)
        reponse = chercheur.run(q)
        notes += f"\n## {q}\n{reponse}\n"
        yield ("recherche", q, reponse)

    # Étape C : rédaction + boucle de critique
    critiques = "Aucune pour l'instant."
    approuve = False
    for tour in range(1, max_revisions + 2):
        yield ("debut", "Rédacteur", f"Rédaction — version {tour}")
        rapport = redacteur.run(
            f"Sujet : {sujet}\n\n"
            f"Notes de recherche :\n{notes}\n\n"
            f"Critiques à prendre en compte :\n{critiques}"
        )

        yield ("debut", "Critique", f"Relecture — version {tour}")
        critiques = critique.run(f"Voici le rapport à relire :\n\n{rapport}")
        approuve = "APPROUV" in critiques.upper()
        yield ("critique", tour, critiques, approuve)
        if approuve:
            break

    yield ("fin", rapport, approuve)
