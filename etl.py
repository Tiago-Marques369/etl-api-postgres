import requests
import pandas as pd
from sqlalchemy import create_engine
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# 1. Extrair da API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd", 
    "per_page": 10, 
    "page": 1,
    "order": "market_cap_desc"
}
response = requests.get(url, params=params)
data = response.json()

# 2. Salvar JSON localmente
os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_filename = f"data/crypto_prices_{timestamp}.json"

with open(json_filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ JSON salvo em: {json_filename}")

# 3. Transformar e salvar CSV
df = pd.DataFrame(data)[["id", "symbol", "current_price", "market_cap", "total_volume"]]
csv_filename = f"data/crypto_prices_{timestamp}.csv"
df.to_csv(csv_filename, index=False)
print(f"✅ CSV salvo em: {csv_filename}")

# 4. Carregar no banco (AGORA COM VARIÁVEIS DE AMBIENTE)
try:
    # Buscar variáveis do ambiente
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS") 
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # Se não tiver senha
    if DB_PASS:
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        connection_string = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(connection_string)
    df.to_sql("crypto_prices", engine, if_exists="append", index=False)

    print("✅ Pipeline executado com sucesso!")
    print(f"✅ {len(df)} registros inseridos na tabela crypto_prices")
    
except Exception as e:
    print(f"❌ Erro ao conectar com o banco: {e}")
    print("⚠️  Dados salvos localmente, mas não foram inseridos no banco")

print("\n📊 Preview dos dados:")
print(df.head())