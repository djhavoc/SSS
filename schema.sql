# Sequel Pro dump
# Version 2492
# http://code.google.com/p/sequel-pro
#
# Host: 127.0.0.1 (MySQL 5.0.77)
# Database: sss
# Generation Time: 2010-09-18 00:09:45 -0400
# ************************************************************

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `results`;

CREATE TABLE `results` (
  `id` int(11) NOT NULL auto_increment,
  `services_id` int(11) default NULL,
  `last_check` datetime default NULL,
  `status` varchar(255) default NULL,
  `status_secondary` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;



# Dump of table services
# ------------------------------------------------------------

DROP TABLE IF EXISTS `services`;

CREATE TABLE `services` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(255) default NULL,
  `kind` varchar(255) default NULL,
  `tcp_port` int(8) default NULL,
  `http_url` varchar(1024) default NULL,
  `db_name` varchar(255) default NULL,
  `db_host` varchar(255) default NULL,
  `db_port` int(8) default NULL,
  `db_user` varchar(255) default NULL,
  `db_pass` blob,
  `tcp_ip` varchar(255) default NULL,
  `ipsec_gateway` varchar(255) default NULL,
  `ipsec_group` varchar(255) default NULL,
  `ipsec_secret` blob,
  `ipsec_user` varchar(255) default NULL,
  `ipsec_pass` blob,
  `ipsec_target_host_ip` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

alter table services add column `icmp_ip` varchar(255) default NULL;
alter table services add column `pop3_ip` varchar(255) default NULL;
alter table services add column `smtp_ip` varchar(255) default NULL;

CREATE TABLE `status` (
  `id` int(255) NOT NULL auto_increment,
  `service_id` int(11) default NULL,
  `status` text,
  `check_date` datetime default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;


/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
