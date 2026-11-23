# Issues propostas para cadastro no GitHub

## 1. Implementar coleta da API histórica
**Descrição:** Implementar requisição Open-Meteo com coordenadas, período, variáveis e timezone; tratar falhas HTTP.
**Critério de conclusão:** Execução recupera exatamente 30 datas e registra parâmetros.
**Responsável:** a definir.

## 2. Preservar JSON original
**Descrição:** Salvar resposta sem alterações e metadados da coleta em dados/.
**Critério de conclusão:** JSON íntegro e metadados de origem disponíveis.
**Responsável:** a definir.

## 3. Validar qualidade com pandas
**Descrição:** Implementar as oito checagens do plano e relatório de erros.
**Critério de conclusão:** Testes de duplicatas, lacunas, NULL e inconsistências passam.
**Responsável:** a definir.

## 4. Modelar e carregar DuckDB
**Descrição:** Criar clima_diario com PK (cidade,data) e carga transacional idempotente.
**Critério de conclusão:** Duas execuções consecutivas mantêm 30 linhas sem duplicatas.
**Responsável:** a definir.

## 5. Criar consultas SQL e KPIs
**Descrição:** Implementar AVG máxima, SUM chuva e contagem de dias ≥35 °C com cobertura.
**Critério de conclusão:** Três consultas retornam unidades e n válido.
**Responsável:** a definir.

## 6. Construir dashboard Streamlit
**Descrição:** Criar três cartões, dois gráficos, tabela, fonte e limitações.
**Critério de conclusão:** Painel apresenta os elementos do wireframe com dados do DuckDB.
**Responsável:** a definir.

## 7. Revisar documentação e devolutiva
**Descrição:** Atualizar README, instruções de reprodução e texto de divulgação acessível.
**Critério de conclusão:** Terceiro consegue reproduzir o fluxo e entender limitações.
**Responsável:** a definir.
