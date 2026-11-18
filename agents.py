import ollama

MODEL = "llama3.2"


class Agent:
    def __init__(self, name, role):
        # On mémorise le nom et le rôle de l'agent
        self.name = name
        self.role = role

    def run(self, task):
        # L'agent reçoit une tâche et renvoie sa réponse
        print(f"\n🤖 [{self.name}] travaille...")
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": task},
            ],
        )
        return response["message"]["content"]