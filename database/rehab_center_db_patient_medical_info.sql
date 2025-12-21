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
-- Table structure for table `patient_medical_info`
--

DROP TABLE IF EXISTS `patient_medical_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_medical_info` (
  `medical_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `primary_addiction` varchar(80) NOT NULL,
  `duration_of_use_months` int NOT NULL,
  `addiction_level` varchar(50) NOT NULL,
  `diseases` text,
  `allergies` text,
  `last_donation_date` date DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`medical_id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  CONSTRAINT `patient_medical_info_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_medical_info`
--

LOCK TABLES `patient_medical_info` WRITE;
/*!40000 ALTER TABLE `patient_medical_info` DISABLE KEYS */;
INSERT INTO `patient_medical_info` VALUES (1,1,'Heroin',60,'High','Hepatitis C','Penicillin','2025-01-10','Requires close monitoring during detox.'),(2,2,'Prescription Opioids',36,'Moderate','None','Dust','2024-11-20','Family history of depression.'),(3,3,'Alcohol',120,'High','Liver Cirrhosis','None',NULL,'Long-term user. High risk.'),(4,4,'Cannabis',48,'Low','Asthma','Pollen','2025-05-01','Primary issue is chronic use and motivation.'),(5,5,'Cocaine',24,'Moderate','Hypertension','Latex','2025-03-05','Discharged on anti-anxiety meds.'),(6,6,'Methamphetamine',18,'Moderate','Dental Issues','None','2024-12-15','Successfully completed 90-day program.'),(7,7,'Heroin',84,'High','HIV','Sulfonamides',NULL,'Requires specialized care and medication.'),(8,8,'Benzodiazepines',10,'Low','Anxiety Disorder','None','2025-09-01','Abused anxiety medication.'),(9,9,'Alcohol',180,'High','Diabetes','Insulin',NULL,'Elderly patient with multiple complications.'),(10,10,'Cigarettes/Nicotine',3,'Low','None','Cats','2025-11-01','Youngest patient. Minor addiction.'),(15,15,'Alcohol',5,'Mild','xsdf','afas',NULL,'xsdf');
/*!40000 ALTER TABLE `patient_medical_info` ENABLE KEYS */;
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
