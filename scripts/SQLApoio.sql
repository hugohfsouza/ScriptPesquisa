select * from controle;
select distinct * from repositorios;	
select * from pull_requests;
select COUNT(1) from pull_request_files

select * from users 

select * from users where login = 'ileler'


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
    not exists (select 1 from pull_request_files where pr_id = pr.id)


select * from startstop


select * from pull_requests limit 1

select count(1) from pull_request_files where pr_id = 1

select sum(additions), sum(deletions) from pull_request_files where pr_id = 1

select distinct user from pull_requests

SELECT count(1) from pull_requests where pr_analisado = 1 and qtdAdditions is null

select `name` from users where id between 1 and 10 and idGithub is null

select * from users 

