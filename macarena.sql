-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Jul 17, 2022 at 04:42 PM
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
-- Table structure for table `profitable`
--

CREATE TABLE `profitable` (
  `id` int NOT NULL,
  `token` varchar(128) DEFAULT NULL,
  `tokenid` int DEFAULT NULL,
  `buy_date` varchar(7) DEFAULT NULL,
  `buy_price` float DEFAULT NULL,
  `buy_gas` float DEFAULT NULL,
  `sell_date` varchar(7) DEFAULT NULL,
  `sell_price` float DEFAULT NULL,
  `sell_gas` float DEFAULT NULL,
  `profit` float DEFAULT NULL,
  `profit_percent` float DEFAULT NULL
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
-- Stand-in structure for view `vw_token_id`
-- (See below for the actual view)
--
CREATE TABLE `vw_token_id` (
`tokenID` int
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_trx_wallets`
-- (See below for the actual view)
--
CREATE TABLE `vw_trx_wallets` (
`hash` varchar(128)
,`mmmm` varchar(2)
,`timestamp` datetime
,`token` text
,`tokenID` int
,`trx_value` double
,`tx_action` varchar(4)
,`tx_block` int
,`tx_from` varchar(128)
,`tx_gas` double
,`tx_to` varchar(128)
,`tx_total` double
,`tx_value` float
,`yyyy` varchar(4)
);

-- --------------------------------------------------------

--
-- Table structure for table `wallets`
--

CREATE TABLE `wallets` (
  `wallet` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure for view `vw_tokens`
--
DROP TABLE IF EXISTS `vw_tokens`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `vw_tokens`  AS SELECT DISTINCT `trx`.`token` AS `token` FROM `trx``trx`  ;

-- --------------------------------------------------------

--
-- Structure for view `vw_token_id`
--
DROP TABLE IF EXISTS `vw_token_id`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `vw_token_id`  AS SELECT DISTINCT `trx`.`tokenID` AS `tokenID` FROM `trx``trx`  ;

-- --------------------------------------------------------

--
-- Structure for view `vw_trx_wallets`
--
DROP TABLE IF EXISTS `vw_trx_wallets`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `vw_trx_wallets`  AS SELECT `a`.`timestamp` AS `timestamp`, date_format(`a`.`timestamp`,'%Y') AS `yyyy`, date_format(`a`.`timestamp`,'%m') AS `mmmm`, `a`.`hash` AS `hash`, `a`.`tx_block` AS `tx_block`, `a`.`tx_from` AS `tx_from`, `a`.`tx_to` AS `tx_to`, if(`a`.`tx_from` in (select `wallets`.`wallet` from `wallets`),'SELL','BUY') AS `tx_action`, `a`.`tokenID` AS `tokenID`, `a`.`token` AS `token`, `a`.`tx_value` AS `tx_value`, (`a`.`tx_gas` * 0.000000001) AS `tx_gas`, (`a`.`tx_value` + (`a`.`tx_gas` * 0.000000001)) AS `tx_total`, if(`a`.`tx_from` in (select `wallets`.`wallet` from `wallets`),`a`.`tx_value`,(-(1) * `a`.`tx_value`)) AS `trx_value` FROM `trx` AS `a``a`  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ether_trx`
--
ALTER TABLE `ether_trx`
  ADD PRIMARY KEY (`hash`);

--
-- Indexes for table `profitable`
--
ALTER TABLE `profitable`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trx`
--
ALTER TABLE `trx`
  ADD PRIMARY KEY (`hash`);

--
-- Indexes for table `wallets`
--
ALTER TABLE `wallets`
  ADD UNIQUE KEY `wallet` (`wallet`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `profitable`
--
ALTER TABLE `profitable`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
