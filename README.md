# 🤖 ResearchCrew — Système multi-agents de recherche

ResearchCrew est une équipe de **4 agents IA spécialisés** qui collaborent pour produire automatiquement un rapport de recherche structuré à partir d'un simple sujet.

Le projet fonctionne **100 % en local et gratuitement** grâce à [Ollama](https://ollama.com) et au modèle open source **Llama 3.2**.

## 🧩 Architecture

```
            Sujet
              │
              ▼
      🧭 Planificateur ──► 3 sous-questions
              │
              ▼
      🔎 Chercheur (×3) ──► notes de recherche
              │
              ▼
      ✍️ Rédacteur ──► rapport ──► 🧐 Critique
              ▲                        │
              │      corrections       │
              └────────────────────────┘
                           │
                       APPROUVÉ
                           ▼
                      rapport.md
```

| Agent | Rôle |
|---|---|
| 🧭 **Planificateur** | Découpe le sujet en sous-questions précises |
| 🔎 **Chercheur** | Répond à chaque sous-question avec des faits |
| ✍️ **Rédacteur** | Assemble les notes en un rapport Markdown structuré |
| 🧐 **Critique** | Relit le rapport : l'approuve ou demande des corrections |

## ✨ Points techniques

- **Orchestration multi-agents** : la sortie de chaque agent devient l'entrée du suivant.
- **Boucle d'auto-correction** (pattern *evaluator–optimizer*) entre le Rédacteur et le Critique.
- **Garde-fou** : nombre maximum de révisions pour éviter les boucles infinies.
- **Nettoyage des sorties du LLM** : extraction robuste des questions générées.
- **Classe `Agent` réutilisable** : un nouvel agent se crée en une ligne.
- **LLM local** : aucune clé API, aucune donnée envoyée sur Internet.

## 🚀 Installation

**Prérequis :** Python 3.10+ et [Ollama](https://ollama.com/download).

```bash
git clone https://github.com/mohamed-berguiga/researchcrew.git
cd researchcrew

python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
ollama pull llama3.2
```

## ▶️ Utilisation

```bash
python main.py
```

```
📝 Sujet de recherche : L'IA dans l'éducation

🤖 [Planificateur] travaille...
📋 Questions à traiter :
  - ...
🤖 [Chercheur] travaille...
🤖 [Rédacteur] travaille...
🤖 [Critique] travaille...
✅ Le Critique a approuvé le rapport !
📄 Rapport final enregistré dans rapport.md
```

Un exemple de rapport généré est disponible dans [`exemples/exemple_rapport.md`](exemples/exemple_rapport.md).

## 📁 Structure

```
researchcrew/
├── agents.py          # Classe Agent (rôle + appel au LLM)
├── main.py            # Orchestration des 4 agents
├── requirements.txt
└── exemples/
    └── exemple_rapport.md
```

## 🛣️ Améliorations prévues

- [ ] Recherche web réelle pour le Chercheur (sources citées)
- [ ] Exécution des Chercheurs en parallèle (`asyncio`)
- [ ] Interface web avec Streamlit
- [ ] Sorties structurées en JSON

## 🛠️ Technologies

Python · Ollama · Llama 3.2 · Prompt engineering · Systèmes multi-agents

## 👤 Auteur

**Mohamed Berguiga** — élève ingénieur à l'ENISO

- 🌐 Portfolio : [mohamed-berguiga.github.io](https://mohamed-berguiga.github.io)
- 💼 LinkedIn : [mohamed-berguiga](https://www.linkedin.com/in/mohamed-berguiga-0b7999343/)
- 💻 GitHub : [@mohamed-berguiga](https://github.com/mohamed-berguiga)
