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
-- Table structure for table `Emp_details`
--

DROP TABLE IF EXISTS `Emp_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Emp_details` (
  `EMP_ID` char(9) NOT NULL,
  `POS_ID` int NOT NULL,
  `EMP_NAME` varchar(20) NOT NULL,
  `MAIL` varchar(20) DEFAULT NULL,
  `PASS` varchar(50) NOT NULL,
  `PH_NO` char(10) DEFAULT NULL,
  `COMPLEX_ID` int NOT NULL,
  `isactive` bit(1) DEFAULT b'1',
  `Createdby` char(9) DEFAULT NULL,
  `Createddate` date DEFAULT NULL,
  `Modifiedby` char(9) DEFAULT NULL,
  `modifieddate` date DEFAULT NULL,
  PRIMARY KEY (`EMP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Emp_details`
--

LOCK TABLES `Emp_details` WRITE;
/*!40000 ALTER TABLE `Emp_details` DISABLE KEYS */;
INSERT INTO `Emp_details` VALUES ('23abc1338',2,'Shuruthi','shuruthi@gmail.com','hello','',1,_binary '','23abc1338','2024-12-27',NULL,NULL),('23abc1736',3,'Manesh','manesh@gmail.com','shuru','7358172600',1,_binary '','Manesh','2024-12-30',NULL,NULL),('23brh1234',3,'Priya','priya@gmail.com','google','8122789407',1,_binary '','23brh1234','2024-12-27',NULL,NULL),('23xyz4567',3,'Gnanavel','abc@gmail.com','abc','1234567890',1,_binary '','Gnanavel','2024-12-29',NULL,NULL);
/*!40000 ALTER TABLE `Emp_details` ENABLE KEYS */;
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
