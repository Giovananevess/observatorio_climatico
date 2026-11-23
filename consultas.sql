-- KPI 1: temperatura máxima média (°C)
SELECT ROUND(AVG(temperatura_max_c), 2) AS temperatura_maxima_media_c,
       COUNT(temperatura_max_c) AS dias_validos
FROM clima_diario;

-- KPI 2: precipitação acumulada (mm)
SELECT ROUND(SUM(precipitacao_mm), 2) AS precipitacao_total_mm,
       COUNT(precipitacao_mm) AS dias_validos
FROM clima_diario;

-- KPI 3: número de dias quentes (máxima >= 35 °C)
SELECT COUNT(*) FILTER (WHERE temperatura_max_c >= 35) AS dias_quentes,
       COUNT(temperatura_max_c) AS dias_validos
FROM clima_diario;
