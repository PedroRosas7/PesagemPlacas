class Placa():
    def __init__(self,peso,pesosolda):
        self._peso = peso
        self._pesosolda = pesosolda
        self._mediasplacas = 0


    def media(self):
        self._mediasplacas = (self._pesosolda - self._peso) / 5
        
    def resultados(self):
        return f"A média das placas são {self._mediasplacas}"

placastotal = []

for i in range(5):
    peso1 = float(input(f"Peso {[i+1]}:"))
    pesosolda1 = float(input(f"Peso Solda {[i+1]}:"))

    p1 = Placa(peso1,pesosolda1)
    p1.media()
    
    placastotal.append(p1)

for i, placa in enumerate(placastotal, start=1):
    print(f"Placa {i}: Peso {placa._peso}. PesoSolda {placa._pesosolda}.")

print(p1.resultados())
