-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 04, 2020 at 12:58 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.2.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `employee`
--

-- --------------------------------------------------------

--
-- Table structure for table `edit_employee`
--

CREATE TABLE `edit_employee` (
  `ID` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Contact` varchar(20) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `DOB` varchar(50) NOT NULL,
  `PAN_Card` varchar(50) NOT NULL,
  `Aadhar_Card` varchar(50) NOT NULL,
  `Address` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `edit_employee`
--

INSERT INTO `edit_employee` (`ID`, `Name`, `Contact`, `Email`, `Department`, `DOB`, `PAN_Card`, `Aadhar_Card`, `Address`) VALUES
('E000005', 'a', '7000070000', '-', 'Electronics', '13/02/4020', '-', '-', '-\n'),
('E00001', 'RAMU', '9009009009', 'ramu.123@gmail.com', 'Furniture', '02/07/2020', '-', '-', '-\n\n'),
('E10001', 'RAMU', '9009009009', 'ramu.123@gmail.com', 'Furniture', '02/07/2020', '-', '-', '-\n\n'),
('E10002', 'BHARAT PANT', '1234567890', 'bharat1234@gmail.com', 'Clothing', '10/10/1010', '34567890', '1234567890', '426511,c block,faridabad\n'),
('E102233', 'BHARAT', '7012121212', 'bharat@1234', 'Electronics', '13/02/1999', '-', '-', '-\n'),
('F00001', 'RAMU', '9009009009', 'ramu.123@gmail.com', 'Furniture', '02/07/2020', '-', '-', '-\n');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `LoginID` varchar(50) NOT NULL,
  `Password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`LoginID`, `Password`) VALUES
('BHARAT PANT', 'BHARAT PANT'),
('E000005', '4020@0000'),
('E00001', '2020@9009'),
('E10001', '2020@9009'),
('E10002', '1010@7890'),
('E102233', '1999@1212'),
('F00001', '2020@9009');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `edit_employee`
--
ALTER TABLE `edit_employee`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`LoginID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
