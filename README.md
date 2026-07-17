# cadastro.py — Formulário de Inscrição (Nome, CPF, E-mail → CSV)

Aplicação simples em Flask (100% Python + HTML/CSS, sem JavaScript escrito à
mão) para coletar nome, CPF e e-mail. É só o **servidor** do formulário —
os scripts de automação (Selenium/PyAutoGUI) que os alunos vão rodar ficam
num pacote separado, pensado para ser distribuído pelo Classroom.

## Estrutura

```
cadastro-app/
├── app.py                # rotas Flask, validação de CPF/e-mail, escrita no CSV
├── templates/
│   ├── index.html        # formulário
│   └── sucesso.html      # tela de confirmação
├── static/style.css
├── requirements.txt      # Flask + gunicorn
├── Procfile               # usado por Render/Railway/Heroku-like
└── cadastros.csv          # gerado automaticamente na primeira inscrição
```

Ids relevantes para as automações dos alunos: `#nome`, `#cpf`, `#email`,
`#btn-enviar` e, na tela de sucesso, `#mensagem-sucesso` e `#link-novo-cadastro`.

## Rodando localmente

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse `http://localhost:5000`. Os cadastros vão sendo gravados em
`cadastros.csv` na raiz do projeto.

## Colocando no ar com o seu domínio (grátis, sem precisar guardar nada)

Como é só uma demonstração de aula, você não precisa de banco de dados nem
de disco persistente — o **Render** (plano gratuito "Hobby") resolve bem:
suporta domínio próprio e HTTPS grátis, e como o disco é temporário, os
dados apagados a cada novo deploy não é um problema, é até conveniente
(nada de dado de teste acumulando de uma aula para a outra).

### Passo a passo — Render

1. Suba este projeto para um repositório no GitHub (só o conteúdo desta
   pasta: `app.py`, `templates/`, `static/`, `requirements.txt`, `Procfile`).
2. Em [render.com](https://render.com), crie um **Web Service** novo
   apontando para esse repositório. O Render detecta o `Procfile`
   e instala o `requirements.txt` sozinho.
3. Antes do primeiro deploy, adicione duas variáveis de ambiente (aba
   *Environment* do serviço):
   - `SECRET_KEY` → qualquer texto longo e aleatório.
   - `ADMIN_TOKEN` → outro texto aleatório, só que **este é o que protege a
     rota `/admin/exportar`** — é o que garante que só você, e não os
     alunos, consegue baixar o CSV de saída. Guarde esse valor com você.
4. Depois do deploy, vá em *Settings → Custom Domains* e adicione seu
   domínio (ex.: `cadastro.seudominio.com.br`). O Render te dá um valor de
   **CNAME** para cadastrar no painel DNS do seu domínio.
5. No painel DNS do seu domínio, crie o registro CNAME apontando esse
   subdomínio para o endereço que o Render mostrou. A propagação costuma
   levar de alguns minutos a poucas horas; o certificado HTTPS é emitido
   automaticamente pelo Render depois que o DNS propaga.
6. **Antes da aula**, acesse a URL uma vez alguns minutos antes de começar:
   no plano gratuito o serviço "dorme" depois de 15 minutos sem acesso e
   demora um pouco para acordar na primeira requisição — melhor não deixar
   isso acontecer bem na hora que a turma for acessar.

Isso é o suficiente para a demonstração. Se depois você quiser manter o
projeto rodando por muito tempo com tráfego real, aí sim vale considerar um
plano pago ou trocar o CSV por um banco de dados — mas para uma aula, não é
necessário.

## Protegendo o CSV de saída

Os alunos só precisam acessar o formulário — não o resultado. Por isso:

- A rota `/admin/exportar?token=SEU_TOKEN` é a única forma de baixar
  `cadastros.csv`, e só funciona com o `ADMIN_TOKEN` certo.
- **Troque o `ADMIN_TOKEN` do valor padrão do código** antes de publicar
  (passo 3 acima). Se você deixar o valor padrão, qualquer aluno que abra o
  código-fonte no GitHub consegue baixar os cadastros de todo mundo.
- Não é uma autenticação de verdade (é só um token na URL), mas é mais do
  que suficiente para uma demonstração em aula.

## Sobre coletar CPF de verdade

O formulário fica público e coleta CPF (dado pessoal sensível para fins da
LGPD). Para uma demo isso é tranquilo desde que:

- Ninguém use CPF real de terceiros — os scripts de automação dos alunos já
  usam CPFs fictícios (válidos pelo algoritmo, mas inventados).
- O serviço sirva sempre em HTTPS (o Render já cuida disso automaticamente).
- O `ADMIN_TOKEN` esteja configurado corretamente (seção acima).

## Variação: outros "GUIs" em Python

Este projeto usa Flask + HTML simples de propósito, porque gera elementos de
página previsíveis e é o mais didático para ensinar Selenium (`find_element`
por `id`). Se o foco de uma próxima aula for mais "construir GUI em Python"
do que automação, frameworks como **Streamlit** ou **NiceGUI** também geram
interface web só com Python — só que os elementos da página ficam mais
aninhados/menos previsíveis para automatizar com Selenium sem ajustes
extras.
