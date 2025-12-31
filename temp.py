import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import matplotlib.pyplot as plt

# === CONFIGURATION API ===
SENTIMENT_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
SUMMARY_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_TOKEN"}

# === COMPTEURS ===
positif_count = 0
negatif_count = 0
neutre_count = 0

# === FONCTIONS APPEL API ===
def query_api(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# === FONCTION PRINCIPALE D’ANALYSE / RÉSUMÉ ===
def executer():
    global positif_count, negatif_count, neutre_count

    texte = input_text.get("1.0", tk.END).strip()
    choix = choix_var.get()

    output_text.delete("1.0", tk.END)

    if not texte:
        messagebox.showwarning("Attention", "Veuillez entrer un texte à analyser.")
        return

    if choix == 1:  # 🔹 Analyse de sentiment
        resultat = query_api(SENTIMENT_URL, {"inputs": texte})
        if isinstance(resultat, list):
            dominant = max(resultat[0], key=lambda x: x["score"])
            label = dominant["label"].lower()
            score = dominant["score"]

            if label == "positive":
                color, emoji = "green", "😃"
                positif_count += 1
            elif label == "negative":
                color, emoji = "red", "😡"
                negatif_count += 1
            else:
                color, emoji = "gray", "😐"
                neutre_count += 1

            output_text.insert(tk.END, f"Texte analysé :\n{texte}\n\n")
            output_text.insert(tk.END, f"Sentiment dominant : {label.upper()} {emoji} ({score:.2f})\n", "result")
            output_text.tag_config("result", foreground=color, font=("Arial", 14, "bold"))

            output_text.insert(tk.END, "\nDétails :\n")
            for item in resultat[0]:
                output_text.insert(tk.END, f"- {item['label']} : {item['score']:.2f}\n")
        else:
            output_text.insert(tk.END, f"Erreur : {resultat.get('error', 'Unknown error')}")

    elif choix == 2:  # 🔹 Résumé du texte
        resultat = query_api(SUMMARY_URL, {"inputs": texte})
        if isinstance(resultat, list) and "summary_text" in resultat[0]:
            resume = resultat[0]["summary_text"]
            output_text.insert(tk.END, f"Texte original :\n{texte}\n\n", "normal")
            output_text.insert(tk.END, f"Résumé généré :\n{resume}\n", "summary")
            output_text.tag_config("summary", foreground="blue", font=("Arial", 12, "italic"))
        else:
            output_text.insert(tk.END, f"Erreur : {resultat.get('error', 'Unknown error')}")

# === GRAPHIQUE DES SENTIMENTS ===
def afficher_graphique():
    labels = ["Positif", "Négatif", "Neutre"]
    valeurs = [positif_count, negatif_count, neutre_count]
    plt.bar(labels, valeurs, color=["green", "red", "gray"])
    plt.title("Répartition des sentiments analysés")
    plt.ylabel("Nombre de textes")
    plt.show()

# === INTERFACE TKINTER ===
fenetre = tk.Tk()
fenetre.title("🧠 Analyse & Résumé de Texte - Hugging Face API")
fenetre.geometry("700x600")
fenetre.configure(bg="#f4f6f9")

# === Titre ===
titre = tk.Label(fenetre, text="Analyse de Sentiments & Résumé de Texte", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#333")
titre.pack(pady=15)

# === Choix utilisateur ===
choix_var = tk.IntVar(value=1)
choix_frame = tk.Frame(fenetre, bg="#f4f6f9")
choix_frame.pack(pady=10)

tk.Label(choix_frame, text="Choisissez une option :", font=("Arial", 12), bg="#f4f6f9").grid(row=0, column=0, sticky="w", padx=10)
tk.Radiobutton(choix_frame, text="1️⃣ Analyse de sentiment", variable=choix_var, value=1, bg="#f4f6f9", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=20)
tk.Radiobutton(choix_frame, text="2️⃣ Résumer le texte", variable=choix_var, value=2, bg="#f4f6f9", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=20)

# === Zone saisie texte ===
label1 = tk.Label(fenetre, text="Entrez votre texte :", font=("Arial", 12), bg="#f4f6f9")
label1.pack(anchor="w", padx=20)

input_text = scrolledtext.ScrolledText(fenetre, height=6, width=75, font=("Arial", 11))
input_text.pack(pady=10)

# === Boutons ===
btn_frame = tk.Frame(fenetre, bg="#f4f6f9")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="▶️ Exécuter", command=executer, bg="#0078D7", fg="white", font=("Arial", 12, "bold"), padx=20, relief="flat").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="📊 Voir statistiques", command=afficher_graphique, bg="#28a745", fg="white", font=("Arial", 12, "bold"), padx=20, relief="flat").grid(row=0, column=1, padx=10)

# === Zone de sortie ===
label2 = tk.Label(fenetre, text="Résultat :", font=("Arial", 12), bg="#f4f6f9")
label2.pack(anchor="w", padx=20, pady=5)

output_text = scrolledtext.ScrolledText(fenetre, height=15, width=75, font=("Consolas", 11))
output_text.pack(pady=5)

# === Lancer interface ===
fenetre.mainloop()
