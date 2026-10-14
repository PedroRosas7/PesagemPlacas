placastotal = []

class Placa():
    def __init__(self,peso,pesosolda):
        self._peso = peso
        self._pesosolda = pesosolda
        self._mediasplacas = 0


    def media(self):
        self._mediasplacas = (self._peso - self._pesosolda) / 5
        print(self._mediasplacas)

    def resultados(self):
        for placa in placastotal:
            print(f"Placa{i}")
        return f"A média das placas são {self._mediasplacas}"

for i in range(5):
    peso1 = float(input(f"Peso {[i+1]}:"))
    pesosolda1 = float(input(f"Peso Solda {[i+1]}:"))



p1 = Placa(peso1,pesosolda1)
print(p1.resultados())
