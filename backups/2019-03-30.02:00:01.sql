-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: mysqldb    Database: hoho
-- ------------------------------------------------------
-- Server version	5.5.5-10.2.18-MariaDB-1:10.2.18+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_account`
--

DROP TABLE IF EXISTS `account_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(125) NOT NULL,
  `email_validated` tinyint(1) NOT NULL,
  `sex` smallint(5) unsigned NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `realname` varchar(50) NOT NULL,
  `role` smallint(5) unsigned NOT NULL,
  `phone` varchar(20) NOT NULL,
  `phone_validated` tinyint(1) NOT NULL,
  `avator` varchar(200) NOT NULL,
  `motto` varchar(60) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `permissions` longtext NOT NULL,
  `temp_access_token` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_account`
--

LOCK TABLES `account_account` WRITE;
/*!40000 ALTER TABLE `account_account` DISABLE KEYS */;
INSERT INTO `account_account` VALUES (1,'121@hoho.net',0,0,'121','121',99,'',0,'','',20190324123203.42,20190327132836.8,'{}','121'),(2,'1@hoho.net',0,0,'1','1',0,'',0,'','',20190327132850.652,20190327132850.652,'{}','1'),(3,'2@hoho.net',0,0,'2','2',0,'',0,'','',20190327132901.258,20190327132901.258,'{}','2');
/*!40000 ALTER TABLE `account_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appraising_appraisingscore`
--

DROP TABLE IF EXISTS `appraising_appraisingscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appraising_appraisingscore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `template_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `appraising_appraisin_association_id_12d50fd6_fk_associati` (`association_id`),
  KEY `appraising_appraisin_author_id_7cd9edf0_fk_associati` (`author_id`),
  KEY `appraising_appraisin_template_id_0fcb4b66_fk_appraisin` (`template_id`),
  CONSTRAINT `appraising_appraisin_association_id_12d50fd6_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `appraising_appraisin_author_id_7cd9edf0_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`),
  CONSTRAINT `appraising_appraisin_template_id_0fcb4b66_fk_appraisin` FOREIGN KEY (`template_id`) REFERENCES `appraising_appraisingscoretemplate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appraising_appraisingscore`
--

LOCK TABLES `appraising_appraisingscore` WRITE;
/*!40000 ALTER TABLE `appraising_appraisingscore` DISABLE KEYS */;
/*!40000 ALTER TABLE `appraising_appraisingscore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appraising_appraisingscoretemplate`
--

DROP TABLE IF EXISTS `appraising_appraisingscoretemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appraising_appraisingscoretemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `config` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `appraising_appraisin_association_id_8ed0092b_fk_associati` (`association_id`),
  KEY `appraising_appraisin_author_id_d9ef2d3f_fk_associati` (`author_id`),
  CONSTRAINT `appraising_appraisin_association_id_8ed0092b_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `appraising_appraisin_author_id_d9ef2d3f_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appraising_appraisingscoretemplate`
--

LOCK TABLES `appraising_appraisingscoretemplate` WRITE;
/*!40000 ALTER TABLE `appraising_appraisingscoretemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `appraising_appraisingscoretemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association_association`
--

DROP TABLE IF EXISTS `association_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `association_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `config` longtext NOT NULL,
  `colony` tinyint(1) NOT NULL,
  `repository_size` bigint(20) NOT NULL,
  `choosing_code` varchar(15) NOT NULL,
  `school_id` int(11) NOT NULL,
  `backlog` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `association_association_school_id_67570f57_fk_school_school_id` (`school_id`),
  KEY `association_association_short_name_732e761b` (`short_name`),
  CONSTRAINT `association_association_school_id_67570f57_fk_school_school_id` FOREIGN KEY (`school_id`) REFERENCES `school_school` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association_association`
--

LOCK TABLES `association_association` WRITE;
/*!40000 ALTER TABLE `association_association` DISABLE KEYS */;
INSERT INTO `association_association` VALUES (2,'格兰芬多','格兰芬多1','','','{}',0,2147483648,'39432101',2,'{\"attendance\": {}}',20190329043720.812,20190329043720.887);
/*!40000 ALTER TABLE `association_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association_associationaccount`
--

DROP TABLE IF EXISTS `association_associationaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `association_associationaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(50) NOT NULL,
  `role` smallint(5) unsigned NOT NULL,
  `retire` tinyint(1) NOT NULL,
  `account_id` int(11) NOT NULL,
  `association_id` int(11) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `permissions` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `association_associat_account_id_7dc71d31_fk_account_a` (`account_id`),
  KEY `association_associat_association_id_3bbdc5f9_fk_associati` (`association_id`),
  KEY `association_associat_department_id_7f90c9ac_fk_associati` (`department_id`),
  CONSTRAINT `association_associat_account_id_7dc71d31_fk_account_a` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `association_associat_association_id_3bbdc5f9_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `association_associat_department_id_7f90c9ac_fk_associati` FOREIGN KEY (`department_id`) REFERENCES `association_associationdepartment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association_associationaccount`
--

LOCK TABLES `association_associationaccount` WRITE;
/*!40000 ALTER TABLE `association_associationaccount` DISABLE KEYS */;
INSERT INTO `association_associationaccount` VALUES (2,'121',99,0,1,2,NULL,'{\"interview\": true, \"notice\": true, \"appraising\": true, \"task\": true, \"scheduling\": true, \"repository\": true}',20190329043720.94,20190329043721),(5,'1',1,0,2,2,NULL,'{\"interview\": false, \"notice\": false, \"appraising\": false, \"task\": false, \"scheduling\": false, \"repository\": false}',20190329043720.94,20190329043721);
/*!40000 ALTER TABLE `association_associationaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association_associationattendance`
--

DROP TABLE IF EXISTS `association_associationattendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `association_associationattendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `description` longtext NOT NULL,
  `place` varchar(64) NOT NULL,
  `distance` double NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `association_associat_association_id_07a2677f_fk_associati` (`association_id`),
  KEY `association_associat_author_id_401182cd_fk_associati` (`author_id`),
  CONSTRAINT `association_associat_association_id_07a2677f_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `association_associat_author_id_401182cd_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association_associationattendance`
--

LOCK TABLES `association_associationattendance` WRITE;
/*!40000 ALTER TABLE `association_associationattendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `association_associationattendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association_associationdepartment`
--

DROP TABLE IF EXISTS `association_associationdepartment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `association_associationdepartment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `description` varchar(255) NOT NULL,
  `config` longtext NOT NULL,
  `association_id` int(11) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `association_associat_association_id_0e719162_fk_associati` (`association_id`),
  KEY `association_associationdepartment_short_name_583a043e` (`short_name`),
  CONSTRAINT `association_associat_association_id_0e719162_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association_associationdepartment`
--

LOCK TABLES `association_associationdepartment` WRITE;
/*!40000 ALTER TABLE `association_associationdepartment` DISABLE KEYS */;
/*!40000 ALTER TABLE `association_associationdepartment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `association_associationdepartment_manager`
--

DROP TABLE IF EXISTS `association_associationdepartment_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `association_associationdepartment_manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `associationdepartment_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `association_associationd_associationdepartment_id_fcbb50f1_uniq` (`associationdepartment_id`,`account_id`),
  KEY `association_associat_account_id_ba1258c3_fk_account_a` (`account_id`),
  CONSTRAINT `association_associat_account_id_ba1258c3_fk_account_a` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `association_associat_associationdepartmen_43274ffa_fk_associati` FOREIGN KEY (`associationdepartment_id`) REFERENCES `association_associationdepartment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `association_associationdepartment_manager`
--

LOCK TABLES `association_associationdepartment_manager` WRITE;
/*!40000 ALTER TABLE `association_associationdepartment_manager` DISABLE KEYS */;
/*!40000 ALTER TABLE `association_associationdepartment_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add user',2,'add_user'),(6,'Can change user',2,'change_user'),(7,'Can delete user',2,'delete_user'),(8,'Can view user',2,'view_user'),(9,'Can add permission',3,'add_permission'),(10,'Can change permission',3,'change_permission'),(11,'Can delete permission',3,'delete_permission'),(12,'Can view permission',3,'view_permission'),(13,'Can add group',4,'add_group'),(14,'Can change group',4,'change_group'),(15,'Can delete group',4,'delete_group'),(16,'Can view group',4,'view_group'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add LittlePigHoHo主账户',7,'add_account'),(26,'Can change LittlePigHoHo主账户',7,'change_account'),(27,'Can delete LittlePigHoHo主账户',7,'delete_account'),(28,'Can view LittlePigHoHo主账户',7,'view_account'),(29,'Can add 协会',8,'add_association'),(30,'Can change 协会',8,'change_association'),(31,'Can delete 协会',8,'delete_association'),(32,'Can view 协会',8,'view_association'),(33,'Can add 协会考勤',9,'add_associationattendance'),(34,'Can change 协会考勤',9,'change_associationattendance'),(35,'Can delete 协会考勤',9,'delete_associationattendance'),(36,'Can view 协会考勤',9,'view_associationattendance'),(37,'Can add 部门',10,'add_associationdepartment'),(38,'Can change 部门',10,'change_associationdepartment'),(39,'Can delete 部门',10,'delete_associationdepartment'),(40,'Can view 部门',10,'view_associationdepartment'),(41,'Can add 协会人事',11,'add_associationaccount'),(42,'Can change 协会人事',11,'change_associationaccount'),(43,'Can delete 协会人事',11,'delete_associationaccount'),(44,'Can view 协会人事',11,'view_associationaccount'),(45,'Can add 学校',12,'add_school'),(46,'Can change 学校',12,'change_school'),(47,'Can delete 学校',12,'delete_school'),(48,'Can view 学校',12,'view_school'),(49,'Can add 协会排班',13,'add_associationscheduling'),(50,'Can change 协会排班',13,'change_associationscheduling'),(51,'Can delete 协会排班',13,'delete_associationscheduling'),(52,'Can view 协会排班',13,'view_associationscheduling'),(53,'Can add 无课表',14,'add_associationcurriculum'),(54,'Can change 无课表',14,'change_associationcurriculum'),(55,'Can delete 无课表',14,'delete_associationcurriculum'),(56,'Can view 无课表',14,'view_associationcurriculum'),(57,'Can add 用户无课表',15,'add_associationaccountcurriculum'),(58,'Can change 用户无课表',15,'change_associationaccountcurriculum'),(59,'Can delete 用户无课表',15,'delete_associationaccountcurriculum'),(60,'Can view 用户无课表',15,'view_associationaccountcurriculum'),(61,'Can add 评分模板',16,'add_appraisingscoretemplate'),(62,'Can change 评分模板',16,'change_appraisingscoretemplate'),(63,'Can delete 评分模板',16,'delete_appraisingscoretemplate'),(64,'Can view 评分模板',16,'view_appraisingscoretemplate'),(65,'Can add 评分',17,'add_appraisingscore'),(66,'Can change 评分',17,'change_appraisingscore'),(67,'Can delete 评分',17,'delete_appraisingscore'),(68,'Can view 评分',17,'view_appraisingscore'),(69,'Can add 报名表模版',18,'add_interviewregistrationtemplate'),(70,'Can change 报名表模版',18,'change_interviewregistrationtemplate'),(71,'Can delete 报名表模版',18,'delete_interviewregistrationtemplate'),(72,'Can view 报名表模版',18,'view_interviewregistrationtemplate'),(73,'Can add 报名表',19,'add_interviewregistration'),(74,'Can change 报名表',19,'change_interviewregistration'),(75,'Can delete 报名表',19,'delete_interviewregistration'),(76,'Can view 报名表',19,'view_interviewregistration'),(77,'Can add 文件',20,'add_repositoryfile'),(78,'Can change 文件',20,'change_repositoryfile'),(79,'Can delete 文件',20,'delete_repositoryfile'),(80,'Can view 文件',20,'view_repositoryfile'),(81,'Can add 任务进度汇报',21,'add_associationtaskreport'),(82,'Can change 任务进度汇报',21,'change_associationtaskreport'),(83,'Can delete 任务进度汇报',21,'delete_associationtaskreport'),(84,'Can view 任务进度汇报',21,'view_associationtaskreport'),(85,'Can add 任务',22,'add_associationtask'),(86,'Can change 任务',22,'change_associationtask'),(87,'Can delete 任务',22,'delete_associationtask'),(88,'Can view 任务',22,'view_associationtask'),(89,'Can add 通知',23,'add_associationnotice'),(90,'Can change 通知',23,'change_associationnotice'),(91,'Can delete 通知',23,'delete_associationnotice'),(92,'Can view 通知',23,'view_associationnotice');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$QdAHslEmJ9jC$vib0ySHgXqDjmTlviU5Ot/fmWIIyu9yumnACO4BqVAs=','2019-03-23 01:36:48.215652',1,'121','','','shoogoome@sina.com',1,1,'2019-01-26 03:44:00.000000'),(2,'pbkdf2_sha256$120000$cgZ6GSGIqvaH$BA9hi1DYEQDmltW0+pgQOolK/tyabLEWNF303OX8Bj8=','2019-03-23 01:37:00.351062',1,'root','','','',1,1,'2019-03-17 07:55:00.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2019-03-17 07:55:07.256984','1','121',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(2,'2019-03-17 07:55:10.502068','1','121',2,'[{\"changed\": {\"fields\": [\"last_login\"]}}]',2,1),(3,'2019-03-17 07:55:22.825992','2','root',1,'[{\"added\": {}}]',2,1),(4,'2019-03-17 07:55:26.707403','2','root',2,'[{\"changed\": {\"fields\": [\"is_staff\", \"is_superuser\"]}}]',2,1),(5,'2019-03-24 12:32:03.432468','1','[1] 昵称：121, 角色：99 ,token: 121',1,'[{\"added\": {}}]',7,2),(6,'2019-03-27 13:13:22.964105','1','[1] 格兰芬多(格兰芬多)',3,'',8,1),(7,'2019-03-27 13:16:12.405083','3','[3] 格兰芬多(格兰芬多)',3,'',8,1),(8,'2019-03-27 13:28:36.805198','1','[1] 昵称：121, 角色：99 ,token: 121',2,'[]',7,1),(9,'2019-03-27 13:28:50.655870','2','[2] 昵称：1, 角色：0 ,token: 1',1,'[{\"added\": {}}]',7,1),(10,'2019-03-27 13:29:01.258394','3','[3] 昵称：2, 角色：0 ,token: 2',1,'[{\"added\": {}}]',7,1),(11,'2019-03-27 13:31:13.087569','4','[4] 0 ',3,'',11,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'account','account'),(1,'admin','logentry'),(17,'appraising','appraisingscore'),(16,'appraising','appraisingscoretemplate'),(8,'association','association'),(11,'association','associationaccount'),(9,'association','associationattendance'),(10,'association','associationdepartment'),(4,'auth','group'),(3,'auth','permission'),(2,'auth','user'),(5,'contenttypes','contenttype'),(19,'interview','interviewregistration'),(18,'interview','interviewregistrationtemplate'),(23,'notice','associationnotice'),(20,'repository','repositoryfile'),(15,'scheduling','associationaccountcurriculum'),(14,'scheduling','associationcurriculum'),(13,'scheduling','associationscheduling'),(12,'school','school'),(6,'sessions','session'),(22,'task','associationtask'),(21,'task','associationtaskreport');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'account','0001_initial','2019-03-17 07:52:23.250259'),(2,'contenttypes','0001_initial','2019-03-17 07:52:23.340044'),(3,'auth','0001_initial','2019-03-17 07:52:23.815123'),(4,'admin','0001_initial','2019-03-17 07:52:23.956499'),(5,'admin','0002_logentry_remove_auto_add','2019-03-17 07:52:23.968104'),(6,'admin','0003_logentry_add_action_flag_choices','2019-03-17 07:52:23.980349'),(7,'school','0001_initial','2019-03-17 07:52:24.037646'),(8,'association','0001_initial','2019-03-17 07:52:24.774703'),(9,'appraising','0001_initial','2019-03-17 07:52:25.256256'),(10,'contenttypes','0002_remove_content_type_name','2019-03-17 07:52:25.344686'),(11,'auth','0002_alter_permission_name_max_length','2019-03-17 07:52:25.387622'),(12,'auth','0003_alter_user_email_max_length','2019-03-17 07:52:25.439437'),(13,'auth','0004_alter_user_username_opts','2019-03-17 07:52:25.461467'),(14,'auth','0005_alter_user_last_login_null','2019-03-17 07:52:25.516528'),(15,'auth','0006_require_contenttypes_0002','2019-03-17 07:52:25.530080'),(16,'auth','0007_alter_validators_add_error_messages','2019-03-17 07:52:25.552072'),(17,'auth','0008_alter_user_username_max_length','2019-03-17 07:52:25.598554'),(18,'auth','0009_alter_user_last_name_max_length','2019-03-17 07:52:25.643133'),(19,'interview','0001_initial','2019-03-17 07:52:25.865655'),(20,'notice','0001_initial','2019-03-17 07:52:26.259643'),(21,'repository','0001_initial','2019-03-17 07:52:26.409083'),(22,'scheduling','0001_initial','2019-03-17 07:52:26.895791'),(23,'sessions','0001_initial','2019-03-17 07:52:26.983633'),(24,'task','0001_initial','2019-03-17 07:52:27.430659'),(25,'account','0002_auto_20190317_0753','2019-03-17 07:53:48.177767'),(26,'account','0003_auto_20190327_1232','2019-03-27 12:34:17.761946'),(27,'appraising','0002_remove_appraisingscoretemplate_manager','2019-03-27 12:34:17.818374'),(28,'association','0002_auto_20190327_1232','2019-03-27 12:34:17.979740'),(29,'notice','0002_remove_associationnotice_manager','2019-03-27 12:34:18.007617'),(30,'scheduling','0002_remove_associationscheduling_manager','2019-03-27 12:34:18.035004'),(31,'association','0003_auto_20190327_1235','2019-03-27 12:35:13.733860'),(32,'association','0004_auto_20190329_0437','2019-03-29 04:37:21.184723'),(33,'interview','0002_auto_20190329_0437','2019-03-29 04:37:21.319848'),(34,'repository','0002_repositoryfile_update_time','2019-03-29 04:37:21.422042'),(35,'scheduling','0003_auto_20190329_0437','2019-03-29 04:37:21.653549'),(36,'school','0002_auto_20190329_0437','2019-03-29 04:37:21.769665'),(37,'account','0004_auto_20190329_2346','2019-03-29 23:46:43.549899'),(38,'appraising','0003_auto_20190329_2346','2019-03-29 23:46:43.714687'),(39,'association','0005_auto_20190329_2346','2019-03-29 23:46:44.272523'),(40,'interview','0003_auto_20190329_2346','2019-03-29 23:46:44.516948'),(41,'notice','0003_auto_20190329_2346','2019-03-29 23:46:44.649415'),(42,'repository','0003_auto_20190329_2346','2019-03-29 23:46:44.779358'),(43,'scheduling','0004_auto_20190329_2346','2019-03-29 23:46:45.073742'),(44,'school','0003_auto_20190329_2346','2019-03-29 23:46:45.161118'),(45,'task','0002_auto_20190329_2346','2019-03-29 23:46:45.358772');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('27nd8s56z4bg30hv16nbf4f9iksye01w','NGExNjBiMzQxOWEzNzg5NGYxOGVlOWMwZWM1NzVlOGY3NWY1ZTMxZjp7IkhvSG9fc2Vzc2lvbl9pZCI6MX0=','2019-04-10 13:35:59.774558'),('qs8k1cr2jq0sqnbhxm1xp9ri22gsw8yf','ODI0NTJiNjU4ZDE3MjcxZDdmN2M3OWI0YTNlNGE3Mzc3ZTAyZDAzNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjUwNGI2NzlkNTQ0ZTcwOWUxNDY1YzQ3ZWRmZTY4NDBkOGNlZGYxY2YiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-03-31 07:55:07.265307'),('vsabt878yzv17wtbgmabzjdiesb8ex56','YzgwYTk3ODY3NDBlMTRlNTQ2NzEyOTJhNTY2NTQ4ODdjY2NhYTJiMTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg3ZTU0NjdiNGY1NDhiY2Y1NWYyYjgzZDBkNWRkMzkyYTI0MzAyMjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2019-04-06 01:37:00.353342');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_interviewregistration`
--

DROP TABLE IF EXISTS `interview_interviewregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interview_interviewregistration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `additional` longtext NOT NULL,
  `eliminate` tinyint(1) NOT NULL,
  `account_id` int(11) NOT NULL,
  `association_id` int(11) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interview_interviewr_account_id_5ea617fe_fk_account_a` (`account_id`),
  KEY `interview_interviewr_association_id_6372a9ba_fk_associati` (`association_id`),
  CONSTRAINT `interview_interviewr_account_id_5ea617fe_fk_account_a` FOREIGN KEY (`account_id`) REFERENCES `account_account` (`id`),
  CONSTRAINT `interview_interviewr_association_id_6372a9ba_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_interviewregistration`
--

LOCK TABLES `interview_interviewregistration` WRITE;
/*!40000 ALTER TABLE `interview_interviewregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview_interviewregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_interviewregistrationtemplate`
--

DROP TABLE IF EXISTS `interview_interviewregistrationtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interview_interviewregistrationtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `additional` longtext NOT NULL,
  `using` tinyint(1) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interview_interviewr_association_id_c61ef95d_fk_associati` (`association_id`),
  CONSTRAINT `interview_interviewr_association_id_c61ef95d_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_interviewregistrationtemplate`
--

LOCK TABLES `interview_interviewregistrationtemplate` WRITE;
/*!40000 ALTER TABLE `interview_interviewregistrationtemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview_interviewregistrationtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notice_associationnotice`
--

DROP TABLE IF EXISTS `notice_associationnotice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice_associationnotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `start_time` double NOT NULL,
  `end_time` double NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notice_associationno_association_id_7d45f8fb_fk_associati` (`association_id`),
  KEY `notice_associationno_author_id_6b2c5763_fk_associati` (`author_id`),
  KEY `notice_associationno_department_id_5842138b_fk_associati` (`department_id`),
  CONSTRAINT `notice_associationno_association_id_7d45f8fb_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `notice_associationno_author_id_6b2c5763_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`),
  CONSTRAINT `notice_associationno_department_id_5842138b_fk_associati` FOREIGN KEY (`department_id`) REFERENCES `association_associationdepartment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notice_associationnotice`
--

LOCK TABLES `notice_associationnotice` WRITE;
/*!40000 ALTER TABLE `notice_associationnotice` DISABLE KEYS */;
/*!40000 ALTER TABLE `notice_associationnotice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repository_repositoryfile`
--

DROP TABLE IF EXISTS `repository_repositoryfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repository_repositoryfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `path` varchar(200) NOT NULL,
  `create_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `repository_repositor_association_id_25131eb3_fk_associati` (`association_id`),
  KEY `repository_repositor_author_id_ce423563_fk_associati` (`author_id`),
  CONSTRAINT `repository_repositor_association_id_25131eb3_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `repository_repositor_author_id_ce423563_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repository_repositoryfile`
--

LOCK TABLES `repository_repositoryfile` WRITE;
/*!40000 ALTER TABLE `repository_repositoryfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `repository_repositoryfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduling_associationaccountcurriculum`
--

DROP TABLE IF EXISTS `scheduling_associationaccountcurriculum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduling_associationaccountcurriculum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `account_id` int(11) NOT NULL,
  `curriculum_id` int(11) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scheduling_associati_account_id_a2914b19_fk_associati` (`account_id`),
  KEY `scheduling_associati_curriculum_id_9c642c7d_fk_schedulin` (`curriculum_id`),
  CONSTRAINT `scheduling_associati_account_id_a2914b19_fk_associati` FOREIGN KEY (`account_id`) REFERENCES `association_associationaccount` (`id`),
  CONSTRAINT `scheduling_associati_curriculum_id_9c642c7d_fk_schedulin` FOREIGN KEY (`curriculum_id`) REFERENCES `scheduling_associationcurriculum` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduling_associationaccountcurriculum`
--

LOCK TABLES `scheduling_associationaccountcurriculum` WRITE;
/*!40000 ALTER TABLE `scheduling_associationaccountcurriculum` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduling_associationaccountcurriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduling_associationcurriculum`
--

DROP TABLE IF EXISTS `scheduling_associationcurriculum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduling_associationcurriculum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `school_id` int(11) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scheduling_associati_school_id_9de18126_fk_school_sc` (`school_id`),
  CONSTRAINT `scheduling_associati_school_id_9de18126_fk_school_sc` FOREIGN KEY (`school_id`) REFERENCES `school_school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduling_associationcurriculum`
--

LOCK TABLES `scheduling_associationcurriculum` WRITE;
/*!40000 ALTER TABLE `scheduling_associationcurriculum` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduling_associationcurriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduling_associationscheduling`
--

DROP TABLE IF EXISTS `scheduling_associationscheduling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduling_associationscheduling` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `config` longtext NOT NULL,
  `content` longtext NOT NULL,
  `start_time` double NOT NULL,
  `end_time` double NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `scheduling_associati_association_id_dd7dfac8_fk_associati` (`association_id`),
  KEY `scheduling_associati_author_id_2f77c0fe_fk_associati` (`author_id`),
  CONSTRAINT `scheduling_associati_association_id_dd7dfac8_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `scheduling_associati_author_id_2f77c0fe_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduling_associationscheduling`
--

LOCK TABLES `scheduling_associationscheduling` WRITE;
/*!40000 ALTER TABLE `scheduling_associationscheduling` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduling_associationscheduling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_school`
--

DROP TABLE IF EXISTS `school_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `config` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_school`
--

LOCK TABLES `school_school` WRITE;
/*!40000 ALTER TABLE `school_school` DISABLE KEYS */;
INSERT INTO `school_school` VALUES (2,'北京师范大学珠海分校','BNUZ','','xi','{}',20190329043721.66,20190329043721.707),(3,'霍格沃茨魔法学校3','霍格沃茨','','霍格沃茨魔法学校（Hogwarts School of Witchcraft and Wizardry）是欧洲的三大魔法学校之一。学校采用七年学制，所有学生在霍格沃茨学习期间寄宿。圣诞节期间，学生可离校返家，也可选择留校过节；三年级以上学生经监护人签字同意后可以在周末的时候前往霍格莫德村（英国唯一一个全部是巫师的村庄）；暑假期间所有学生必须离开学校。','{}',20190329043721.66,20190329043721.707),(4,'霍格沃茨魔法学校4','霍格沃茨','','霍格沃茨魔法学校（Hogwarts School of Witchcraft and Wizardry）是欧洲的三大魔法学校之一。学校采用七年学制，所有学生在霍格沃茨学习期间寄宿。圣诞节期间，学生可离校返家，也可选择留校过节；三年级以上学生经监护人签字同意后可以在周末的时候前往霍格莫德村（英国唯一一个全部是巫师的村庄）；暑假期间所有学生必须离开学校。','{}',20190329043721.66,20190329043721.707);
/*!40000 ALTER TABLE `school_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_associationtask`
--

DROP TABLE IF EXISTS `task_associationtask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_associationtask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `start_time` double NOT NULL,
  `end_time` double NOT NULL,
  `working` tinyint(1) NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `association_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_associationtask_association_id_2e403dd4_fk_associati` (`association_id`),
  KEY `task_associationtask_author_id_cae85076_fk_associati` (`author_id`),
  KEY `task_associationtask_department_id_c19510d3_fk_associati` (`department_id`),
  CONSTRAINT `task_associationtask_association_id_2e403dd4_fk_associati` FOREIGN KEY (`association_id`) REFERENCES `association_association` (`id`),
  CONSTRAINT `task_associationtask_author_id_cae85076_fk_associati` FOREIGN KEY (`author_id`) REFERENCES `association_associationaccount` (`id`),
  CONSTRAINT `task_associationtask_department_id_c19510d3_fk_associati` FOREIGN KEY (`department_id`) REFERENCES `association_associationdepartment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_associationtask`
--

LOCK TABLES `task_associationtask` WRITE;
/*!40000 ALTER TABLE `task_associationtask` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_associationtask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_associationtaskreport`
--

DROP TABLE IF EXISTS `task_associationtaskreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_associationtaskreport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `summary` longtext NOT NULL,
  `create_time` double NOT NULL,
  `update_time` double NOT NULL,
  `task_id` int(11) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_associationtask_task_id_058d4759_fk_task_asso` (`task_id`),
  KEY `task_associationtask_worker_id_1c0dd69c_fk_associati` (`worker_id`),
  CONSTRAINT `task_associationtask_task_id_058d4759_fk_task_asso` FOREIGN KEY (`task_id`) REFERENCES `task_associationtask` (`id`),
  CONSTRAINT `task_associationtask_worker_id_1c0dd69c_fk_associati` FOREIGN KEY (`worker_id`) REFERENCES `association_associationaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_associationtaskreport`
--

LOCK TABLES `task_associationtaskreport` WRITE;
/*!40000 ALTER TABLE `task_associationtaskreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_associationtaskreport` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-30  2:00:01
