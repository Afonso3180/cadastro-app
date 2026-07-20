"""
Aplicação de cadastro simples (Nome, CPF, E-mail) -> CSV.

Feita para servir de material de aula:
- Demonstra uma "GUI" em Python para a web (formulário HTML servido por Flask).
- Serve como alvo estável para automação com Selenium (ids/names previsíveis).

Como rodar localmente:
    pip install -r requirements.txt
    python app.py
Depois acesse http://localhost:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash, Response
import csv
import os
import re
from datetime import datetime

app = Flask(__name__)

# Em produção, defina essas variáveis de ambiente em vez de usar os valores padrão.
app.secret_key = os.environ.get("SECRET_KEY", "0c014b105c16194c6b95a14fa3f41ae8")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "928617b7b1b0f5de82d150ce0b9b759f")

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cadastros.csv")
CSV_HEADER = ["nome", "cpf", "email", "data_hora"]


def validar_cpf(cpf: str) -> bool:
    """Valida um CPF usando o algoritmo oficial dos dígitos verificadores."""
    cpf = re.sub(r"\D", "", cpf or "")
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def formatar_cpf(cpf: str) -> str:
    cpf = re.sub(r"\D", "", cpf or "")
    return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def validar_email(email: str) -> bool:
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(padrao, email or "") is not None


def garantir_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CSV_HEADER)


@app.route("/", methods=["GET", "POST"])
def index():
    valores = {"nome": "", "cpf": "", "email": ""}

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        email = request.form.get("email", "").strip()
        valores = {"nome": nome, "cpf": cpf, "email": email}

        erros = []
        if len(nome) < 3:
            erros.append("Informe o nome completo.")
        if not validar_cpf(cpf):
            erros.append("CPF inválido. Confira os números digitados.")
        if not validar_email(email):
            erros.append("E-mail inválido.")

        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("index.html", valores=valores)

        garantir_csv()
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                nome,
                formatar_cpf(cpf),
                email,
                datetime.now().isoformat(timespec="seconds"),
            ])

        return redirect(url_for("sucesso"))

    return render_template("index.html", valores=valores)


@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")


@app.route("/admin/exportar")
def exportar_csv():
    """Baixa o CSV completo. Protegido por um token simples via query string.

    Uso: /admin/exportar?token=SEU_TOKEN
    Isso NÃO é segurança de produção — é só o suficiente para uma demo de aula.
    Para dados reais, troque por autenticação de verdade (login, HTTPS obrigatório etc).
    """
    if request.args.get("token", "") != ADMIN_TOKEN:
        return "Acesso negado.", 403

    garantir_csv()
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        conteudo = f.read()

    return Response(
        conteudo,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=cadastros.csv"},
    )


if __name__ == "__main__":
    garantir_csv()
    # host="0.0.0.0" para aceitar conexões de fora do localhost (necessário ao publicar)
    app.run(debug=True, host="0.0.0.0", port=5000)
