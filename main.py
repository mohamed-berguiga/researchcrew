from agents import Agent

MAX_REVISIONS = 2  # 🆕 garde-fou : nombre maximum de corrections

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

# 🆕 Rédacteur
redacteur = Agent(
    "Rédacteur",
    "Tu rédiges un rapport en français, en Markdown, à partir de notes de recherche. "
    "Structure : un titre, une introduction, une section par question, une conclusion. "
    "Si des critiques sont fournies, corrige le rapport en en tenant compte.",
)

# 🆕 Critique
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


# ---------- Le programme ----------
sujet = input("📝 Sujet de recherche : ")

# Étape A : planification
plan = planificateur.run(f"Sujet : {sujet}")
questions = extraire_questions(plan)

print("\n📋 Questions à traiter :")
for q in questions:
    print("  -", q)

# Étape B : recherche
notes = ""
for q in questions:
    reponse = chercheur.run(q)
    notes += f"\n## {q}\n{reponse}\n"

# 🆕 Étape C : rédaction + boucle de critique
critiques = "Aucune pour l'instant."

for tour in range(MAX_REVISIONS + 1):
    rapport = redacteur.run(
        f"Sujet : {sujet}\n\n"
        f"Notes de recherche :\n{notes}\n\n"
        f"Critiques à prendre en compte :\n{critiques}"
    )

    critiques = critique.run(f"Voici le rapport à relire :\n\n{rapport}")

    if "APPROUV" in critiques.upper():   # accepte "Approuvé", "APPROUVE"...
        print("\n✅ Le Critique a approuvé le rapport !")
        break
    else:
        print(f"\n🔁 Tour {tour + 1} : le Critique demande des corrections :")
        print(critiques)
else:
    print("\n⚠️ Nombre maximum de révisions atteint : on garde la dernière version.")

# 🆕 Étape D : sauvegarde
with open("rapport.md", "w", encoding="utf-8") as f:
    f.write(rapport)

print("\n📄 Rapport final enregistré dans rapport.md")