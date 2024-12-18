import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import periodogram
from sklearn.linear_model import LinearRegression

class SignalProcessor:
    def __init__(self):
        self.signal = None
        self.noisy_signal = None
        self.profile = None
        self.tendency = None
        self.residue = None

    def load_signal(self, filepath):
        self.signal = np.loadtxt(filepath)
        self.noisy_signal = self.signal.copy()

    def add_noise(self, rsb):
        noise = np.random.normal(0, np.std(self.signal) / rsb, self.signal.shape)
        self.noisy_signal = self.signal + noise

    def calculate_profile(self):
        M_x = np.mean(self.noisy_signal)
        N = len(self.noisy_signal)
        self.profile = np.cumsum(self.noisy_signal - M_x)

    def calculate_tendency(self, N):
        L = len(self.profile) // N
        tendency = np.zeros(L * N)
        for i in range(L):
            segment = self.profile[i * N:(i + 1) * N]
            x = np.arange(i * N, (i + 1) * N)
            A = np.vstack([x**2, x, np.ones(N)]).T
            coeff = np.linalg.lstsq(A, segment, rcond=None)[0]
            tendency[i * N:(i + 1) * N] = coeff[0] * x**2 + coeff[1] * x + coeff[2]
        self.tendency = tendency

    def calculate_residue(self):
        if self.tendency is None:
            raise ValueError("Tendency has not been calculated. Please calculate tendency before calculating residue.")
        self.residue = self.profile[:len(self.tendency)] - self.tendency

    def calculate_F2(self, N):
        if self.residue is None:
            raise ValueError("Residue has not been calculated. Please calculate residue before calculating F2.")
        L = len(self.residue) // N
        F2 = np.zeros(L)
        for i in range(L):
            segment = self.residue[i * N:(i + 1) * N]
            F2[i] = np.var(segment)
        return np.log(F2)

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processor")
        self.processor = SignalProcessor()

        # Créer des cadres pour organiser les widgets
        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_canvas = tk.Frame(root)
        self.frame_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_canvas)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.frame_buttons, text="Charger Signal", command=self.load_signal)
        self.load_button.pack(pady=5)

        self.noise_button = tk.Button(self.frame_buttons, text="Bruit RSB", command=self.add_noise)
        self.noise_button.pack(pady=5)

        self.reload_button = tk.Button(self.frame_buttons, text="Recharger Signal", command=self.reload_signal)
        self.reload_button.pack(pady=5)

        self.periodogram_button = tk.Button(self.frame_buttons, text="Périodogramme", command=self.show_periodogram)
        self.periodogram_button.pack(pady=5)

        self.profile_button = tk.Button(self.frame_buttons, text="Profil", command=self.show_profile)
        self.profile_button.pack(pady=5)

        self.tendency_button = tk.Button(self.frame_buttons, text="Tendance", command=self.show_tendency)
        self.tendency_button.pack(pady=5)

        self.residue_button = tk.Button(self.frame_buttons, text="Résidu", command=self.show_residue)
        self.residue_button.pack(pady=5)

        self.F2_button = tk.Button(self.frame_buttons, text="Courbe F2(N)", command=self.show_F2)
        self.F2_button.pack(pady=5)

        self.rsb_entry = tk.Entry(self.frame_buttons)
        self.rsb_entry.pack(pady=5)
        self.rsb_entry.insert(0, "RSB")

        self.N_entry = tk.Entry(self.frame_buttons)
        self.N_entry.pack(pady=5)
        self.N_entry.insert(0, "N")

    def load_signal(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.processor.load_signal(filepath)
            self.plot_signal(self.processor.signal)

    def add_noise(self):
        try:
            rsb = float(self.rsb_entry.get())
            self.processor.add_noise(rsb)
            self.plot_signal(self.processor.noisy_signal)
        except ValueError:
            print("Veuillez entrer une valeur numérique pour le RSB.")

    def reload_signal(self):
        self.processor.noisy_signal = self.processor.signal.copy()
        self.plot_signal(self.processor.signal)

    def show_periodogram(self):
        f, Pxx = periodogram(self.processor.noisy_signal)
        plt.figure()
        plt.semilogy(f, Pxx)
        plt.title("Périodogramme")
        plt.xlabel("Fréquence")
        plt.ylabel("Densité spectrale de puissance")
        plt.show()

    def show_profile(self):
        self.processor.calculate_profile()
        self.plot_signal(self.processor.profile)

    def show_tendency(self):
        N = int(self.N_entry.get())
        self.processor.calculate_tendency(N)
        self.plot_signal(self.processor.tendency)

    def show_residue(self):
        self.processor.calculate_residue()
        self.plot_signal(self.processor.residue)

    def show_F2(self):
        self.processor.calculate_residue()
        N_values = np.arange(10, 8001)
        F2_values = []

        for N in N_values:
            self.processor.calculate_tendency(N)
            self.processor.calculate_residue()
            F2 = np.sqrt(np.var(self.processor.residue))
            F2_values.append(F2)

        log_N = np.log(N_values)
        log_F2 = np.log(F2_values)

        plt.figure()
        plt.plot(log_N, log_F2, label="F2(N)")
        plt.title("Courbe F2(N)")
        plt.xlabel("log(N)")
        plt.ylabel("log(F2(N))")
        plt.legend()
        plt.show()

    def plot_signal(self, signal):
        self.ax.clear()
        self.ax.plot(signal, color="blue")
        self.ax.set_xlabel("Échantillons")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("Signal")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()