import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import pypdf
import json




API_KEY = "OigQQrSgyNRpeBGtNVhTB2ziikqwniFPtfytcIum"

url = "https://api.cohere.com/v2/chat"
headers = {
    "Authorization" : f"Bearer {API_KEY}",
    "Content-Type" : "application/json"
}
historique =[
    {"role": "system", "content": "Tu es SAI, un assistant éducatif spécialisé dans le programme scolaire Camerounais, tu acceptes des fichiers pdf importer et génère des questions à choix multiples"}
]

questionIndx = 0
quiz_quests = []
score = 0
result = []

def sendMsg(event=None):
    message = textArea.get()
    if not message.strip():
        return
    if quiz_quests and questionIndx >= len(quiz_quests):
        historique.clear()
        historique.append({"role": "system", "content": "Tu es SAI, un assistant éducatif spécialisé dans le programme scolaire Camerounais, tu acceptes des fichiers pdf importer et génère des questions à choix multiples"})
        btnA.pack_forget()
        btnB.pack_forget()
        btnC.pack_forget()
        btnD.pack_forget()
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, "Toi: " + message + '\n\n')
    widget.config(state=tk.DISABLED)
    textArea.delete(0, tk.END)
    historique.append({"role":"user", "content":message})
    
    payload = {
    "model": "command-r-08-2024",
    "messages": historique
    }
    response = requests.post(url, headers=headers, json=payload)
    data=response.json()
    texte = data["message"]["content"][0]["text"]
    historique.append({"role":"assistant", "content":texte})
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, "Bot: " + texte + "\n\n")
    widget.config(state=tk.DISABLED)



def importPDF():
    global quiz_quests, questionIndx, score, result
    path = filedialog.askopenfilename()
    if not path:
        return
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, "⏳Analyse du PDF en cours...\n\n")
    widget.config(state=tk.DISABLED)
    window.update()  # force Tkinter à rafraîchir l'affichage
    
    reader = pypdf.PdfReader(path)
    content = ""
    for page in reader.pages[2:]:
        content += page.extract_text()
    historique.clear()
    historique.append({"role": "user", "content": f"Voici le contenu d'un document scolaire : {content[:3000]}. Génère 5 questions QCM basées sur les concepts et notions de ce contenu. Réponds UNIQUEMENT avec un tableau JSON valide, sans texte avant ou après, sans balises markdown. Format attendu : [{{'question': '...', 'choix': ['A. ...', 'B. ...', 'C. ...', 'D. ...'], 'reponse': 'A'}}]"})
    
    payload = {
         "model":"command-r-08-2024",
         "messages": historique
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    texte = data["message"]["content"][0]["text"]
    historique.append({"role": "assistant", "content": texte})
    try:
        questions = json.loads(texte)
        quiz_quests = questions
        questionIndx = 0
        score = 0
        result = []
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, "Question 1: " + questions[0]["question"] +"\n\n")
        for choix in questions[0]["choix"]:
            widget.insert(tk.END, choix + "\n")
        widget.config(state=tk.DISABLED)
        btnA.pack(fill="x")
        btnB.pack(fill="x")
        btnC.pack(fill="x")
        btnD.pack(fill="x")
    except:
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, "❌ Erreur lors de la génération des questions. Réessaie.\n\n")
        widget.config(state=tk.DISABLED)
        return

def generateReport():
    if not result:
        return
    plt.clf()
    bonneRep = score
    mauvaiseRep = len(result) - score
    plt.pie(
    [bonneRep, mauvaiseRep],
    labels = ["Correct answer", "Wrong answer"],
    colors = ["green", "red"],
    autopct ="%1.1f%%"
        )
    plt.title("Chart progression")
    plt.show()
    
def respond(choice):
    global questionIndx, score
    if not quiz_quests:
        return
    result.append({
        "question": quiz_quests[questionIndx]["question"],
        "user_response": choice,
        "correct_answer": quiz_quests[questionIndx]["reponse"],
        "correct": choice == quiz_quests[questionIndx]["reponse"],
        "date": datetime.now().strftime("%d%m%Y %H:%M")
         })
    # 1. comparer choix_eleve avec la bonne réponse
    if choice == quiz_quests[questionIndx]["reponse"]:
    # 2. incrémenter score si correct
        score += 1
    # 3. afficher résultat
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, quiz_quests[questionIndx]["question"] + " bonne réponse: " + quiz_quests [questionIndx]["reponse"] + "\n\n")
        widget.config(state=tk.DISABLED)
    else:
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, quiz_quests[questionIndx]["question"] + " La bonne réponse était: " + quiz_quests [questionIndx]["reponse"] + "\n\n")
        widget.config(state=tk.DISABLED)
    # 4. passer à la question suivante ou afficher score final
    questionIndx += 1
    if questionIndx < len(quiz_quests):
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, f"Question {questionIndx+1}: " + quiz_quests[questionIndx]["question"] +"\n\n")
        for choix in quiz_quests[questionIndx]["choix"]:
            widget.insert(tk.END, choix + "\n")
        widget.config(state=tk.DISABLED)
    else:
        widget.config(state=tk.NORMAL)
        widget.insert(tk.END, "Le score final est: " + str(score) + "\nFin du quiz vous pourrez consulter votre rapport en cliquant sur le bouton Generate Report.\n\n")
        widget.config(state=tk.DISABLED)
        btnA.pack_forget()
        btnB.pack_forget()
        btnC.pack_forget()
        btnD.pack_forget()

window = tk.Tk()
window.title('Chatbot-v1')
widget = ScrolledText(window, width=40, height=40, state=tk.DISABLED, wrap=tk.WORD)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
widget.grid(row=0, column=0, rowspan=5, sticky="nsew")

textArea = tk.Entry(window, width=50)
textArea.bind("<Return>", sendMsg)
textArea.grid(row=5, column=0, sticky="ew")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=0) 

sendBtn = tk.Button(window, text="Send", command=sendMsg)
sendBtn.grid(row=5, column=1, sticky="ew")

board = tk.Frame(window)
board.grid(row=0, column=1, sticky="n")

importBtn = tk.Button(board, text="Import PDF", command=importPDF)
importBtn.pack(fill="x")

reportBtn = tk.Button(board, text="Generate Report", command=generateReport)
reportBtn.pack(fill="x")


btnA = tk.Button(board, text = "A", command=lambda: respond("A"))
btnA.pack_forget()


btnB = tk.Button(board, text = "B", command=lambda: respond("B"))
btnB.pack_forget()


btnC = tk.Button(board, text = "C",
command=lambda: respond("C"))
btnC.pack_forget()


btnD = tk.Button(board, text = "D", command=lambda: respond("D"))
btnD.pack_forget()


window.mainloop()