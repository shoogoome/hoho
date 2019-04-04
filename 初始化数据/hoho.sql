-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： db
-- 生成日期： 2019-04-02 06:41:04
-- 服务器版本： 10.2.18-MariaDB-1:10.2.18+maria~bionic
-- PHP 版本： 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `hoho`
--

--
-- 转存表中的数据 `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$120000$jm3N2LjbJ0wO$g47GxsRoGaKuUChTbNzd73oa2jndg+OvvUhHzP15m5I=', '2019-04-02 06:39:00.000000', 1, '121', '', '', 'shoogoome@sina.com', 1, 1, '2019-01-26 03:44:00.000000'),
(2, 'pbkdf2_sha256$120000$PVu5oSto91Bp$VlVKPjc5acvH3UUBcxLiCeLPemPE4HmrP/MJl86Jmy8=', NULL, 1, 'root', '', '', '', 1, 1, '2019-04-02 06:40:00.000000');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
