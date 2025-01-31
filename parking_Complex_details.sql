-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: localhost    Database: parking
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Complex_details`
--

DROP TABLE IF EXISTS `Complex_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Complex_details` (
  `Complex_ID` int NOT NULL AUTO_INCREMENT,
  `Complex_Name` varchar(50) DEFAULT NULL,
  `Complex_Address` varchar(150) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `Pincode` int DEFAULT NULL,
  `floors` int DEFAULT NULL,
  `Hourly_Charges` float DEFAULT NULL,
  `grace_time` float DEFAULT NULL,
  `isactive` bit(1) DEFAULT b'1',
  `Createdby` char(9) DEFAULT NULL,
  `Createddate` date DEFAULT NULL,
  `Modifiedby` char(9) DEFAULT NULL,
  `modifieddate` date DEFAULT NULL,
  PRIMARY KEY (`Complex_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Complex_details`
--

LOCK TABLES `Complex_details` WRITE;
/*!40000 ALTER TABLE `Complex_details` DISABLE KEYS */;
INSERT INTO `Complex_details` VALUES (1,'LULU','Tambaram','Chennai',600126,3,60,10,_binary '','23abc1338','2024-12-27',NULL,NULL);
/*!40000 ALTER TABLE `Complex_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-31 15:56:51
