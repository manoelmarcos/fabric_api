import requests
import webbrowser
from flask import Flask, request

# Configurações do Azure AD
TENANT_ID = "6653b20a-edb6-44e9-b25f-e28c14679f1d"
CLIENT_ID = "03f12ddb-c47a-420e-bceb-0e6a8ccdfaad"
CLIENT_SECRET = "O2L8Q~TT6T3pecCHFGRinXB.rqm75a0ib4GfYcLt"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "https://api.fabric.microsoft.com/.default"

# Criar aplicação Flask para capturar o token
app = Flask(__name__)

@app.route('/')
def login():
    auth_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope={SCOPE}"
        f"&state=12345"
    )
    webbrowser.open(auth_url)  # Abre o navegador automaticamente
    return "Por favor, faça login e autorize o aplicativo."

@app.route('/callback')
def callback():
    code = request.args.get("code")
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    # Troca o código de autorização pelo Access Token
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info["access_token"]
    
        print("\n✅ Token obtido com sucesso! Copie e use no seu código:")
        print(access_token, "\n")  # Exibe o token completo no terminal
        return f"✅ Token obtido com sucesso! Use esse token nas requisições: {access_token}"

        # return "✅ Token obtido com sucesso! O token completo foi impresso no terminal."


    else:
        return f"❌ Erro ao obter token: {response.text}"

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(port=5000, debug=True)
