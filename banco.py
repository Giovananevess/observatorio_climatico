"""Valida dados e recria a tabela sem duplicações."""
import json
from pathlib import Path
import pandas as pd
import duckdb

BASE = Path(__file__).resolve().parent
DADOS = BASE / 'dados'

def main():
    raw = json.loads((DADOS / 'open_meteo_original.json').read_text(encoding='utf-8'))
    diario = raw['daily']
    campos = {'time': 'data', 'temperature_2m_min': 'temperatura_min_c',
              'temperature_2m_max': 'temperatura_max_c', 'precipitation_sum': 'precipitacao_mm'}
    if not all(c in diario for c in campos):
        raise ValueError('Faltam campos meteorológicos obrigatórios no JSON')
    df = pd.DataFrame({novo: diario[antigo] for antigo, novo in campos.items()})
    df['data'] = pd.to_datetime(df['data'], errors='raise').dt.date
    for coluna in ['temperatura_min_c', 'temperatura_max_c', 'precipitacao_mm']:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    if len(df) != 30 or df['data'].nunique() != 30:
        raise ValueError(f'Esperados 30 dias únicos; encontrados {len(df)} registros, {df.data.nunique()} dias')
    esperado = pd.date_range('2026-10-01', '2026-10-30').date
    if set(df['data']) != set(esperado):
        raise ValueError('Cobertura de datas incompleta ou fora do período')
    if df['data'].duplicated().any():
        raise ValueError('Datas duplicadas')
    faltantes = df.isna().sum().to_dict()
    if df['precipitacao_mm'].dropna().lt(0).any():
        raise ValueError('Precipitação negativa')
    if (df['temperatura_min_c'] > df['temperatura_max_c']).fillna(False).any():
        raise ValueError('Temperatura mínima maior que máxima')
    df.to_csv(DADOS / 'dados_tratados.csv', index=False)
    con = duckdb.connect(str(DADOS / 'clima.duckdb'))
    try:
        con.execute('BEGIN TRANSACTION')
        con.execute('''CREATE OR REPLACE TABLE clima_diario (
            data DATE PRIMARY KEY,
            temperatura_min_c DOUBLE,
            temperatura_max_c DOUBLE,
            precipitacao_mm DOUBLE
        )''')
        con.register('entrada', df)
        con.execute('INSERT INTO clima_diario SELECT * FROM entrada ORDER BY data')
        con.execute('COMMIT')
        print('Banco carregado:', con.execute('SELECT COUNT(*) FROM clima_diario').fetchone()[0], 'registros')
        print('Valores ausentes (mantidos como NULL):', faltantes)
        print(con.execute('SELECT * FROM clima_diario ORDER BY data LIMIT 5').df().to_string(index=False))
    except Exception:
        con.execute('ROLLBACK')
        raise
    finally:
        con.close()

if __name__ == '__main__':
    main()
