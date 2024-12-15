import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
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

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Charger Signal", command=self.load_signal)
        self.load_button.pack(side=tk.LEFT)

        self.noise_button = tk.Button(root, text="Bruit RSB", command=self.add_noise)
        self.noise_button.pack(side=tk.LEFT)

        self.reload_button = tk.Button(root, text="Recharger Signal", command=self.reload_signal)
        self.reload_button.pack(side=tk.LEFT)

        self.periodogram_button = tk.Button(root, text="Périodogramme", command=self.show_periodogram)
        self.periodogram_button.pack(side=tk.LEFT)

        self.profile_button = tk.Button(root, text="Profil", command=self.show_profile)
        self.profile_button.pack(side=tk.LEFT)

        self.tendency_button = tk.Button(root, text="Tendance", command=self.show_tendency)
        self.tendency_button.pack(side=tk.LEFT)

        self.residue_button = tk.Button(root, text="Résidu", command=self.show_residue)
        self.residue_button.pack(side=tk.LEFT)

        self.F2_button = tk.Button(root, text="Courbe F2(N)", command=self.show_F2)
        self.F2_button.pack(side=tk.LEFT)

        self.rsb_entry = tk.Entry(root)
        self.rsb_entry.pack(side=tk.LEFT)
        self.rsb_entry.insert(0, "RSB")

        self.N_entry = tk.Entry(root)
        self.N_entry.pack(side=tk.LEFT)
        self.N_entry.insert(0, "N")

    def load_signal(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.processor.load_signal(filepath)
            self.plot_signal(self.processor.signal)

    def add_noise(self):
        rsb = float(self.rsb_entry.get())
        self.processor.add_noise(rsb)
        self.plot_signal(self.processor.noisy_signal)

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
        N = int(self.N_entry.get())
        F2 = self.processor.calculate_F2(N)
        x = np.arange(1, len(F2) + 1)
        plt.figure()
        plt.plot(x, F2, label="F2(N)")
        plt.title("Courbe F2(N)")
        plt.xlabel("N")
        plt.ylabel("log(F2(N))")
        plt.legend()
        plt.show()

    def plot_signal(self, signal):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x = np.linspace(0, width, len(signal))
        y = height / 2 - signal * height / (2 * np.max(np.abs(signal)))
        points = np.array([x, y]).T.flatten().tolist()
        self.canvas.create_line(points, fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()