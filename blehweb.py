import json
import math
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PAGINA = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cálculo da média das placas</title>
  <style>
    :root { color-scheme: light; font-family: system-ui, sans-serif; }
    body { margin: 0; padding: 32px 16px; background: #f1f5f9; color: #172033; }
    main { max-width: 680px; margin: auto; padding: 28px; background: white;
      border-radius: 14px; box-shadow: 0 8px 28px #17203318; }
    h1 { margin-top: 0; font-size: 1.6rem; }
    p { color: #526078; }
    .linha { display: grid; grid-template-columns: 70px 1fr 1fr; gap: 12px;
      align-items: center; margin: 12px 0; }
    label { font-weight: 600; }
    input { box-sizing: border-box; width: 100%; padding: 11px;
      border: 1px solid #bdc8d8; border-radius: 7px; font: inherit; }
    input:focus { outline: 2px solid #2563eb; border-color: transparent; }
    .cabecalho { color: #526078; font-size: .9rem; font-weight: 600; }
    .botoes { display: flex; gap: 10px; margin-top: 22px; }
    button { padding: 11px 16px; border: 0; border-radius: 7px;
      font: inherit; font-weight: 600; cursor: pointer; }
    button[type="submit"] { background: #2563eb; color: white; }
    button[type="reset"] { background: #e2e8f0; color: #172033; }
    #resultado { margin-top: 24px; white-space: pre-line; line-height: 1.7; }
    #resultado.erro { color: #b42318; }
    @media (max-width: 480px) {
      main { padding: 20px 16px; }
      .linha { grid-template-columns: 42px 1fr 1fr; gap: 7px; }
      input { padding: 9px 6px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>Cálculo da média das placas</h1>
    <p>Informe os pesos em gramas para calcular a média de material de solda em kg.</p>
    <form id="formulario">
      <div class="linha cabecalho" aria-hidden="true">
        <span>Placa</span><span>Peso (g)</span><span>Peso + solda (g)</span>
      </div>
      <div id="campos"></div>
      <div class="botoes">
        <button type="submit">Calcular média</button>
        <button type="reset">Limpar</button>
      </div>
    </form>
    <div id="resultado" role="status" aria-live="polite"></div>
  </main>
  <script>
    const campos = document.querySelector("#campos");
    for (let i = 1; i <= 5; i += 1) {
      const linha = document.createElement("div");
      linha.className = "linha";
      linha.innerHTML =
        `<label for="peso-${i}">Placa ${i}</label>` +
        `<input id="peso-${i}" name="peso" type="text" inputmode="decimal" ` +
        `placeholder="Ex.: 1200" aria-label="Peso da placa ${i} em gramas" required>` +
        `<input id="solda-${i}" name="peso_solda" type="text" inputmode="decimal" ` +
        `placeholder="Ex.: 1250" aria-label="Peso da placa ${i} com solda em gramas" required>`;
      campos.append(linha);
    }

    const formulario = document.querySelector("#formulario");
    const resultado = document.querySelector("#resultado");

    formulario.addEventListener("submit", async (evento) => {
      evento.preventDefault();
      resultado.className = "";
      resultado.textContent = "Calculando...";
      const dados = {
        placas: Array.from({ length: 5 }, (_, i) => ({
          peso: document.querySelector(`#peso-${i + 1}`).value.trim(),
          peso_solda: document.querySelector(`#solda-${i + 1}`).value.trim()
        }))
      };

      try {
        const resposta = await fetch("/calcular", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dados)
        });
        const conteudo = await resposta.json();
        if (!resposta.ok) throw new Error(conteudo.erro || "Não foi possível calcular.");
        resultado.textContent = conteudo.placas.join("\\n") +
          `\\n\\nMédia das placas: ${conteudo.media.toFixed(2)} kg`;
      } catch (erro) {
        resultado.className = "erro";
        resultado.textContent = erro.message;
      }
    });

    formulario.addEventListener("reset", () => {
      resultado.className = "";
      resultado.textContent = "";
    });
  </script>
</body>
</html>
"""


def ler_peso(valor):
    texto = str(valor).strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)


def calcular_placas(dados):
    if not isinstance(dados, dict) or not isinstance(dados.get("placas"), list):
        raise ValueError("Envie os dados das placas.")
    if len(dados["placas"]) != 5:
        raise ValueError("Informe os pesos das cinco placas.")

    resultados = []
    diferencas = []
    for indice, placa in enumerate(dados["placas"], start=1):
        if not isinstance(placa, dict):
            raise ValueError(f"Dados inválidos para a placa {indice}.")
        try:
            peso = ler_peso(placa["peso"])
            peso_solda = ler_peso(placa["peso_solda"])
        except (KeyError, ValueError) as erro:
            raise ValueError(f"Informe números válidos para a placa {indice}.") from erro
        if not math.isfinite(peso) or not math.isfinite(peso_solda):
            raise ValueError(f"Informe números válidos para a placa {indice}.")

        diferenca = peso_solda - peso
        diferencas.append(diferenca)
        resultados.append(
            f"Placa {indice}: Peso {peso:.0f} g | "
            f"Peso + solda {peso_solda:.0f} g | "
            f"Solda: {diferenca / 1000:.2f} kg"
        )

    media = sum(diferencas) / len(diferencas) / 1000
    return {"placas": resultados, "media": media}


class Servidor(BaseHTTPRequestHandler):
    def responder(self, status, conteudo, tipo):
        corpo = conteudo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Página não encontrada")
            return
        self.responder(200, PAGINA, "text/html")

    def do_POST(self):
        if self.path != "/calcular":
            self.send_error(404, "Página não encontrada")
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if tamanho <= 0 or tamanho > 16_384:
                raise ValueError("Envie dados válidos para calcular.")
            dados = json.loads(self.rfile.read(tamanho))
            resultado = calcular_placas(dados)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as erro:
            corpo = json.dumps({"erro": str(erro)}, ensure_ascii=False)
            self.responder(400, corpo, "application/json")
            return
        self.responder(
            200,
            json.dumps(resultado, ensure_ascii=False),
            "application/json",
        )

    def log_message(self, formato, *args):
        print(f"{self.address_string()} - {formato % args}")


def main():
    endereco = ("0.0.0.0", 8000)
    servidor = ThreadingHTTPServer(endereco, Servidor)
    url = "http://localhost:8000"
    print(f"Aplicação disponível em {url}")
    print("Para parar o servidor, pressione Ctrl+C.")
    threading.Timer(1, webbrowser.open, args=(url,)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
