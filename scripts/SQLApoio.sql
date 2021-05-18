select * from controle;
select * from repositorios;	
select * from pull_requests;
select COUNT(1) from pull_request_files


SET SQL_SAFE_UPDATES = 0;
update repositorios set temTeste = 1 where nameWithOwner = 'mockito/mockito'


select sum(additions) from pull_request_files where pr_id = 1 and filename not like '%test%'

select * from pull_requests where id = 4079
select count(1) from pull_request_files where pr_id = 1
UPDATE `analisegithub`.`pull_requests` SET `pr_analisado` = '0' WHERE (`id` = 189);



select sum(pr.hasTest) as qtdTest, sum(pr.hasCode) as qtdCode from pull_requests pr
	inner join pull_request_files prf on (pr.id = prf.pr_id)
    where pr.repo_id = 35
    and pr.user = 'Yangdaidai'

select pr.user, sum(pr.hasTest) as qtdTest, sum(pr.hasCode) as qtdCode from pull_requests as pr
	where pr.repo_id = 35
    group by pr.user
    having sum(pr.hasTest) > 0
    and  sum(pr.hasCode) <= 0


-- PR que precisam ser analisados ainda
SELECT b.* from repositorios as a
inner join pull_requests as b on (a.id = b.repo_id)
where a.temTeste = 1
	and a.prs_recuperados = 1
	and b.pr_analisado = 0
limit 1


-- ver PRs com 0 arquivos alterados
-- se retornar algo, é pq tem problema
select * from pull_requests as pr
	where 
    pr.repo_id = 1504
    and not exists (select 1 from pull_request_files where pr_id = pr.id)

select count(1) from repositorios where temTeste = 1 and prs_recuperados is null
select * from pull_requests where pr_analisado = 0

select * from startstop
insert into startstop values (0, '')
update startstop set continuar = 1
update startstop set continuar = 0





select *  from pull_request_files limit 1
select count(1) from (select distinct filename from pull_request_files where filename like '%test%') as a

select * from repositorios where temTeste = 1 and nameWithOwner = 'runelite/runelite'
select * 
	from pull_requests



select pr.url, pr.user, pr.number, sum(prf.additions), sum(prf.deletions) 
	from pull_requests as pr
    inner join pull_request_files prf on (pr.id = prf.pr_id)
    where 
		hasTest = 1 
        and hasCode = 0 
	group by pr.url, pr.user, pr.number
	limit 10
    
   