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
-- Table structure for table `medicines`
--

DROP TABLE IF EXISTS `medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicines` (
  `medicine_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dosage_form` varchar(50) DEFAULT NULL,
  `stock_quantity` int DEFAULT '0',
  `supplier_batch` varchar(100) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`medicine_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicines`
--

LOCK TABLES `medicines` WRITE;
/*!40000 ALTER TABLE `medicines` DISABLE KEYS */;
INSERT INTO `medicines` VALUES (1,'Panadol Extra','Tablet',500,'GSK-001','2025-12-01','2025-12-15 21:38:44'),(2,'Brufen 400mg','Tablet',300,'ABB-092','2024-10-15','2025-12-15 21:38:44'),(3,'Methadone','Syrup',100,'RHB-110','2024-08-20','2025-12-15 21:38:44'),(4,'Diazepam (Valium)','Injection',50,'PSY-554','2025-01-10','2025-12-15 21:38:44'),(5,'B-Complex','Injection',200,'VIT-990','2025-06-30','2025-12-15 21:38:44'),(6,'Omeprazole (Risek)','Capsule',400,'GET-112','2026-02-14','2025-12-15 21:38:44'),(7,'Augmentin 625mg','Tablet',150,'GSK-220','2024-11-05','2025-12-15 21:38:44'),(8,'Xanax 0.5mg','Tablet',250,'PFZ-303','2025-03-22','2025-12-15 21:38:44'),(9,'Insulin Regular','Injection',40,'LIL-887','2024-09-01','2025-12-15 21:38:44'),(10,'Cough Syrup','Syrup',80,'HER-101','2024-12-12','2025-12-15 21:38:44'),(11,'Disprin','Tablet',1000,'REC-005','2026-01-01','2025-12-15 21:38:44'),(12,'Flagyl 400mg','Tablet',200,'SAN-776','2025-07-20','2025-12-15 21:38:44'),(13,'Gravinate','Tablet',150,'SEA-443','2025-04-10','2025-12-15 21:38:44'),(14,'Kestine','Tablet',120,'ALL-221','2025-08-08','2025-12-15 21:38:44'),(15,'Calcium + D3','Tablet',600,'BON-555','2026-05-15','2025-12-15 21:38:44');
/*!40000 ALTER TABLE `medicines` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-16  9:54:50
