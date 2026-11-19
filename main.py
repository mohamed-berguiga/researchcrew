from crew import research_crew

# Version terminal de ResearchCrew (l'interface web est dans app.py)
sujet = input("📝 Sujet de recherche : ")

for evenement in research_crew(sujet):
    type_ = evenement[0]

    if type_ == "debut":
        _, agent, detail = evenement
        print(f"\n🤖 [{agent}] {detail}...")

    elif type_ == "plan":
        print("\n📋 Questions à traiter :")
        for q in evenement[1]:
            print("  -", q)

    elif type_ == "critique":
        _, tour, critiques, approuve = evenement
        if approuve:
            print("\n✅ Le Critique a approuvé le rapport !")
        else:
            print(f"\n🔁 Version {tour} : le Critique demande des corrections :")
            print(critiques)

    elif type_ == "fin":
        _, rapport, approuve = evenement
        if not approuve:
            print("\n⚠️ Nombre maximum de révisions atteint : on garde la dernière version.")
        with open("rapport.md", "w", encoding="utf-8") as f:
            f.write(rapport)
        print("\n📄 Rapport final enregistré dans rapport.md")
