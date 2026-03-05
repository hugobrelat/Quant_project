import yfinance as yf
import pandas as pd
import os

# Liste corrigée avec les vrais symboles boursiers
stocks_lists = stocks_lists = ['NVDA','AAPL', 'TSLA','BTC-USD','GC=F','PYPL', 'JPM', 'KO', 'PG','MC.PA','ORA.PA','AC.PA','STLAP.PA' ,'ETH-USD','PFE', 'UNH', 'XOM', 'COST']
folder = "module 6"

if not os.path.exists(folder):
    os.makedirs(folder)

for ticker in stocks_lists:
    print(f"\n--- Téléchargement de {ticker} ---")
    
    # Téléchargement (auto_adjust=True est plus fiable pour les rendements)
    data = yf.download(ticker, start="2015-01-01", end="2026-02-28", auto_adjust=True)
    
    if data.empty:
        print(f"❌ Erreur : Le ticker '{ticker}' est invalide ou délisté.")
        continue

    # On gère le MultiIndex si nécessaire
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Avec auto_adjust=True, la colonne s'appelle 'Close' mais c'est le prix ajusté
    df_filtered = data[['Close']].copy()
    df_filtered.columns = ['Adj Close']
    
    # Sauvegarde
    file_path = os.path.join(folder, f"{ticker}.csv")
    df_filtered.to_csv(file_path)
    print(f"✅ Succès : {len(df_filtered)} lignes sauvegardées pour {ticker}.")

print("\nFichiers prêts pour ton projet Coursera !")