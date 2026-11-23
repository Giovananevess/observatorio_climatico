"""Executa os três KPIs e salva evidências verificáveis."""
import json
from pathlib import Path
import duckdb

BASE = Path(__file__).resolve().parent
DADOS = BASE / 'dados'

consultas = {
 'temperatura_maxima_media_c': 'SELECT ROUND(AVG(temperatura_max_c),2) FROM clima_diario',
 'precipitacao_total_mm': 'SELECT ROUND(SUM(precipitacao_mm),2) FROM clima_diario',
 'dias_quentes_35c': 'SELECT COUNT(*) FILTER (WHERE temperatura_max_c >= 35) FROM clima_diario',
}

def main():
    con = duckdb.connect(str(DADOS / 'clima.duckdb'), read_only=True)
    try:
        resultados = {chave: con.execute(sql).fetchone()[0] for chave, sql in consultas.items()}
        resultados['total_registros'] = con.execute('SELECT COUNT(*) FROM clima_diario').fetchone()[0]
        resultados['dias_com_dados_completos'] = con.execute('''SELECT COUNT(*) FROM clima_diario WHERE temperatura_min_c IS NOT NULL AND temperatura_max_c IS NOT NULL AND precipitacao_mm IS NOT NULL''').fetchone()[0]
        resultados['primeiras_linhas'] = con.execute('SELECT * FROM clima_diario ORDER BY data LIMIT 5').df().to_string(index=False)
    finally:
        con.close()
    (DADOS / 'resultados.json').write_text(json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(json.dumps(resultados, ensure_ascii=False, indent=2, default=str))

if __name__ == '__main__':
    main()
