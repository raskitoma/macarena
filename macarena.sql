-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Jul 17, 2022 at 12:12 AM
-- Server version: 8.0.29
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `macarena`
--

-- --------------------------------------------------------

--
-- Table structure for table `ether_trx`
--

CREATE TABLE `ether_trx` (
  `hash` varchar(128) NOT NULL,
  `blockNumber` int DEFAULT NULL,
  `timeStamp` datetime DEFAULT NULL,
  `from` varchar(128) DEFAULT NULL,
  `to` varchar(128) DEFAULT NULL,
  `contractAddress` varchar(128) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `gas` float DEFAULT NULL,
  `gasPrice` float DEFAULT NULL,
  `gasUsed` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trx`
--

CREATE TABLE `trx` (
  `hash` varchar(128) NOT NULL,
  `tx_block` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `tx_from` varchar(128) DEFAULT NULL,
  `tx_to` varchar(128) DEFAULT NULL,
  `tokenID` int DEFAULT NULL,
  `token` text,
  `tx_value` float DEFAULT NULL,
  `tx_gas` float DEFAULT NULL,
  `tx_gas_price` float DEFAULT NULL,
  `tx_gas_used` float DEFAULT NULL,
  `nft_symbol` varchar(128) DEFAULT NULL,
  `nft_address` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_tokens`
-- (See below for the actual view)
--
CREATE TABLE `vw_tokens` (
`token` text
);

-- --------------------------------------------------------

--
-- Structure for view `vw_tokens`
--
DROP TABLE IF EXISTS `vw_tokens`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `vw_tokens`  AS SELECT DISTINCT `trx`.`token` AS `token` FROM `trx``trx`  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ether_trx`
--
ALTER TABLE `ether_trx`
  ADD PRIMARY KEY (`hash`);

--
-- Indexes for table `trx`
--
ALTER TABLE `trx`
  ADD PRIMARY KEY (`hash`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
