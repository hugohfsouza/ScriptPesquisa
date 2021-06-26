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
    where pr.repo_id in ('1657', '1432', '1231', '1750', '1190', '1286', '909', '1549', '982', '1032', '1371', '987', '1215', '1716', '1080', '928', '1010', '1504', '1094', '1559', '991', '1384', '1486', '1000', '1129', '1727', '1303', '919', '901', '1174')
    group by  repo.id, 
		 repo.nameWithOwner, 
		 pr.user, 
		 us.name, 
		 us.company, 
		 us.location,
		 us.email,
		 us.twitter_username
    