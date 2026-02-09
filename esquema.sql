CREATE DATABASE  IF NOT EXISTS `temperaturas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `temperaturas`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: temperaturas
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `fronteras`
--

DROP TABLE IF EXISTS `fronteras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fronteras` (
  `idfronteras` int NOT NULL AUTO_INCREMENT,
  `idpais` int NOT NULL,
  `cca3_frontera` varchar(3) NOT NULL,
  PRIMARY KEY (`idfronteras`),
  KEY `fk_frontera_pais_idx` (`idpais`),
  CONSTRAINT `fk_frontera_pais` FOREIGN KEY (`idpais`) REFERENCES `paises` (`idpais`)
) ENGINE=InnoDB AUTO_INCREMENT=367 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paises`
--

DROP TABLE IF EXISTS `paises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paises` (
  `idpais` int NOT NULL AUTO_INCREMENT,
  `cca2` varchar(2) NOT NULL,
  `cca3` varchar(3) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `capital` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `subregion` varchar(255) NOT NULL,
  `miembroUE` bit(1) NOT NULL,
  `latitud` float DEFAULT NULL,
  `longitud` float DEFAULT NULL,
  PRIMARY KEY (`idpais`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temperaturas`
--

DROP TABLE IF EXISTS `temperaturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperaturas` (
  `idtemperaturas` int NOT NULL AUTO_INCREMENT,
  `idpais` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `temperatura` float NOT NULL,
  `sensacion` float NOT NULL,
  `minima` float NOT NULL,
  `maxima` float NOT NULL,
  `humedad` float NOT NULL,
  `amanecer` time NOT NULL,
  `atardecer` time NOT NULL,
  PRIMARY KEY (`idtemperaturas`),
  KEY `fk_pais_temperatura_idx` (`idpais`),
  CONSTRAINT `fk_pais_temperatura` FOREIGN KEY (`idpais`) REFERENCES `paises` (`idpais`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-13 12:26:03
