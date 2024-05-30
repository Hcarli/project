SELECT popul, cftp, rtfpna, delta, csh_i from pennworld
JOIN countries
ON country_id=countries.id
WHERE country IN ('Sorbia', 'Rwanda', 'Ukraine', 'Romania', 'Modolvia', 'Lithuania', 'Latvia', 'Kuwait', 'Kazakstan', 'Ireland', 'Estonia', 'Cyprus', 'China', 'Armenia');


SELECT popul, cftp, rtfpna, delta, csh_i from pennworld
JOIN countries
ON country_id=countries.id
WHERE country="Venezuela"
AND year BETWEEN 2015 AND 2019;

UPDATE pennworld
SET csh_i= 0.00000
WHERE country_id= (
    SELECT country_id FROM countries
    WHERE country="Venezuela"
)
AND year=2017;


UPDATE pennworld
SET csh_i= 0.00000
WHERE country_id= (
    SELECT country_id FROM countries
    WHERE country="Venezuela"
)

csh_i = -0.029723395 2017 venezuela


UPDATE countries
SET country="Cote d'Ivoire"
WHERE id=21;
