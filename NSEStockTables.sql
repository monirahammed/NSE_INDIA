-- #Author : Moniruddin Ahammed
-- #Email : monirahammed@gmail.com


CREATE DATABASE  IF NOT EXISTS `StockInformation` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `StockInformation`;
-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (i686)
--
-- Host: 127.0.0.1    Database: StockInformation
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

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
-- Table structure for table `TestbulkDeals`
--

DROP TABLE IF EXISTS `TestbulkDeals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TestbulkDeals` (
  `tradeDateText` char(20) NOT NULL,
  `ticker` char(20) NOT NULL,
  `company` char(150) NOT NULL,
  `clientName` char(150) NOT NULL,
  `tradeType` char(10) NOT NULL,
  `tradedQuantity` bigint(20) NOT NULL,
  `avgTradePrice` float NOT NULL,
  `remarks` text,
  `tradeDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `blockDeals`
--

DROP TABLE IF EXISTS `blockDeals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blockDeals` (
  `tradeDateText` char(20) NOT NULL,
  `ticker` char(20) NOT NULL,
  `company` char(150) NOT NULL,
  `clientName` char(150) NOT NULL,
  `tradeType` char(10) NOT NULL,
  `tradedQuantity` bigint(20) NOT NULL,
  `avgTradePrice` float NOT NULL,
  `tradeDate` date DEFAULT NULL,
  UNIQUE KEY `index_blockDeals_unique` (`tradeDateText`,`ticker`,`company`,`clientName`,`tradeType`,`tradedQuantity`,`avgTradePrice`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bulkDeals`
--

DROP TABLE IF EXISTS `bulkDeals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulkDeals` (
  `tradeDateText` char(20) NOT NULL,
  `ticker` char(20) NOT NULL,
  `company` char(150) NOT NULL,
  `clientName` char(150) NOT NULL,
  `tradeType` char(10) NOT NULL,
  `tradedQuantity` bigint(20) NOT NULL,
  `avgTradePrice` float NOT NULL,
  `remarks` text,
  `tradeDate` date DEFAULT NULL,
  UNIQUE KEY `index_bulkDeals_unique` (`tradeDateText`,`ticker`,`company`,`clientName`,`tradeType`,`tradedQuantity`,`avgTradePrice`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dailySecurityPriceInfo`
--

DROP TABLE IF EXISTS `dailySecurityPriceInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dailySecurityPriceInfo` (
  `ticker` char(20) NOT NULL,
  `series` char(4) NOT NULL,
  `openPrice` float NOT NULL,
  `highPrice` float NOT NULL,
  `lowPrice` float NOT NULL,
  `closePrice` float NOT NULL,
  `lastPrice` float NOT NULL,
  `previousClosePrice` float NOT NULL,
  `tradedQuantity` bigint(20) NOT NULL,
  `tradeValue` double NOT NULL,
  `totalNumberOfTrade` bigint(20) NOT NULL,
  `ISIN` char(12) NOT NULL,
  `tradeDate` date NOT NULL,
  PRIMARY KEY (`ticker`,`tradeDate`, `series`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `securityDeliveryInfo`
--

DROP TABLE IF EXISTS `securityDeliveryInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `securityDeliveryInfo` (
  `recordType` int(11) NOT NULL,
  `serialNumber` int(11) NOT NULL,
  `ticker` char(20) NOT NULL,
  `securityType` char(8) NOT NULL,
  `tradedQuantity` bigint(20) NOT NULL,
  `deliveryQuantity` bigint(20) NOT NULL,
  `deliveryPercentage` float NOT NULL,
  `tradeDate` date NOT NULL,
  `settlementDate` date NOT NULL,
  UNIQUE KEY `securityDeliveryInfo_unique_index` (`ticker`,`tradeDate`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stockPriceDaily`
--

DROP TABLE IF EXISTS `stockPriceDaily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stockPriceDaily` (
  `ticker` char(20) NOT NULL,
  `company` char(150) NOT NULL,
  `price_previous` float DEFAULT NULL,
  `price_low` float DEFAULT NULL,
  `price_high` float DEFAULT NULL,
  `volume_daily` bigint(20) DEFAULT NULL,
  `volume_quarter_avg` bigint(20) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `SYMBOL` varchar(20) NOT NULL,
  `SERIES` varchar(20) NOT NULL,
  `OPEN` double NOT NULL,
  `HIGH` double NOT NULL,
  `LOW` double NOT NULL,
  `CLOSE` double NOT NULL,
  `LAST` double NOT NULL,
  `PREVCLOSE` double NOT NULL,
  `TOTTRDQTY` double NOT NULL,
  `TOTTRDVAL` double NOT NULL,
  `TIMESTAMP` varchar(20) NOT NULL,
  `TOTALTRADE` double NOT NULL,
  `ISIN` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-26 11:28:49
