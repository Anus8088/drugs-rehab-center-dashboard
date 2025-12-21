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
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `branch_id` int NOT NULL,
  `patient_code` varchar(50) NOT NULL,
  `full_name` varchar(120) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(20) NOT NULL,
  `admission_date` date NOT NULL,
  `expected_discharge_date` date NOT NULL,
  `status` varchar(30) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `patient_code` (`patient_code`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,1,'P-NN-001','Ahmed Khan','1995-05-15','Male','2025-11-01','2026-02-01','Admitted','2025-12-15 17:03:50'),(2,1,'P-NN-002','Sara Ali','2000-02-28','Female','2025-11-10','2026-01-20','Admitted','2025-12-15 17:03:50'),(3,2,'P-ST-003','Fahad Mehmood','1988-10-03','Male','2025-10-25','2026-03-25','Admitted','2025-12-15 17:03:50'),(4,3,'P-KB-004','Aisha Tariq','1998-07-20','Female','2025-12-05','2026-04-05','Admitted','2025-12-15 17:03:50'),(5,4,'P-GI-005','Junaid Raza','1992-04-12','Male','2025-10-01','2025-12-15','Discharge-Planned','2025-12-15 17:03:50'),(6,4,'P-GI-006','Hina Imran','1996-09-01','Female','2025-09-15','2025-12-05','Completed','2025-12-15 17:03:50'),(7,1,'P-NN-007','Usman Javed','1985-11-20','Male','2025-12-10','2026-05-10','Admitted','2025-12-15 17:03:50'),(8,2,'P-ST-008','Nazia Saleem','1990-01-01','Female','2025-11-05','2026-03-05','Admitted','2025-12-15 17:03:50'),(9,3,'P-KB-009','Kamran Butt','1975-06-18','Male','2025-10-15','2026-01-15','Admitted','2025-12-15 17:03:50'),(10,4,'P-GI-010','Rabia Zahid','2003-12-12','Female','2025-12-01','2026-02-28','Admitted','2025-12-15 17:03:50'),(15,4,'P-GU-011','Ali','2025-12-18','Male','2025-12-14','2025-12-24','Admitted','2025-12-15 21:13:46');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
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
