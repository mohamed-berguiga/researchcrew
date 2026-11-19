import ollama
import streamlit as st

import agents
from crew import MAX_REVISIONS, research_crew

ICONES = {"Planificateur": "🧭", "Chercheur": "🔎", "Rédacteur": "✍️", "Critique": "🧐"}

st.set_page_config(page_title="ResearchCrew", page_icon="🤖", layout="wide")


# ---------- Barre latérale : réglages ----------
def modeles_installes():
    try:
        return [m.model for m in ollama.list().models]
    except Exception:
        return []


with st.sidebar:
    st.header("⚙️ Réglages")
    modeles = modeles_installes()
    if not modeles:
        st.error("Ollama ne répond pas. Lance Ollama puis recharge la page.")
        st.stop()
    defaut = next((i for i, m in enumerate(modeles) if m.startswith(agents.MODEL)), 0)
    agents.MODEL = st.selectbox("Modèle", modeles, index=defaut)
    max_revisions = st.slider("Révisions maximum", 0, 4, MAX_REVISIONS,
                              help="Garde-fou : nombre de fois où le Critique peut demander des corrections.")
    st.divider()
    st.markdown("**L'équipe**")
    st.markdown(
        "🧭 **Planificateur** — découpe le sujet\n\n"
        "🔎 **Chercheur** — répond aux questions\n\n"
        "✍️ **Rédacteur** — écrit le rapport\n\n"
        "🧐 **Critique** — relit et fait corriger"
    )
    st.caption("100 % local avec Ollama — aucune donnée n'est envoyée sur Internet.")


# ---------- Page principale ----------
st.title("🤖 ResearchCrew")
st.write("Une équipe de **4 agents IA** qui produit un rapport de recherche à partir d'un simple sujet.")

with st.form("formulaire"):
    sujet = st.text_input("📝 Sujet de recherche", placeholder="Ex. : L'IA dans l'éducation")
    lancer = st.form_submit_button("🚀 Lancer l'équipe", type="primary")

if lancer and sujet.strip():
    st.session_state.pop("resultat", None)
    gauche, droite = st.columns([1, 1])

    with gauche:
        st.subheader("🛠️ L'équipe au travail")
        journal = st.status("Démarrage…", expanded=True)

    with droite:
        st.subheader("📋 Plan de recherche")
        zone_plan = st.empty()
        st.subheader("📚 Notes du Chercheur")
        zone_notes = st.container()

    for evenement in research_crew(sujet, max_revisions):
        type_ = evenement[0]

        if type_ == "debut":
            _, agent, detail = evenement
            journal.update(label=f"{ICONES[agent]} {agent} : {detail}…")
            journal.write(f"{ICONES[agent]} **{agent}** — {detail}")

        elif type_ == "plan":
            questions = evenement[1]
            if questions:
                zone_plan.markdown("\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1)))
            else:
                zone_plan.warning("Le Planificateur n'a renvoyé aucune question exploitable.")

        elif type_ == "recherche":
            _, question, reponse = evenement
            with zone_notes.expander(question):
                st.markdown(reponse)

        elif type_ == "critique":
            _, tour, critiques, approuve = evenement
            if approuve:
                journal.write(f"✅ Version {tour} **approuvée** par le Critique")
            else:
                journal.write(f"🔁 Version {tour} : corrections demandées")
                journal.info(critiques)

        elif type_ == "fin":
            _, rapport, approuve = evenement
            journal.update(
                label="✅ Rapport approuvé !" if approuve else "⚠️ Révisions maximum atteintes",
                state="complete", expanded=False,
            )
            st.session_state["resultat"] = {"sujet": sujet, "rapport": rapport, "approuve": approuve}

elif lancer:
    st.warning("Écris d'abord un sujet de recherche.")

# ---------- Rapport final (reste affiché après un clic sur « Télécharger ») ----------
if "resultat" in st.session_state:
    res = st.session_state["resultat"]
    st.divider()
    st.subheader("📄 Rapport final")
    if not res["approuve"]:
        st.caption("Le Critique n'a pas approuvé le rapport : voici la dernière version.")
    st.download_button("⬇️ Télécharger le rapport (.md)", res["rapport"],
                       file_name="rapport.md", mime="text/markdown")
    st.markdown(res["rapport"])
