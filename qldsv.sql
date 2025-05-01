-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: quan_ly_sinh_vien
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `cau_hinh_diem`
--

DROP TABLE IF EXISTS `cau_hinh_diem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cau_hinh_diem` (
  `id` int NOT NULL,
  `ma_lop` varchar(10) NOT NULL,
  `ten_cot_diem` varchar(50) NOT NULL,
  `trong_so` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cau_hinh_diem_ibfk_1` (`ma_lop`),
  CONSTRAINT `cau_hinh_diem_ibfk_1` FOREIGN KEY (`ma_lop`) REFERENCES `lop` (`ma_lop`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cau_hinh_diem`
--

LOCK TABLES `cau_hinh_diem` WRITE;
/*!40000 ALTER TABLE `cau_hinh_diem` DISABLE KEYS */;
/*!40000 ALTER TABLE `cau_hinh_diem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chi_tiet_diem`
--

DROP TABLE IF EXISTS `chi_tiet_diem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_diem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mssv` bigint DEFAULT NULL,
  `id_cot_diem` int NOT NULL,
  `diem` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chi_tiet_diem_ibfk_1` (`mssv`),
  CONSTRAINT `chi_tiet_diem_ibfk_1` FOREIGN KEY (`mssv`) REFERENCES `sinh_vien` (`mssv`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_diem`
--

LOCK TABLES `chi_tiet_diem` WRITE;
/*!40000 ALTER TABLE `chi_tiet_diem` DISABLE KEYS */;
/*!40000 ALTER TABLE `chi_tiet_diem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dang_ky`
--

DROP TABLE IF EXISTS `dang_ky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dang_ky` (
  `mssv` bigint NOT NULL,
  `ma_lop` varchar(50) NOT NULL,
  PRIMARY KEY (`mssv`,`ma_lop`),
  KEY `ma_lop` (`ma_lop`),
  CONSTRAINT `dang_ky_ibfk_1` FOREIGN KEY (`mssv`) REFERENCES `sinh_vien` (`mssv`),
  CONSTRAINT `dang_ky_ibfk_2` FOREIGN KEY (`ma_lop`) REFERENCES `lop` (`ma_lop`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dang_ky`
--

LOCK TABLES `dang_ky` WRITE;
/*!40000 ALTER TABLE `dang_ky` DISABLE KEYS */;
INSERT INTO `dang_ky` VALUES (3122941875,'123'),(3124129568,'123'),(3122941875,'321'),(3123904821,'321'),(3122493264,'LCT10101'),(3125230147,'LCT10101'),(3126054893,'LCT10101'),(3126710095,'LCT10101'),(3126052349,'LCT10102'),(3126710095,'LCT10102'),(3127812709,'LCT10102'),(3125230147,'LCT10201'),(3126052349,'LCT10201'),(3126054893,'LCT10201'),(3125839714,'LDL10102');
/*!40000 ALTER TABLE `dang_ky` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diem`
--

DROP TABLE IF EXISTS `diem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diem` (
  `mssv` bigint NOT NULL,
  `ma_mon` varchar(50) NOT NULL,
  `diem_kiem_tra` float DEFAULT '0',
  `diem_cuoi_ky` float DEFAULT '0',
  `diem_tong_ket` float DEFAULT '0',
  `xep_loai` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`mssv`,`ma_mon`),
  KEY `ma_mon` (`ma_mon`),
  CONSTRAINT `diem_ibfk_1` FOREIGN KEY (`mssv`) REFERENCES `sinh_vien` (`mssv`),
  CONSTRAINT `diem_ibfk_2` FOREIGN KEY (`ma_mon`) REFERENCES `mon_hoc` (`ma_mon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diem`
--

LOCK TABLES `diem` WRITE;
/*!40000 ALTER TABLE `diem` DISABLE KEYS */;
/*!40000 ALTER TABLE `diem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giang_vien`
--

DROP TABLE IF EXISTS `giang_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giang_vien` (
  `ma_gv` varchar(50) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `khoa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `sdt` varchar(50) NOT NULL,
  `ma_nguoi_dung` varchar(50) DEFAULT NULL,
  `trang_thai` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ma_gv`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `so_dien_thoai` (`sdt`),
  UNIQUE KEY `sdt` (`sdt`),
  UNIQUE KEY `ma_nguoi_dung` (`ma_nguoi_dung`),
  KEY `fk_khoa_gv` (`khoa`),
  CONSTRAINT `fk_khoa_gv` FOREIGN KEY (`khoa`) REFERENCES `khoa` (`ma_khoa`) ON DELETE SET NULL,
  CONSTRAINT `giang_vien_ibfk_1` FOREIGN KEY (`ma_nguoi_dung`) REFERENCES `tai_khoan` (`ma_nguoi_dung`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giang_vien`
--

LOCK TABLES `giang_vien` WRITE;
/*!40000 ALTER TABLE `giang_vien` DISABLE KEYS */;
INSERT INTO `giang_vien` VALUES ('201201','Nguyễn Văn An','DCT','nguyenvanan1@gmail.com','0912345670','501',0),('201202','Trần Thị Bích','DDL','tranbich02@gmail.com','0912345671','502',1),('201203','Lê Minh Tuấn','DCT','leminhtuan3@gmail.com','0912345672','503',1),('201204','Phạm Ngọc Hà','DKD','phamngoch4@gmail.com','0912345673','504',1),('201205','Đỗ Quang Vinh','DGM','doquangvinh5@gmail.com','0912345674','505',1),('201206','Hoàng Thị Yến','DKT','hoangthiyen6@gmail.com','0912345675','506',1),('201207','Vũ Hải Long','DAN','vuhailong7@gmail.com','0912345676','507',1),('201208','Ngô Thanh Tùng','DQT','ngothanhtung8@gmail.com','0912345677','508',1),('201209','Đặng Thị Lan','DTN','dangthilan9@gmail.com','0912345678','509',1),('201210','Bùi Đức Anh','DLU','buianhduc10@gmail.com','0912345679','510',1),('201211','Nguyễn Thị Mai','DKE','nguyenthimai11@gmail.com','0912345680','511',1),('201212','Trần Văn Nam','DKQ','tranvannam12@gmail.com','0912345681','512',1),('201213','Lê Thị Thu','DGT','lethithu13@gmail.com','0912345682','513',1),('201214','Phạm Minh Phương','DKD','phamminhphuong14@gmail.com','0912345683','514',1),('201215','Đỗ Thị Hồng','DAN','dothihong15@gmail.com','0912345684','515',1),('201216','Hoàng Minh Trí','DDL','hoangminhtri16@gmail.com','0912345685','516',1),('201217','Vũ Thị Duyên','DCT','vuthiduyen17@gmail.com','0912345686','517',1),('201218','Ngô Minh Nhật','DTN','ngominhnhat18@gmail.com','0912345687','518',1),('201219','Đặng Quốc Toàn','DGM','dangquoctoan19@gmail.com','0912345688','519',1),('201220','Bùi Thị Ngọc','DKQ','buithingoc20@gmail.com','0912345689','520',1);
/*!40000 ALTER TABLE `giang_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khoa`
--

DROP TABLE IF EXISTS `khoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khoa` (
  `ma_khoa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ten_khoa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `trang_thai` int NOT NULL DEFAULT '1',
  `sdt_khoa` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email_khoa` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ma_khoa`),
  UNIQUE KEY `ten_khoa` (`ten_khoa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khoa`
--

LOCK TABLES `khoa` WRITE;
/*!40000 ALTER TABLE `khoa` DISABLE KEYS */;
INSERT INTO `khoa` VALUES ('DAN','Ngôn ngữ Anh',1,'0901901234','ngon_ngu_anh@gmail.com'),('DCT','Công nghệ thông tin',1,'0904234567','cntt@gmail.com'),('DDL','Du lịch',1,'0905345678','dulich@gmail.com'),('DGM','Giáo dục mầm non',1,'0906456789','gdmn@gmail.com'),('DGT','Giáo dục tiểu học',1,'0907567890','gdth@gmail.com'),('DKD','Điện tử',1,'0903123456','dien_tu@gmail.com'),('DKE','Kế toán',1,'0908678901','ke_toan@gmail.com'),('DKQ','Kinh doanh quốc tế',1,'0909789012','kinhdoanhquocte@gmail.com'),('DKT','Kinh tế',1,'0904234567','kinhte@gmail.com'),('DLU','Luật',1,'0900890123','luat@gmail.com'),('DQT','Quốc tế học',1,'0902012345','quocte@gmail.com'),('DTN','Tài chính ngân hàng',1,'0903123456','taichinhnganhang@gmail.com');
/*!40000 ALTER TABLE `khoa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lop`
--

DROP TABLE IF EXISTS `lop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lop` (
  `ma_lop` varchar(50) NOT NULL,
  `ma_mon` varchar(50) NOT NULL,
  `so_luong` int DEFAULT NULL,
  `hoc_ky` int DEFAULT NULL,
  `nam` int DEFAULT NULL,
  `ma_gv` varchar(50) DEFAULT NULL,
  `trang_thai` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ma_lop`),
  KEY `ma_mon` (`ma_mon`),
  KEY `ma_gv` (`ma_gv`),
  CONSTRAINT `lop_ibfk_1` FOREIGN KEY (`ma_mon`) REFERENCES `mon_hoc` (`ma_mon`),
  CONSTRAINT `lop_ibfk_2` FOREIGN KEY (`ma_gv`) REFERENCES `giang_vien` (`ma_gv`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lop`
--

LOCK TABLES `lop` WRITE;
/*!40000 ALTER TABLE `lop` DISABLE KEYS */;
INSERT INTO `lop` VALUES ('123','CT101',2,1,2022,'201201',1),('321','DL101',3,3,5623,'201202',1),('LCT10101','CT101',50,1,2024,'201201',1),('LCT10102','CT101',80,2,2024,NULL,1),('LCT10201','CT102',50,1,2025,'201217',1),('LCT10202','CT102',102,2,2024,'201201',1),('LCT10301','CT103',85,2,2025,'201203',1),('LCT10302','CT103',120,3,2024,'201203',1),('LCT10401','CT104',50,1,2024,'201217',1),('LCT10402','CT104',80,2,2025,'201217',1),('LDL10101','DL101',65,3,2024,'201202',1),('LDL10102','DL101',100,1,2025,'201216',1),('LDT10101','DT101',95,1,2025,'201204',1),('LDT10102','DT101',120,2,2025,'201214',1),('LDT10201','DT102',100,2,2024,'201214',1),('LEN10201','EN102',50,1,2025,'201207',1),('LEN10202','EN102',100,3,2024,'201215',1),('LKT10101','KT101',80,3,2024,'201211',1),('LKT10102','KT101',120,1,2025,'201211',1),('LLU10201','LU102',80,3,2024,'201210',1),('LLU10202','LU102',85,2,2025,'201210',1),('LMN10101','MN101',80,2,2024,'201205',1),('LMN10102','MN101',110,3,2025,'201219',1),('LQT10201','QT102',90,2,2024,'201208',1),('LTH10101','TH101',50,1,2025,'201213',1),('LTH10102','TH101',100,2,2025,'201213',1),('LTH10201','TH102',50,3,2024,'201213',1),('LTN10201','TN102',70,3,2024,'201209',1),('LTN10202','TN102',50,2,2025,'201218',1);
/*!40000 ALTER TABLE `lop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mon_hoc`
--

DROP TABLE IF EXISTS `mon_hoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mon_hoc` (
  `ma_mon` varchar(50) NOT NULL,
  `ten_mon` varchar(100) NOT NULL,
  `so_tin_chi` int NOT NULL,
  `khoa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `trang_thai` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ma_mon`),
  KEY `mh_khoa_khoa` (`khoa`),
  CONSTRAINT `mh_khoa_khoa` FOREIGN KEY (`khoa`) REFERENCES `khoa` (`ten_khoa`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mon_hoc`
--

LOCK TABLES `mon_hoc` WRITE;
/*!40000 ALTER TABLE `mon_hoc` DISABLE KEYS */;
INSERT INTO `mon_hoc` VALUES ('CT100','Lập trình Python',3,'Công nghệ thông tin',1),('CT101','Lập trình Python',3,'Công nghệ thông tin',0),('CT102','Cấu trúc dữ liệu & Giải thuật',4,'Công nghệ thông tin',1),('CT103','Hệ quản trị cơ sở dữ liệu',3,'Công nghệ thông tin',1),('CT104','Trí tuệ nhân tạo',3,'Công nghệ thông tin',1),('CT105','Mạng máy tính',3,'Công nghệ thông tin',1),('CT106','Lập trình hướng đối tượng',3,'Công nghệ thông tin',1),('CT107','Bảo mật hệ thống',3,'Công nghệ thông tin',1),('DL101','Nguyên lý du lịch',3,'Du lịch',1),('DL102','Quản trị dịch vụ du lịch',4,'Du lịch',1),('DL103','Quản lý du lịch bền vững',3,'Du lịch',1),('DL104','Marketing du lịch hiện đại',3,'Du lịch',1),('DT101','Mạch điện tử cơ bản',3,'Điện tử',1),('DT102','Xử lý tín hiệu số',4,'Điện tử',1),('DT103','Thiết kế hệ thống nhúng',3,'Điện tử',1),('DT104','Tự động hóa công nghiệp',4,'Điện tử',1),('EN101','Tiếng Anh giao tiếp',2,'Ngôn ngữ Anh',1),('EN102','Dịch thuật Anh–Việt',3,'Ngôn ngữ Anh',1),('EN103','Tiếng Anh học thuật',3,'Ngôn ngữ Anh',1),('EN104','Ngữ pháp nâng cao',2,'Ngôn ngữ Anh',1),('KN101','Vi mô kinh tế học',3,'Kinh tế',1),('KN102','Thống kê kinh tế',3,'Kinh tế',1),('KN103','Kinh tế vĩ mô nâng cao',3,'Kinh tế',1),('KN104','Kinh tế lượng',4,'Kinh tế',1),('KQ101','Thương mại quốc tế',3,'Kinh doanh quốc tế',1),('KQ102','Logistics và chuỗi cung ứng',4,'Kinh doanh quốc tế',1),('KQ103','Đàm phán quốc tế',2,'Kinh doanh quốc tế',1),('KQ104','Chiến lược kinh doanh toàn cầu',4,'Kinh doanh quốc tế',1),('KT101','Nguyên lý kế toán',3,'Kế toán',1),('KT102','Kế toán tài chính doanh nghiệp',4,'Kế toán',1),('KT103','Kiểm toán cơ bản',3,'Kế toán',1),('KT104','Thuế và luật thuế',3,'Kế toán',1),('LU101','Luật Hiến pháp',3,'Luật',1),('LU102','Luật Dân sự cơ bản',4,'Luật',1),('LU103','Luật lao động',3,'Luật',1),('LU104','Luật thương mại quốc tế',4,'Luật',1),('MN101','Phát triển ngôn ngữ trẻ em',3,'Giáo dục mầm non',1),('MN102','Phương pháp giảng dạy mầm non',4,'Giáo dục mầm non',1),('MN103','Tâm lý phát triển trẻ',2,'Giáo dục mầm non',1),('MN104','Sáng tạo và nghệ thuật cho trẻ',3,'Giáo dục mầm non',1),('QT101','Quan hệ quốc tế cơ bản',3,'Quốc tế học',1),('QT102','Kinh tế chính trị quốc tế',4,'Quốc tế học',1),('QT103','Văn hóa và xã hội toàn cầu',2,'Quốc tế học',1),('QT104','Kinh tế phát triển quốc tế',3,'Quốc tế học',1),('TH101','Phương pháp dạy toán tiểu học',3,'Giáo dục tiểu học',1),('TH102','Giáo dục giá trị sống',2,'Giáo dục tiểu học',1),('TH103','Giáo dục âm nhạc tiểu học',2,'Giáo dục tiểu học',1),('TH104','Thực hành sư phạm tiểu học',3,'Giáo dục tiểu học',1),('TN101','Ngân hàng thương mại',3,'Tài chính ngân hàng',1),('TN102','Thị trường chứng khoán',4,'Tài chính ngân hàng',1),('TN103','Ngân hàng đầu tư',3,'Tài chính ngân hàng',1),('TN104','Quản lý rủi ro tài chính',4,'Tài chính ngân hàng',1);
/*!40000 ALTER TABLE `mon_hoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhat_ky`
--

DROP TABLE IF EXISTS `nhat_ky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhat_ky` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ma_nguoi_dung` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `hanh_dong` text COLLATE utf8mb4_general_ci,
  `thoi_gian` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ma_nguoi_dung` (`ma_nguoi_dung`),
  CONSTRAINT `nhat_ky_ibfk_1` FOREIGN KEY (`ma_nguoi_dung`) REFERENCES `tai_khoan` (`ma_nguoi_dung`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhat_ky`
--

LOCK TABLES `nhat_ky` WRITE;
/*!40000 ALTER TABLE `nhat_ky` DISABLE KEYS */;
INSERT INTO `nhat_ky` VALUES (1,'admin','Sửa người dùng: pp','2025-04-15 01:49:28'),(2,'admin','Thêm người dùng: nnnn','2025-04-15 01:50:55'),(3,'admin','Xóa người dùng ID: nnnn','2025-04-15 01:51:05'),(4,'admin','Thêm người dùng: 2433111','2025-04-15 23:59:28'),(5,'admin','Thêm người dùng: dfszfg','2025-04-16 00:18:32'),(6,'admin','Sửa người dùng: kyerye','2025-04-18 00:01:56'),(7,'admin','Sửa người dùng: hhhhff','2025-04-18 00:03:50'),(8,'admin','Sửa người dùng: 55555555','2025-04-18 00:13:57'),(9,'admin','Sửa người dùng: 2433111ttt','2025-04-18 00:14:12'),(10,'admin','Sửa người dùng: gggg','2025-04-18 00:23:34'),(11,'admin','Sửa người dùng: ppaaaa','2025-04-18 00:24:30'),(12,'admin','Sửa người dùng: ppaa','2025-04-18 00:24:40'),(13,'admin','Sửa người dùng: aagggg','2025-04-18 00:34:10'),(14,'admin','Sửa người dùng: aagggg','2025-04-18 00:36:05');
/*!40000 ALTER TABLE `nhat_ky` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phan_quyen`
--

DROP TABLE IF EXISTS `phan_quyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phan_quyen` (
  `id` int NOT NULL,
  `vai_tro_id` int DEFAULT NULL,
  `quyen_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vai_tro_id` (`vai_tro_id`),
  KEY `quyen_id` (`quyen_id`),
  CONSTRAINT `phan_quyen_ibfk_1` FOREIGN KEY (`vai_tro_id`) REFERENCES `vai_tro` (`id`) ON DELETE CASCADE,
  CONSTRAINT `phan_quyen_ibfk_2` FOREIGN KEY (`quyen_id`) REFERENCES `quyen` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phan_quyen`
--

LOCK TABLES `phan_quyen` WRITE;
/*!40000 ALTER TABLE `phan_quyen` DISABLE KEYS */;
INSERT INTO `phan_quyen` VALUES (1,100,0),(2,200,1),(3,201,1);
/*!40000 ALTER TABLE `phan_quyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quyen`
--

DROP TABLE IF EXISTS `quyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quyen` (
  `id` int NOT NULL,
  `ten_quyen` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ten_quyen` (`ten_quyen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quyen`
--

LOCK TABLES `quyen` WRITE;
/*!40000 ALTER TABLE `quyen` DISABLE KEYS */;
INSERT INTO `quyen` VALUES (0,'admin'),(1,'user');
/*!40000 ALTER TABLE `quyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sinh_vien`
--

DROP TABLE IF EXISTS `sinh_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sinh_vien` (
  `mssv` bigint NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `he_dao_tao` varchar(255) DEFAULT NULL,
  `khoa` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ngay_sinh` date DEFAULT NULL,
  `gioi_tinh` enum('Nam','Nữ') DEFAULT NULL,
  `que` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `trang_thai` int DEFAULT '1',
  PRIMARY KEY (`mssv`),
  UNIQUE KEY `email` (`email`),
  KEY `sv_tenkhoa_khoa` (`khoa`),
  CONSTRAINT `sv_tenkhoa_khoa` FOREIGN KEY (`khoa`) REFERENCES `khoa` (`ten_khoa`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sinh_vien`
--

LOCK TABLES `sinh_vien` WRITE;
/*!40000 ALTER TABLE `sinh_vien` DISABLE KEYS */;
INSERT INTO `sinh_vien` VALUES (3122493264,'Nguyễn Văn An','Đại trà','Công nghệ thông tin','2000-09-05','Nam','TPHCM','nguyenvanan@gmail.com',1),(3122941875,'Trần Văn Bình','CLC','Du lịch','2000-08-13','Nam','Hà Nội','tranbinh@example.com',1),(3123456890,'Lê Thị Chi','CLC','Giáo dục mầm non','2002-01-16','Nữ','Đồng Tháp','lethic@gmail.com',1),(3123789245,'Trương Văn Dũng','Đại trà','Ngôn ngữ Anh','2004-04-26','Nam','Đà Nẵng','truongvand@gmail.com',1),(3123904821,'Dư Lan Em','Đại trà','Kinh tế','2001-06-19','Nữ','Hà Tỉnh','dulane2001@gmai.com',1),(3124129568,'Văn Lại Đức','Đại trà','Luật','2005-11-30','Nam','Vũng Tàu','homie@gmail.com',1),(3124348796,'Trần Thanh Giang','Đại trà','Giáo dục tiểu học','2004-02-22','Nữ','Huế','thanhgiang@gmail.com',1),(3124875923,'Mai Như Hiền','Đại trà','Ngôn ngữ Anh','2000-05-12','Nữ','TPHCM','abchien@gmail.com',1),(3125098263,'Bùi Hoàng Khang','Đại trà','Quốc tế học','1999-12-31','Nam','Đồng Tháp','lanngoc@gmail.com',1),(3125230147,'Nguyễn Anh Tài','Đại trà','Công nghệ thông tin','2003-06-29','Nam','Cần Thơ','anhtai296@gmail.com',1),(3125361729,'Châu Liễu Lan','CLC','Tài chính ngân hàng','2003-02-12','Nữ','Lâm Đồng','chaulan@gmail.com',1),(3125498671,'Nguyễn Sinh Đại','Đại trà','Du lịch','1999-04-15','Nam','Bình Dương','sinhdai@gmail.com',1),(3125601490,'Lại Như Mai','CLC','Luật','2003-06-13','Nữ','Vũng Tàu','mainhu1306@gmail.com',1),(3125610235,'Nguyễn Quang Huy','Đại trà','Điện tử','2002-03-01','Nam','Hà Nội','quanghuy@gmail.com',1),(3125723401,'Lê Minh Khánh','CLC','Kinh tế','2002-07-19','Nam','Hà Nội','leminhkhanh@example.com',1),(3125724567,'Trần Bảo Linh','Đại trà','Giáo dục mầm non','2001-11-14','Nữ','Đồng Nai','baolinh@gmail.com',1),(3125837890,'Lê Minh Tuấn','CLC','Kinh tế','2000-05-23','Nam','TPHCM','minhtuan@gmail.com',1),(3125839714,'Nguyễn Thị Bích','Đại trà','Du lịch','2001-05-03','Nữ','Bình Dương','nguyenbich@example.com',1),(3125942678,'Phan Tuấn Anh','CLC','Công nghệ thông tin','2000-11-15','Nam','TPHCM','phantuananh@example.com',1),(3125948701,'Võ Thị Lan','Đại trà','Giáo dục tiểu học','2003-08-05','Nữ','Hà Tĩnh','lanvothi@gmail.com',1),(3126052349,'Nguyễn Thiện Đức','Đại trà','Công nghệ thông tin','2002-12-12','Nam','Bình Dương','thienthu@gmail.com',1),(3126054893,'Trần Ngọc Mai','CLC','Công nghệ thông tin','2001-10-09','Nữ','Cần Thơ','tranngocmai@example.com',1),(3126165402,'Phạm Hương Giang','CLC','Luật','2001-04-22','Nữ','Huế','huonggiang@gmail.com',1),(3126165932,'Vũ Minh Tú','Đại trà','Kinh doanh quốc tế','2003-01-24','Nữ','Quảng Nam','vuminhtu@example.com',1),(3126278015,'Hoàng Thanh Bình','Đại trà','Quốc tế học','2002-06-07','Nam','Cần Thơ','hoangbinh@gmail.com',1),(3126278045,'Nguyễn Hồng Sơn','Đại trà','Giáo dục mầm non','1999-03-08','Nam','Đà Nẵng','nguyenhongson@example.com',1),(3126389123,'Lê Kim Oanh','CLC','Ngôn ngữ Anh','2003-01-10','Nữ','Đà Nẵng','kim.oanh@gmail.com',1),(3126389264,'Lê Hồng Sơn','CLC','Quốc tế học','2002-05-21','Nam','Hà Tĩnh','lehongson@example.com',1),(3126493287,'Trương Thị Tuyết','Đại trà','Giáo dục mầm non','2001-02-28','Nữ','Quảng Ninh','tuyettrung@gmail.com',1),(3126497481,'Trương Thanh Mai','CLC','Ngôn ngữ Anh','2004-12-15','Nữ','Vũng Tàu','truongthanhmai@example.com',1),(3126601158,'Nguyễn Trung Dũng','CLC','Kinh tế','2000-03-25','Nam','Lâm Đồng','trungdung@gmail.com',1),(3126601598,'Phạm Gia Bảo','Đại trà','Tài chính ngân hàng','2001-09-30','Nam','Lâm Đồng','phamgiabao@example.com',1),(3126710095,'Bùi Minh Hảo','Đại trà','Công nghệ thông tin','2002-07-18','Nữ','TPHCM','minhhao@gmail.com',1),(3126714702,'Đoàn Thị Lan','Đại trà','Kế toán','2000-01-11','Nữ','TPHCM','doanthilan@example.com',1),(3126823806,'Trần Văn Tiến','CLC','Luật','2003-04-02','Nam','Đắk Lắk','tranvantiendlu@example.com',1),(3126824569,'Lê Mai Chi','CLC','Giáo dục mầm non','2003-10-01','Nữ','Bắc Ninh','maichi@gmail.com',1),(3126934120,'Võ Tiến Dũng','Đại trà','Công nghệ thông tin','2000-09-15','Nam','Hà Nội','tiendung@gmail.com',1),(3126938527,'Nguyễn Thị Bích Duyên','CLC','Giáo dục mầm non','2002-11-13','Nữ','Huế','nguyenbichduyen@example.com',1),(3127045789,'Phan Thanh Tâm','Đại trà','Giáo dục tiểu học','2001-05-07','Nữ','Đắk Lắk','thantam@gmail.com',1),(3127045932,'Lê Văn Kiệt','CLC','Quốc tế học','2004-06-25','Nam','Đồng Nai','levankiet@example.com',1),(3127158043,'Võ Minh Đức','CLC','Điện tử','2003-09-18','Nam','Bắc Giang','vominhduc@example.com',1),(3127261156,'Nguyễn Tuấn Anh','Đại trà','Công nghệ thông tin','2001-02-02','Nam','Bình Phước','nguyentuananh@example.com',1),(3127379269,'Hoàng Lan Anh','CLC','Kinh doanh quốc tế','2002-04-13','Nữ','Kiên Giang','hoanglananh@example.com',1),(3127485371,'Đặng Quang Hieu','CLC','Ngôn ngữ Anh','2000-07-25','Nam','Hà Nam','dangquanghieu@example.com',1),(3127590485,'Nguyễn Đình Khoa','Đại trà','Giáo dục mầm non','2003-08-14','Nam','Quảng Ninh','nguyendinhkhoa@example.com',1),(3127702598,'Phan Thị Thanh','CLC','Tài chính ngân hàng','2001-12-20','Nữ','Cà Mau','phanthithanh@example.com',1),(3127812709,'Trịnh Mai Linh','Đại trà','Công nghệ thông tin','2003-03-17','Nữ','Hải Phòng','trinhmailinh@example.com',1),(3127923810,'Vũ Thanh Sơn','CLC','Kế toán','2002-08-02','Nam','Hà Nội','vuthanhson@example.com',1),(3128034921,'Lê Quang Hải','Đại trà','Giáo dục mầm non','2000-10-29','Nam','Thanh Hóa','lequanghai@example.com',1),(3128146034,'Nguyễn Thanh Tùng','Đại trà','Quốc tế học','2001-07-11','Nam','Cần Thơ','nguyenthantung@example.com',1);
/*!40000 ALTER TABLE `sinh_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tai_khoan`
--

DROP TABLE IF EXISTS `tai_khoan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tai_khoan` (
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `vai_tro` enum('admin','giang_vien','tro_giang') DEFAULT NULL,
  `ma_nguoi_dung` varchar(50) NOT NULL,
  PRIMARY KEY (`ma_nguoi_dung`),
  UNIQUE KEY `username` (`username`),
  KEY `tk_vaitro_vt` (`vai_tro`),
  CONSTRAINT `tk_vaitro_vt` FOREIGN KEY (`vai_tro`) REFERENCES `vai_tro` (`ten_vai_tro`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tai_khoan`
--

LOCK TABLES `tai_khoan` WRITE;
/*!40000 ALTER TABLE `tai_khoan` DISABLE KEYS */;
INSERT INTO `tai_khoan` VALUES ('nguyenvanan1','123456','giang_vien','501'),('tranbich02','123456','giang_vien','502'),('leminhtuan3','123456','giang_vien','503'),('phamngoch4','123456','giang_vien','504'),('doquangvinh5','123456','giang_vien','505'),('hoangthiyen6','123456','giang_vien','506'),('vuhailong7','123456','giang_vien','507'),('ngothanhtung8','123456','giang_vien','508'),('dangthilan9','123456','giang_vien','509'),('buianhduc10','123456','giang_vien','510'),('nguyenthimai11','123456','giang_vien','511'),('tranvannam12','123456','giang_vien','512'),('lethithu13','123456','giang_vien','513'),('phamminhphuong14','123456','giang_vien','514'),('dothihong15','123456','giang_vien','515'),('hoangminhtri16','123456','giang_vien','516'),('vuthiduyen17','123456','giang_vien','517'),('ngominhnhat18','123456','giang_vien','518'),('dangquoctoan19','123456','giang_vien','519'),('buithingoc20','123456','giang_vien','520'),('admin','admin123','admin','admin');
/*!40000 ALTER TABLE `tai_khoan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vai_tro`
--

DROP TABLE IF EXISTS `vai_tro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vai_tro` (
  `id` int NOT NULL,
  `ten_vai_tro` enum('admin','giang_vien','tro_giang') COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ten_vai_tro` (`ten_vai_tro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vai_tro`
--

LOCK TABLES `vai_tro` WRITE;
/*!40000 ALTER TABLE `vai_tro` DISABLE KEYS */;
INSERT INTO `vai_tro` VALUES (100,'admin'),(200,'giang_vien'),(201,'tro_giang');
/*!40000 ALTER TABLE `vai_tro` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-29 14:00:18
