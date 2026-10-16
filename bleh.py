class Placa():
    def __init__(self,peso,pesosolda):
        self._peso = peso
        self._pesosolda = pesosolda
        self._mediasplacas = 0


    def media(self):
        self._mediasplacas = (self._pesosolda - self._peso)/1000
   
saida = 0

def ler_peso(mensagem):
        while True:
            try:
                return float(input(mensagem))
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")

while saida != 1:
    placastotal = []
    for i in range(5):
        peso1 = ler_peso(f"Peso {[i+1]}:")
        pesosolda1 = ler_peso(f"Peso Solda {[i+1]}:")
        
        p1 = Placa(peso1,pesosolda1)
        p1.media()
        
        placastotal.append(p1)

    print("\n")

    media_placas = sum(placa._mediasplacas for placa in placastotal) / len(placastotal)

    print("PLACAS CADASTRADAS:\n")

    for i, placa in enumerate(placastotal, start=1):
        print(f"Placa {i}: Peso {placa._peso:.0f}g !! Peso+Solda {placa._pesosolda:.0f}g ")

    print(f"\nA média das placas são {media_placas:.2f}Kg\n")
    saida = int(input("Deseja sair? (1 - Sim, 0 - Não): "))

print("\nPrograma encerrado.")