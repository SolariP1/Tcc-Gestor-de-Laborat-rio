# SQL-Front 5.1  (Build 4.16)

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE */;
/*!40101 SET SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES */;
/*!40103 SET SQL_NOTES='ON' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;


# Host: localhost    Database: testepython
# ------------------------------------------------------
# Server version 5.5.5-10.4.32-MariaDB

DROP DATABASE IF EXISTS `testepython`;
CREATE DATABASE `testepython` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `testepython`;

CREATE TABLE IF NOT EXISTS materiais
                      (id INTEGER PRIMARY KEY,
                      nome TEXT,
                      descricao TEXT,
                      imagem TEXT,
                      quantidade INTEGER
											);

#
# Source for table reservas
#

DROP TABLE IF EXISTS `reservas`;
CREATE TABLE `reservas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `laboratorio` text DEFAULT NULL,
  `pessoa` text DEFAULT NULL,
  `primeiro_horario` text DEFAULT NULL,
  `ultimo_horario` text DEFAULT NULL,
  `data_reserva` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


#
# Source for table tbl_agendamento
#

DROP TABLE IF EXISTS `tbl_agendamento`;
CREATE TABLE `tbl_agendamento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `laboratorio` text DEFAULT NULL,
  `pessoa` text DEFAULT NULL,
  `primeiro_horario` text DEFAULT NULL,
  `ultimo_horario` text DEFAULT NULL,
  `data_reserva` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_agendamento
#

LOCK TABLES `tbl_agendamento` WRITE;
/*!40000 ALTER TABLE `tbl_agendamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_agendamento` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_cadastro
#

DROP TABLE IF EXISTS `tbl_cadastro`;
CREATE TABLE `tbl_cadastro` (
  `cad_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`cad_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_cadastro
#

LOCK TABLES `tbl_cadastro` WRITE;
/*!40000 ALTER TABLE `tbl_cadastro` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_cadastro` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_cargo
#

DROP TABLE IF EXISTS `tbl_cargo`;
CREATE TABLE `tbl_cargo` (
  `car_cod` int(11) NOT NULL AUTO_INCREMENT,
  `car_marcaProduto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`car_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_cargo
#

LOCK TABLES `tbl_cargo` WRITE;
/*!40000 ALTER TABLE `tbl_cargo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_cargo` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_categorias
#

DROP TABLE IF EXISTS `tbl_categorias`;
CREATE TABLE `tbl_categorias` (
  `cat_cod` int(11) NOT NULL AUTO_INCREMENT,
  `cat_categoria` varchar(255) DEFAULT NULL,
  `cat_descrição` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_categorias
#

LOCK TABLES `tbl_categorias` WRITE;
/*!40000 ALTER TABLE `tbl_categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_categorias` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_chefe
#

DROP TABLE IF EXISTS `tbl_chefe`;
CREATE TABLE `tbl_chefe` (
  `che_cod` int(11) NOT NULL AUTO_INCREMENT,
  `che_matrículas` varchar(255) DEFAULT NULL,
  `che_nome` varchar(255) DEFAULT NULL,
  `che_cpf` varchar(255) DEFAULT NULL,
  `che_perfil` varchar(255) DEFAULT NULL,
  `che_telefone` varchar(255) DEFAULT NULL,
  `che_celular` varchar(255) DEFAULT NULL,
  `che_email` varchar(255) DEFAULT NULL,
  `che_im` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`che_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_chefe
#

LOCK TABLES `tbl_chefe` WRITE;
/*!40000 ALTER TABLE `tbl_chefe` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_chefe` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_cidades
#

DROP TABLE IF EXISTS `tbl_cidades`;
CREATE TABLE `tbl_cidades` (
  `cid_cod` int(11) NOT NULL AUTO_INCREMENT,
  `cid_nome` varchar(255) DEFAULT NULL,
  `est_idEstado` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cid_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_cidades
#

LOCK TABLES `tbl_cidades` WRITE;
/*!40000 ALTER TABLE `tbl_cidades` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_cidades` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_departamento
#

DROP TABLE IF EXISTS `tbl_departamento`;
CREATE TABLE `tbl_departamento` (
  `dep_cod` int(11) NOT NULL AUTO_INCREMENT,
  `dep_ID` varchar(255) DEFAULT NULL,
  `dep_detalhes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`dep_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_departamento
#

LOCK TABLES `tbl_departamento` WRITE;
/*!40000 ALTER TABLE `tbl_departamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_departamento` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_detalheemp
#

DROP TABLE IF EXISTS `tbl_detalheemp`;
CREATE TABLE `tbl_detalheemp` (
  `det_cod` int(11) NOT NULL AUTO_INCREMENT,
  `det_IDEmpresa` varchar(255) DEFAULT NULL,
  `det_IDNpatri` varchar(255) DEFAULT NULL,
  `det_obs` varchar(255) DEFAULT NULL,
  `det_situação` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`det_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_detalheemp
#

LOCK TABLES `tbl_detalheemp` WRITE;
/*!40000 ALTER TABLE `tbl_detalheemp` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_detalheemp` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_empréstimo
#

DROP TABLE IF EXISTS `tbl_empréstimo`;
CREATE TABLE `tbl_empréstimo` (
  `emp_cod` int(11) NOT NULL AUTO_INCREMENT,
  `emp_IDEmpresa` varchar(255) DEFAULT NULL,
  `emp_IDLocatario` varchar(255) DEFAULT NULL,
  `emp_autorização` varchar(255) DEFAULT NULL,
  `emp_levarPara` varchar(255) DEFAULT NULL,
  `emp_obs` varchar(255) DEFAULT NULL,
  `emp_dataRetiro` varchar(255) DEFAULT NULL,
  `emp_previsãoDevolução` varchar(255) DEFAULT NULL,
  `emp_dataDevolução` varchar(255) DEFAULT NULL,
  `emp_uso` varchar(255) DEFAULT NULL,
  `emp_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`emp_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_empréstimo
#

LOCK TABLES `tbl_empréstimo` WRITE;
/*!40000 ALTER TABLE `tbl_empréstimo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_empréstimo` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_equipamento
#

DROP TABLE IF EXISTS `tbl_equipamento`;
CREATE TABLE `tbl_equipamento` (
  `equ_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`equ_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_equipamento
#

LOCK TABLES `tbl_equipamento` WRITE;
/*!40000 ALTER TABLE `tbl_equipamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_equipamento` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_equipe
#

DROP TABLE IF EXISTS `tbl_equipe`;
CREATE TABLE `tbl_equipe` (
  `equ_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`equ_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_equipe
#

LOCK TABLES `tbl_equipe` WRITE;
/*!40000 ALTER TABLE `tbl_equipe` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_equipe` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_estado
#

DROP TABLE IF EXISTS `tbl_estado`;
CREATE TABLE `tbl_estado` (
  `est_cod` int(11) NOT NULL AUTO_INCREMENT,
  `est_idEstado` varchar(2) DEFAULT NULL,
  `est_nome` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`est_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_estado
#

LOCK TABLES `tbl_estado` WRITE;
/*!40000 ALTER TABLE `tbl_estado` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_estado` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_estoque
#

DROP TABLE IF EXISTS `tbl_estoque`;
CREATE TABLE `tbl_estoque` (
  `est_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`est_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_estoque
#

LOCK TABLES `tbl_estoque` WRITE;
/*!40000 ALTER TABLE `tbl_estoque` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_estoque` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_estoqueentrada
#

DROP TABLE IF EXISTS `tbl_estoqueentrada`;
CREATE TABLE `tbl_estoqueentrada` (
  `estE_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`estE_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_estoqueentrada
#

LOCK TABLES `tbl_estoqueentrada` WRITE;
/*!40000 ALTER TABLE `tbl_estoqueentrada` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_estoqueentrada` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_estoquesaida
#

DROP TABLE IF EXISTS `tbl_estoquesaida`;
CREATE TABLE `tbl_estoquesaida` (
  `estS_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`estS_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_estoquesaida
#

LOCK TABLES `tbl_estoquesaida` WRITE;
/*!40000 ALTER TABLE `tbl_estoquesaida` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_estoquesaida` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_fichaentrada
#

DROP TABLE IF EXISTS `tbl_fichaentrada`;
CREATE TABLE `tbl_fichaentrada` (
  `ficha_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ficha_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_fichaentrada
#

LOCK TABLES `tbl_fichaentrada` WRITE;
/*!40000 ALTER TABLE `tbl_fichaentrada` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_fichaentrada` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_funcionário
#

DROP TABLE IF EXISTS `tbl_funcionário`;
CREATE TABLE `tbl_funcionário` (
  `fun_cod` int(11) NOT NULL AUTO_INCREMENT,
  `fun_matrículas` varchar(255) DEFAULT NULL,
  `fun_nome` varchar(255) DEFAULT NULL,
  `fun_cpf` varchar(255) DEFAULT NULL,
  `fun_perfil` varchar(255) DEFAULT NULL,
  `fun_telefone` varchar(255) DEFAULT NULL,
  `fun_celular` varchar(255) DEFAULT NULL,
  `fun_email` varchar(255) DEFAULT NULL,
  `fun_im` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`fun_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_funcionário
#

LOCK TABLES `tbl_funcionário` WRITE;
/*!40000 ALTER TABLE `tbl_funcionário` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_funcionário` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_login
#

DROP TABLE IF EXISTS `tbl_login`;
CREATE TABLE `tbl_login` (
  `login_cod` int(11) NOT NULL AUTO_INCREMENT,
  `login_nome` varchar(255) DEFAULT NULL,
  `login_senha` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`login_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_login
#

LOCK TABLES `tbl_login` WRITE;
/*!40000 ALTER TABLE `tbl_login` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_login` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_notificações
#

DROP TABLE IF EXISTS `tbl_notificações`;
CREATE TABLE `tbl_notificações` (
  `not_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`not_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_notificações
#

LOCK TABLES `tbl_notificações` WRITE;
/*!40000 ALTER TABLE `tbl_notificações` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_notificações` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_patrimônio
#

DROP TABLE IF EXISTS `tbl_patrimônio`;
CREATE TABLE `tbl_patrimônio` (
  `pat_cod` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`pat_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_patrimônio
#

LOCK TABLES `tbl_patrimônio` WRITE;
/*!40000 ALTER TABLE `tbl_patrimônio` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_patrimônio` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table tbl_produto
#

DROP TABLE IF EXISTS `tbl_produto`;
CREATE TABLE `tbl_produto` (
  `pro_cod` int(11) NOT NULL AUTO_INCREMENT,
  `pro_marcaProduto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pro_cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

#
# Dumping data for table tbl_produto
#

LOCK TABLES `tbl_produto` WRITE;
/*!40000 ALTER TABLE `tbl_produto` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_produto` ENABLE KEYS */;
UNLOCK TABLES;

#
# Source for table usuario
#

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `usu_id` int(11) NOT NULL AUTO_INCREMENT,
  `usu_nome` varchar(255) NOT NULL,
  `usu_usuario` varchar(50) NOT NULL,
  `usu_email` varchar(255) NOT NULL,
  `usu_cpf` varchar(14) NOT NULL,
  `usu_cidade` varchar(255) NOT NULL,
  `usu_senha` varchar(255) NOT NULL,
  PRIMARY KEY (`usu_id`),
  UNIQUE KEY `usu_usuario` (`usu_usuario`),
  UNIQUE KEY `usu_email` (`usu_email`),
  UNIQUE KEY `usu_cpf` (`usu_cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
