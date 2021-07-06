select * from controle;
select distinct * from repositorios;	
select * from pull_requests;
select * from repositorios where temTeste is not null;
select * from repositorios where temTeste = 1 and prs_recuperados is null
select * from pull_requests;
select * from repositorios where temTeste is not null;


--  30 projetos com o maior número de PRs
select r.id, r.nameWithOwner, count(1) from repositorios as r
    inner join pull_requests as pr on (r.id = pr.repo_id)
    where r.temTeste = 1
group by r.id, r.nameWithOwner
order by 3 desc
limit 30;

-- Quantidade de PRs para analisar
select sum(table1.qtd) from (
select r.id, r.nameWithOwner, count(1) as qtd from repositorios as r
    inner join pull_requests as pr on (r.id = pr.repo_id)
    where r.temTeste = 1
group by r.id, r.nameWithOwner
order by 3 desc
limit 30
) as table1;



-- PR que precisam ser analisados ainda
SELECT b.* from repositorios as a
inner join pull_requests as b on (a.id = b.repo_id)
where a.temTeste = 1
	and a.prs_recuperados = 1
	and b.pr_analisado = 0
limit 1;



SELECT b.* from repositorios as a
	inner join pull_requests as b on (a.id = b.repo_id)
	where a.temTeste = 1
	and a.prs_recuperados = 1
	and b.pr_analisado = 0
	and a.id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)
    and b.id > 0
	order by id 
    limit 12852;
                    

SELECT NOW(), count(1) from repositorios as a
	inner join pull_requests as b on (a.id = b.repo_id)
	where a.temTeste = 1
	and a.prs_recuperados = 1
	and b.pr_analisado = 0
	and a.id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559);




select 
	repo.id, 
    repo.nameWithOwner, 
     pr.user, 
     us.name, 
     us.company, 
     us.location,
     us.email,
     us.twitter_username,
    sum(hasCode) as qtdPRsCodigo, 
    sum(hasTest) as qtdPRsTest,
    count(1) as qtdPRsUser
from pull_requests pr
	inner join repositorios repo on (repo.id = pr.repo_id)
    inner join users us on (us.login = pr.user)
    where pr.repo_id in (1657,1432,1231,1750,1190,1286,909,1549,982,1032,1371,987,1215,1716,1080,928,1010,1504,1094,1559,991,1384,1486,1000,1129,1727,1303,919,901,1174)
    group by  repo.id, 
		 repo.nameWithOwner, 
		 pr.user, 
		 us.name, 
		 us.company, 
		 us.location,
		 us.email,
		 us.twitter_username;



-- quantidade de pr por usuário
select r.id, r.nameWithOwner, count(1) from repositorios as r
    inner join pull_requests as pr on (r.id = pr.repo_id)
    where r.temTeste = 1
group by r.id, r.nameWithOwner
order by 3 desc
limit 30;


select count(1) from repositorios as r
    inner join pull_requests as pr on (r.id = pr.repo_id)
    inner join pull_request_files as prf on (pr.id = prf.pr_id)
    where r.temTeste = 1
    and r.id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592);
    
-- JAVA
-- 1657,1432,1231,1750,1190,1286,909,1549,982,1032,1371,987,1215,1716,1080,928,1010,1504,1094,1559,991,1384,1486,1000,1129,1727,1303,919,901,1174

-- Python
-- 1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559

-- Javascript
-- 1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592

SELECT * from repositorios
	where temTeste = 1
	and prs_analisados is null
	and id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)


SELECT * from repositorios
                    where temTeste = 1
                    and prs_analisados is null
                    and id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)


select * from pull_requests


SET SQL_SAFE_UPDATES=0;
update pull_requests set pr_analisado = null where 1=1;

-- PYTHON
	SELECT *  from 
		pull_requests 
	where repo_id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)
	and state <> 'open'
	and closed_at is null;

	SELECT *  from 
		pull_requests 
	where repo_id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)
	and hasTest is null
    
-- JAVASCRIPT
	SELECT *  from 
		pull_requests 
	where repo_id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)
	and state <> 'open'
	and closed_at is null;

	SELECT *  from 
		pull_requests 
	where repo_id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)
	and hasTest is null


SELECT distinct
	pr.user
from pull_requests pr
	where pr.repo_id in (1657,1432,1231,1750,1190,1286,909,1549,982,1032,1371,987,1215,1716,1080,928,1010,1504,1094,1559,991,1384,1486,1000,1129,1727,1303,919,901,1174)
	and (hasCode = 1 or hasTest = 1)
	order by pr.user
    
    
    select 
	r.id, 
    r.nameWithOwner, 
    count(1) 
from repositorios as r
    inner join pull_requests as pr on (r.id = pr.repo_id)
    where r.temTeste = 1
group by r.id, r.nameWithOwner
order by 3 desc
limit 30;

select count(1) from users
