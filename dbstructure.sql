-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: databases_mariadb
-- Generation Time: Feb 27, 2022 at 05:18 PM
-- Server version: 10.6.5-MariaDB-1:10.6.5+maria~focal
-- PHP Version: 8.0.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wooden_parachute`
--

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `device_id` int(11) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `friendly_name` text NOT NULL,
  `date_create` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `staticapp_ntp`
--

CREATE TABLE `staticapp_ntp` (
  `ntp_id` int(11) NOT NULL,
  `friendly_name` int(11) NOT NULL,
  `device_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `target_address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `staticapp_webcontent`
--

CREATE TABLE `staticapp_webcontent` (
  `content_id` int(11) NOT NULL,
  `friendly_name` text NOT NULL COMMENT 'Friendly name to show in the GUI',
  `enabled` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'BOOL: enable or disable this check',
  `device_id` int(11) NOT NULL,
  `url` text NOT NULL COMMENT 'URL',
  `resolve` text DEFAULT NULL COMMENT 'OPT: host:port, provide curl a hostname:port, useful for when providing a URL of an ip address',
  `dns-servers` text DEFAULT '\'1.1.1.2,1.0.0.2\'' COMMENT 'Opt: DNS servers to use instead of system defaults',
  `doh-url` text DEFAULT '\'https://cloudflare-dns.com/dns-query\'' COMMENT 'Opt: Use DNS-over-HTTPS server instead of system',
  `insecure` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Opt: Ignore invaild SSL certs',
  `referer` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'Opt BOOL: Provide referer URL to content check in system',
  `retry` int(11) NOT NULL DEFAULT 3 COMMENT 'Number of retries',
  `retry_connrefused` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'OPT: Add connection refused to retry reasons',
  `retry_delay` int(11) NOT NULL DEFAULT 3 COMMENT 'Delay between retries',
  `date_create` datetime NOT NULL DEFAULT current_timestamp(),
  `date_modify` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `staticapp_webcontent_data`
--

CREATE TABLE `staticapp_webcontent_data` (
  `content_data_id` int(11) NOT NULL,
  `content_id` int(11) NOT NULL,
  `data` text NOT NULL,
  `data2` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`device_id`),
  ADD UNIQUE KEY `UNIQUE` (`device_id`) USING BTREE,
  ADD KEY `parent_id` (`parent_id`);

--
-- Indexes for table `staticapp_ntp`
--
ALTER TABLE `staticapp_ntp`
  ADD PRIMARY KEY (`ntp_id`),
  ADD KEY `ntp_to_device` (`device_id`);

--
-- Indexes for table `staticapp_webcontent`
--
ALTER TABLE `staticapp_webcontent`
  ADD PRIMARY KEY (`content_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Indexes for table `staticapp_webcontent_data`
--
ALTER TABLE `staticapp_webcontent_data`
  ADD PRIMARY KEY (`content_data_id`),
  ADD KEY `content_id` (`content_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `device_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `staticapp_ntp`
--
ALTER TABLE `staticapp_ntp`
  MODIFY `ntp_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `staticapp_webcontent`
--
ALTER TABLE `staticapp_webcontent`
  MODIFY `content_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `staticapp_webcontent_data`
--
ALTER TABLE `staticapp_webcontent_data`
  MODIFY `content_data_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `device_to_webcontent` FOREIGN KEY (`device_id`) REFERENCES `staticapp_webcontent` (`device_id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `staticapp_ntp`
--
ALTER TABLE `staticapp_ntp`
  ADD CONSTRAINT `ntp_to_device` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `staticapp_webcontent`
--
ALTER TABLE `staticapp_webcontent`
  ADD CONSTRAINT `webcontent_to_devices` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `webcontent_to_webcontentdata` FOREIGN KEY (`content_id`) REFERENCES `staticapp_webcontent_data` (`content_id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `staticapp_webcontent_data`
--
ALTER TABLE `staticapp_webcontent_data`
  ADD CONSTRAINT `webcontentdata_to_webcontent` FOREIGN KEY (`content_id`) REFERENCES `staticapp_webcontent` (`content_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
