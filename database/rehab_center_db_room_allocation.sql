-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: rehab_center_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `room_allocation`
--

DROP TABLE IF EXISTS `room_allocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_allocation` (
  `allocation_id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `bed_number` int NOT NULL,
  `allocation_date` date NOT NULL,
  `release_date` date DEFAULT NULL,
  `status` varchar(30) NOT NULL,
  PRIMARY KEY (`allocation_id`),
  KEY `room_id` (`room_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `room_allocation_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`),
  CONSTRAINT `room_allocation_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_allocation`
--

LOCK TABLES `room_allocation` WRITE;
/*!40000 ALTER TABLE `room_allocation` DISABLE KEYS */;
INSERT INTO `room_allocation` VALUES (1,1,1,1,'2025-11-01',NULL,'Active'),(2,2,2,3,'2025-11-10',NULL,'Active'),(3,6,3,1,'2025-10-25',NULL,'Active'),(4,9,4,2,'2025-12-05',NULL,'Active'),(5,14,5,2,'2025-10-01','2025-12-15','Released'),(6,15,6,1,'2025-09-15','2025-12-05','Released'),(7,4,7,1,'2025-12-10',NULL,'Active'),(8,7,8,1,'2025-11-05',NULL,'Active'),(9,10,9,3,'2025-10-15',NULL,'Active'),(10,16,10,4,'2025-12-01',NULL,'Active');
/*!40000 ALTER TABLE `room_allocation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-16  9:54:49
