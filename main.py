import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import pinv

# Fonction pour calculer le profil du signal
def profil_signal(x, M_x):
    N = len(x)
    p = np.zeros(N)
    c = x - M_x
    for i in range(N):
        p[i] = np.sum(c[:i+1])
    return p

# Fonction pour calculer la tendance locale
def tendance_2(segment, i, N):
    x = np.arange(i * N, (i + 1) * N)
    y = segment

    B = y.reshape(-1, 1)
    A = np.vstack([x**2, x, np.ones_like(x)]).T

    coeff = pinv(A) @ B
    a, b, c = coeff.flatten()
    return a * x**2 + b * x + c

# Fonction pour calculer le résidu
def calcul_residu(profil, N):
    L = len(profil) // N
    profil = profil[:L * N]
    residu = np.zeros_like(profil)

    for i in range(L):
        segment = profil[i * N:(i + 1) * N]
        tendance_loc = tendance_2(segment, i, N)
        residu[i * N:(i + 1) * N] = segment - tendance_loc

    return residu

# Classe principale de l'interface graphique
class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyse de Signal")

        self.signal = None
        self.noised_signal = None
        self.mean_signal = 0

        # Zone d'affichage
        self.figure, self.ax = plt.subplots()
        self.canvas = None
        self.create_canvas()

        # Boutons et champs de l'interface
        self.create_controls()

    def create_canvas(self):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(frame, text="Charger Signal", command=self.load_signal).pack(side=tk.LEFT)
        tk.Button(frame, text="Bruit RSB", command=self.add_noise).pack(side=tk.LEFT)
        tk.Button(frame, text="Afficher Périodogramme", command=self.show_periodogram).pack(side=tk.LEFT)
        tk.Button(frame, text="Afficher Profil", command=self.show_profile).pack(side=tk.LEFT)
        tk.Button(frame, text="Afficher Tendance", command=self.show_trends).pack(side=tk.LEFT)
        tk.Button(frame, text="Afficher Résidu", command=self.show_residu).pack(side=tk.LEFT)
        tk.Button(frame, text="Afficher F2(N)", command=self.show_F2).pack(side=tk.LEFT)

    def load_signal(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.signal = np.loadtxt(file_path)
                self.mean_signal = np.mean(self.signal)
                self.noised_signal = self.signal.copy()
                self.plot_signal(self.signal, "Signal Initial")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le signal : {e}")

    def add_noise(self):
        if self.signal is None:
            messagebox.showerror("Erreur", "Aucun signal chargé.")
            return

        try:
            rsb = simpledialog.askfloat("RSB", "Entrez le RSB (en dB) :")
            if rsb is None:
                return

            puissance_signal = np.mean(self.signal**2)
            puissance_bruit = puissance_signal / (10**(rsb / 10))
            bruit = np.random.normal(0, np.sqrt(puissance_bruit), size=self.signal.shape)

            self.noised_signal = self.signal + bruit
            self.plot_signal(self.noised_signal, "Signal Bruité")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du bruitage : {e}")

    def show_periodogram(self):
        if self.noised_signal is None:
            messagebox.showerror("Erreur", "Aucun signal à analyser.")
            return

        freq, Pxx = plt.psd(self.noised_signal, NFFT=256, Fs=1)
        self.ax.clear()
        self.ax.plot(freq, Pxx)
        self.ax.set_title("Périodogramme")
        self.canvas.draw()

    def show_profile(self):
        if self.noised_signal is None:
            messagebox.showerror("Erreur", "Aucun signal à analyser.")
            return

        profil = profil_signal(self.noised_signal, self.mean_signal)
        self.plot_signal(profil, "Profil du Signal")

    def show_trends(self):
        if self.noised_signal is None:
            messagebox.showerror("Erreur", "Aucun signal à analyser.")
            return

        try:
            N = simpledialog.askinteger("Taille des parties", "Entrez la taille N des parties :")
            if N is None:
                return

            profil = profil_signal(self.noised_signal, self.mean_signal)
            L = len(profil) // N
            profil = profil[:L * N]

            tendance_globale = np.zeros_like(profil)
            for i in range(L):
                segment = profil[i * N:(i + 1) * N]
                tendance_globale[i * N:(i + 1) * N] = tendance_2(segment, i, N)

            self.plot_signal(tendance_globale, "Tendance Globale")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul des tendances : {e}")

    def show_residu(self):
        if self.noised_signal is None:
            messagebox.showerror("Erreur", "Aucun signal à analyser.")
            return

        try:
            N = simpledialog.askinteger("Taille des parties", "Entrez la taille N des parties :")
            if N is None:
                return

            profil = profil_signal(self.noised_signal, self.mean_signal)
            residu = calcul_residu(profil, N)
            self.plot_signal(residu, "Résidu du Profil")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul du résidu : {e}")

    def show_F2(self):
        if self.noised_signal is None:
            messagebox.showerror("Erreur", "Aucun signal à analyser.")
            return

        try:
            N = simpledialog.askinteger("Taille des parties", "Entrez la taille N des parties :")
            if N is None:
                return

            profil = profil_signal(self.noised_signal, self.mean_signal)
            residu = calcul_residu(profil, N)

            L = len(residu) // N
            F2 = [np.var(residu[i * N:(i + 1) * N]) for i in range(L)]
            log_F2 = np.log(F2)

            self.plot_signal(log_F2, "log(F2(N))")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul de F2(N) : {e}")

    def plot_signal(self, signal, title):
        self.ax.clear()
        self.ax.plot(signal)
        self.ax.set_title(title)
        self.canvas.draw()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()