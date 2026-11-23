"""Coleta dados históricos da Open-Meteo e preserva a resposta original."""
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = Path(__file__).resolve().parent
DADOS = BASE / 'dados'
PARAMETROS = {
    'latitude': -20.2833, 'longitude': -50.2467,
    'start_date': '2026-10-01', 'end_date': '2026-10-30',
    'daily': 'temperature_2m_min,temperature_2m_max,precipitation_sum',
    'timezone': 'America/Sao_Paulo',
}
URL = 'https://archive-api.open-meteo.com/v1/archive'

def main():
    DADOS.mkdir(exist_ok=True)
    resposta = requests.get(URL, params=PARAMETROS, timeout=45)
    resposta.raise_for_status()
    payload = resposta.json()
    if 'daily' not in payload:
        raise ValueError(f'Resposta sem daily: {payload}')
    (DADOS / 'open_meteo_original.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    metadata = {'coletado_em_utc': datetime.now(timezone.utc).isoformat(),
                'url': resposta.url, 'parametros': PARAMETROS,
                'fonte': 'Open-Meteo Historical Weather API'}
    (DADOS / 'metadados_coleta.json').write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Coleta concluída:', len(payload['daily']['time']), 'dias')
    print('JSON original salvo em dados/open_meteo_original.json')

if __name__ == '__main__':
    main()
