CREATE TABLE `controle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endCursor` varchar(60) DEFAULT NULL,
  `startCursor` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;


CREATE TABLE `pull_request_files` (
  `pr_id` int(11) NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `sha` varchar(100) NOT NULL,
  UNIQUE KEY `unique_todas` (`pr_id`,`filename`,`additions`,`deletions`,`sha`),
  KEY `ix_01` (`pr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



CREATE TABLE `pull_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo_id` int(11) NOT NULL,
  `github_id` bigint(20) NOT NULL,
  `number` int(11) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `locked` varchar(45) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `user` varchar(200) DEFAULT NULL,
  `user_id` bigint(40) DEFAULT NULL,
  `created_at` varchar(45) DEFAULT NULL,
  `updated_at` varchar(45) DEFAULT NULL,
  `pr_analisado` tinyint(4) DEFAULT '0',
  `hasTest` tinyint(4) DEFAULT NULL,
  `hasCode` tinyint(4) DEFAULT NULL,
  `qtdArqTest` int(11) DEFAULT NULL,
  `qtdArqCode` int(11) DEFAULT NULL,
  `qtdAdditions` int(11) DEFAULT NULL,
  `qtdDeletions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `github_id_UNIQUE` (`github_id`),
  KEY `ix_repo_id` (`repo_id`),
  KEY `ix_primary` (`id`),
  KEY `ix_hasTest` (`hasTest`),
  KEY `ix_hasCode` (`hasCode`),
  KEY `ix_qtd_addictions` (`qtdAdditions`),
  KEY `ix_qtd_deletions` (`qtdDeletions`)
) ENGINE=InnoDB AUTO_INCREMENT=496105 DEFAULT CHARSET=latin1;


CREATE TABLE `startstop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `continuar` tinyint(4) DEFAULT NULL,
  `token` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;



CREATE TABLE `repositorios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `nameWithOwner` varchar(200) DEFAULT NULL,
  `createdAt` varchar(45) DEFAULT NULL,
  `databaseId` bigint(9) DEFAULT NULL,
  `languages` text,
  `temTeste` tinyint(4) DEFAULT NULL,
  `prs_recuperados` tinyint(4) DEFAULT NULL,
  `prs_analisados` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1802 DEFAULT CHARSET=latin1;


-- CREATE TABLE `tokens` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `token` varchar(200) DEFAULT NULL,
--   `qtdRestante` int(11) DEFAULT NULL,
--   `usar` varchar(45) DEFAULT '0',
--   PRIMARY KEY (`id`)
-- ) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;



CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(100) DEFAULT NULL,
  `idGithub` bigint(20) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `blog` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `twitter_username` varchar(255) DEFAULT NULL,
  `public_repos` varchar(255) DEFAULT NULL,
  `public_gists` varchar(255) DEFAULT NULL,
  `followers` bigint(20) DEFAULT NULL,
  `following` bigint(20) DEFAULT NULL,
  `erro` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_name` (`name`),
  KEY `ix_name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;

