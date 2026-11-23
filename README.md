# Observatório Climático Local — AE2

Projeto acadêmico de coleta, tratamento, armazenamento e análise de dados históricos de Fernandópolis (SP), para apoiar moradores, agricultores e trabalhadores ao ar livre.

> **Importante:** recorte e público-alvo provisórios, pois o planejamento AE1 original não foi fornecido. Confirme a continuidade com o trabalho anterior antes da entrega.

## Fonte e recorte

- Fonte: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- Localidade: Fernandópolis, SP (coordenadas aproximadas: -20.2833, -50.2467)
- Datas: 01/10/2026 a 30/10/2026 (30 dias consecutivos)
- Fuso horário: America/Sao_Paulo
- Variáveis diárias: temperatura mínima (°C), máxima (°C) e precipitação acumulada (mm)
- A Open-Meteo fornece dados históricos modelados/reanalisados; não devem ser descritos como medições diretas de estação local.

## Perguntas e KPIs

1. Qual foi a temperatura máxima média do período? KPI: média das máximas diárias, em °C.
2. Quanto choveu no período? KPI: soma da precipitação diária, em mm.
3. Quantos dias tiveram máxima de pelo menos 35 °C? KPI: contagem de dias, em dias.

## Arquivos

- `coleta.py`: requisição HTTP e salvamento do JSON bruto e metadados.
- `banco.py`: validação com pandas, CSV tratado e carga idempotente em DuckDB.
- `consultas.sql`: três consultas SQL.
- `analise.py`: execução dos KPIs e geração de `dados/resultados.json`.
- `dados/`: arquivos originais, tratados e banco após a execução.
- `docs/escopo-1/AE2/`: relatório acadêmico.

## Como executar (Windows / PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python coleta.py
python banco.py
python analise.py
```

No macOS/Linux: `python3 -m venv .venv`, `source .venv/bin/activate` e `python3` nos comandos.

## Validações e reprodutibilidade

O script exige exatamente 30 datas únicas, cobertura integral do intervalo, tipos numéricos, precipitação não negativa e mínima <= máxima. Valores ausentes são preservados como NULL e informados no terminal. A tabela é recriada em transação a cada execução, evitando duplicações.

## Resultados obtidos

A coleta foi executada para o período de 01/10/2026 a 30/10/2026:

| Indicador | Resultado |
|---|---:|
| Temperatura máxima média | 30,82 °C |
| Precipitação acumulada | 117,20 mm |
| Dias com máxima >= 35 °C | 5 dias |
| Registros no banco | 30 |
| Dias com dados completos | 30 |

Os resultados detalhados estão em `dados/resultados.json`; os dados tratados estão em `dados/dados_tratados.csv` e no banco `dados/clima.duckdb`.

**Evidências para anexar ao relatório:** saída dos três comandos, amostra da tabela, `dados/resultados.json` e metadados da coleta. Substitua os campos pendentes do relatório apenas com os resultados reais.

## Limitações e ética

Série de apenas 30 dias, sujeita a limitações de resolução espacial e qualidade da reanálise. Não permite inferir tendência climática de longo prazo nem prever o tempo futuro. Não há dados pessoais coletados; caso haja devolutiva à comunidade, não publique dados identificáveis sem consentimento.

## GitHub

O projeto pode ser publicado no GitHub com os dados gerados, o código-fonte, as consultas SQL e o relatório acadêmico. Antes do envio, confira o histórico de commits e disponibilize o repositório com permissão de leitura ao professor.
