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
-- Table structure for table `guardians`
--

DROP TABLE IF EXISTS `guardians`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardians` (
  `guardian_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `name` varchar(120) NOT NULL,
  `relation` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `emergency_contact` tinyint(1) NOT NULL,
  PRIMARY KEY (`guardian_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `guardians_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardians`
--

LOCK TABLES `guardians` WRITE;
/*!40000 ALTER TABLE `guardians` DISABLE KEYS */;
INSERT INTO `guardians` VALUES (1,1,'Zaheer Khan','Father','0300-1112222','Block J, Nazimabad',1),(2,2,'Kiran Ali','Mother','0321-3334444','Block B, North Nazimabad',1),(3,3,'Samina Mehmood','Wife','0333-5556666','Surjani Town Sector 7',1),(4,4,'Bilal Tariq','Brother','0345-7778888','Federal B Area',0),(5,5,'Naila Raza','Sister','0300-9990000','Gulshan-e-Iqbal',1),(6,6,'Imran Butt','Husband','0313-1113333','Defence Housing Authority',0),(7,7,'Javed Qadir','Uncle','0300-4446666','PECHS, Karachi',1),(8,8,'Asif Saleem','Husband','0322-7779999','Gulistan-e-Jauhar',1),(9,9,'Fauzia Butt','Daughter','0345-1234567','Malir Cantt',1),(10,10,'Zahid Malik','Father','0300-9876543','Bahadurabad',1),(11,15,'Ammar','Friend','03213302123','fasfasdfsfsa',1);
/*!40000 ALTER TABLE `guardians` ENABLE KEYS */;
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
