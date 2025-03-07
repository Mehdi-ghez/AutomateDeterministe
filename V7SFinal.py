import customtkinter as ctk
from tkinter import messagebox

class AutomateGen:
    def __init__(self):
        self.states = set()
        self.StartState = None
        self.finalStates = set()
        self.transitions = {}

    def addState(self, state, ret, sep):
        for num in state.split(sep):
            self.states.add(num.strip())
        ret[0] += 1

    def setStartState(self, state, ret):
        if state in self.states:
            self.StartState = state
            ret[0] += 1
        else:
            print("Etat inexistant.")            

    def addFinalState(self, state, ret, sep):
        for num in state.split(sep):
            if num in self.states:
                self.finalStates.add(num.strip())
            else:
                print("Etat inexistant.")
                ret[0] -= 1
            ret[0] += 1
            
    def add_transition(self, from_state, to_state, label):
        if from_state in self.states and to_state in self.states:
            if from_state not in self.transitions:
                self.transitions[from_state] = []
            self.transitions[from_state].append((to_state, label))
        else:
            print("L'un des etats est inexistant")

    def visualize(self, text_widget):
        if not self.StartState:
            messagebox.showerror("Erreur", "Etat initial inexistant")
            return

        Chemin = []

        def traverse(current_state, path):
            if current_state in self.finalStates:
                Chemin.append(f"{path} -> {current_state}*")
                return

            if current_state not in self.transitions:
                Chemin.append(f"{path} -> {current_state}")
                return

            for next_state, label in self.transitions[current_state]:
                if next_state == current_state:
                    Chemin.append(f"{path} -> {current_state} --({label})-- boucle")
                else:
                    traverse(next_state, f"{path} -> {current_state} --({label})--")

        traverse(self.StartState, f"start={self.StartState}")

        text_widget.delete("1.0", ctk.END)
        for path in Chemin:
            text_widget.insert(ctk.END, f"Path: {path}\n")

    def test_string_nd(self, test_str):
        Stck = [(self.StartState, 0, [])]

        while Stck:
            current_state, pos, path = Stck.pop()

            if pos == len(test_str):
                if current_state in self.finalStates:
                    return True, "Accepté", path
                else :
                    return False, "etat non final", path
                continue

            if current_state in self.transitions:
                char = test_str[pos]
                for to_state, label in self.transitions[current_state]:
                    if label == char:
                        Stck.append((to_state, pos + 1, path + [f"{current_state} --({label})--> {to_state}"]))

        return False, "Rejeté : Aucun chemin valide trouvé", path

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.fsm = AutomateGen()
        self.ret = [0]
        self.sep = ','  # Default separator
        self.title("SCreation Automate et reconnaissance de mots")
        self.geometry("900x520")

        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=3, uniform="group1")

        self.Lframe = ctk.CTkFrame(self)
        self.Lframe.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
        
        self.Lframe3 = ctk.CTkFrame(self)
        self.Lframe3.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        
        self.Lframe2 = ctk.CTkFrame(self)
        self.Lframe2.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.Rframe = ctk.CTkFrame(self)
        self.Rframe.grid(row=0 , column=1, rowspan=3, sticky="nswe", padx=10, pady=10)

        self.sep_label = ctk.CTkLabel(self.Lframe2, text="Séparateur de caractères")
        self.sep_entry = ctk.CTkEntry(self.Lframe2, placeholder_text="Caractere séparateur")
        self.sep_entry.pack(pady=5)

        self.state_label = ctk.CTkLabel(self.Lframe2, text="Definition des états")
        self.state_entry = ctk.CTkEntry(self.Lframe2, placeholder_text="Les états")
        self.state_entry.pack(pady=5)

        self.StartState_entry = ctk.CTkEntry(self.Lframe2, placeholder_text="Etat initial")
        self.StartState_entry.pack(pady=5)

        self.final_state_entry = ctk.CTkEntry(self.Lframe2, placeholder_text="Etats finaux")
        self.final_state_entry.pack(pady=5)
        
        self.Label=ctk.CTkLabel(self.Lframe, text="Transitions")
        self.process_button = ctk.CTkButton(self.Lframe2, text="Ajouter/Définir", command=self.process_states)
        self.process_button.pack(pady=5)

        self.from_state_entry = ctk.CTkEntry(self.Lframe3, placeholder_text="De l'état")
        self.from_state_entry.pack(pady=5)

        self.to_state_entry = ctk.CTkEntry(self.Lframe3, placeholder_text="Vers l'état")
        self.to_state_entry.pack(pady=5)

        self.label_entry = ctk.CTkEntry(self.Lframe3, placeholder_text="Le caractère")
        self.label_entry.pack(pady=5)

        self.transition_button = ctk.CTkButton(self.Lframe3, text="Ajouter transition", command=self.add_transition)
        self.transition_button.pack(pady=5)

        self.test_entry = ctk.CTkEntry(self.Lframe, placeholder_text="Entrez le mot à tester")
        self.test_entry.pack(pady=5)

        self.visualize_button = ctk.CTkButton(self.Lframe, text="Visualiser", command=self.visualize)
        self.visualize_button.pack(pady=5)

        self.test_button = ctk.CTkButton(self.Lframe, text="Tester le mot", command=self.test_string)
        self.test_button.pack(pady=5)

        self.text_widget = ctk.CTkTextbox(self.Rframe, height=100)
        self.text_widget.pack(fill="both", expand=True, pady=10)

    def process_states(self):
        state = self.state_entry.get()
        StartState = self.StartState_entry.get()
        final_state = self.final_state_entry.get()
        sep = self.sep_entry.get()

        if state:
            self.fsm.addState(state, self.ret, self.sep)
            self.state_entry.delete(0, ctk.END)

        if StartState:
            self.fsm.setStartState(StartState, self.ret)
            self.StartState_entry.delete(0, ctk.END)

        if final_state:
            self.fsm.addFinalState(final_state, self.ret, self.sep)
            self.final_state_entry.delete(0, ctk.END)

    def add_transition(self):
        from_state = self.from_state_entry.get()
        to_state = self.to_state_entry.get()
        label = self.label_entry.get()
        if from_state and to_state and label:
            self.fsm.add_transition(from_state, to_state, label)
            self.from_state_entry.delete(0, ctk.END)
            self.to_state_entry.delete(0, ctk.END)
            self.label_entry.delete(0, ctk.END)

    def visualize(self):
        self.fsm.visualize(self.text_widget)

    def test_string(self):
        test_str = self.test_entry.get()
        if test_str:
            accepted, message, path = self.fsm.test_string_nd(test_str)
            messagebox.showinfo("Résultat", f"{'Accepté' if accepted else 'Rejeté'} - {message}")
            if accepted:
                self.text_widget.delete("1.0", ctk.END)
                self.text_widget.insert(ctk.END, "Chemin: " + " -> ".join(path))
            else:
                self.text_widget.delete("1.0", ctk.END)
                self.text_widget.insert(ctk.END, "Aucun chemin valide trouvé")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
