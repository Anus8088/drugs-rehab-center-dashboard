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
-- Table structure for table `medication_records`
--

DROP TABLE IF EXISTS `medication_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medication_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `medicine_id` int NOT NULL,
  `dosage` varchar(50) DEFAULT NULL,
  `administered_by` varchar(100) DEFAULT NULL,
  `admin_date` date NOT NULL,
  `admin_time` time NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`record_id`),
  KEY `patient_id` (`patient_id`),
  KEY `medicine_id` (`medicine_id`),
  CONSTRAINT `medication_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `medication_records_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicines` (`medicine_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medication_records`
--

LOCK TABLES `medication_records` WRITE;
/*!40000 ALTER TABLE `medication_records` DISABLE KEYS */;
INSERT INTO `medication_records` VALUES (1,1,1,'1 Tablet','Staff Nurse','2025-12-16','09:00:00','2025-12-15 21:38:44'),(2,2,1,'1 Tablet','Staff Nurse','2025-12-16','09:00:00','2025-12-15 21:38:44'),(3,7,1,'1 Tablet','Staff Nurse','2025-12-16','09:00:00','2025-12-15 21:38:44'),(4,3,1,'1 Tablet','Staff Nurse','2025-12-16','09:00:00','2025-12-15 21:38:44'),(5,8,1,'1 Tablet','Staff Nurse','2025-12-16','09:00:00','2025-12-15 21:38:44'),(8,15,5,'1 Injection','Dr. Ahmed','2025-12-15','20:00:00','2025-12-15 21:38:44'),(9,10,5,'1 Injection','Dr. Ahmed','2025-12-15','20:00:00','2025-12-15 21:38:44'),(10,9,5,'1 Injection','Dr. Ahmed','2025-12-15','20:00:00','2025-12-15 21:38:44'),(11,8,5,'1 Injection','Dr. Ahmed','2025-12-15','20:00:00','2025-12-15 21:38:44'),(12,7,5,'1 Injection','Dr. Ahmed','2025-12-15','20:00:00','2025-12-15 21:38:44'),(15,1,4,'5mg IV','Head Nurse','2025-12-14','14:30:00','2025-12-15 21:38:44'),(16,2,4,'5mg IV','Head Nurse','2025-12-14','14:30:00','2025-12-15 21:38:44'),(17,7,4,'5mg IV','Head Nurse','2025-12-14','14:30:00','2025-12-15 21:38:44');
/*!40000 ALTER TABLE `medication_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-16  9:54:48
