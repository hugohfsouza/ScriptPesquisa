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


    
