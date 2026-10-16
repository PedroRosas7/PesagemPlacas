import tkinter as tk
from tkinter import messagebox, ttk


class Placa:
    def __init__(self, peso, pesosolda):
        self._peso = peso
        self._pesosolda = pesosolda
        self._mediasplacas = 0

    def media(self):
        self._mediasplacas = (self._pesosolda - self._peso) / 1000


def calcular():
    placas = []
    try:
        for i, (peso_entry, solda_entry) in enumerate(campos, start=1):
            peso = float(peso_entry.get().strip().replace(",", "."))
            peso_solda = float(solda_entry.get().strip().replace(",", "."))
            placa = Placa(peso, peso_solda)
            placa.media()
            placas.append(placa)
    except ValueError:
        messagebox.showerror(
            "Valor inválido",
            f"Preencha os dois pesos da placa {i} com números válidos.",
        )
        return

    linhas = [
        f"Placa {i}: Peso {placa._peso:.0f} g | Peso + solda {placa._pesosolda:.0f} g"
        for i, placa in enumerate(placas, start=1)
    ]
    media_placas = sum(placa._mediasplacas for placa in placas) / len(placas)
    resultado.config(
        text="\n".join(linhas) + f"\n\nMédia das placas: {media_placas:.2f} kg"
    )


def limpar():
    for peso_entry, solda_entry in campos:
        peso_entry.delete(0, tk.END)
        solda_entry.delete(0, tk.END)
    resultado.config(text="")


janela = tk.Tk()
janela.title("Cálculo da média das placas")
janela.resizable(False, False)

principal = ttk.Frame(janela, padding=16)
principal.grid()

ttk.Label(principal, text="Placa").grid(row=0, column=0, padx=6, pady=6)
ttk.Label(principal, text="Peso (g)").grid(row=0, column=1, padx=6, pady=6)
ttk.Label(principal, text="Peso + solda (g)").grid(row=0, column=2, padx=6, pady=6)

campos = []
for i in range(1, 6):
    ttk.Label(principal, text=str(i)).grid(row=i, column=0, padx=6, pady=4)
    peso_entry = ttk.Entry(principal, width=18)
    peso_entry.grid(row=i, column=1, padx=6, pady=4)
    solda_entry = ttk.Entry(principal, width=18)
    solda_entry.grid(row=i, column=2, padx=6, pady=4)
    campos.append((peso_entry, solda_entry))

acoes = ttk.Frame(principal)
acoes.grid(row=6, column=0, columnspan=3, pady=(12, 4))
ttk.Button(acoes, text="Calcular média", command=calcular).grid(
    row=0, column=0, padx=5
)
ttk.Button(acoes, text="Limpar", command=limpar).grid(row=0, column=1, padx=5)

resultado = ttk.Label(principal, text="", justify="left")
resultado.grid(row=7, column=0, columnspan=3, sticky="w", pady=(12, 0))

janela.mainloop()
