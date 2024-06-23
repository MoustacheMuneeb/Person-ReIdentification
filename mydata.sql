-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 23, 2024 at 09:44 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mydata`
--

-- --------------------------------------------------------

--
-- Table structure for table `cameraconfig`
--

CREATE TABLE `cameraconfig` (
  `CameraID` int(10) NOT NULL,
  `IPAddress` varchar(16) NOT NULL,
  `CameraName` varchar(100) NOT NULL,
  `Location` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cameraconfig`
--

INSERT INTO `cameraconfig` (`CameraID`, `IPAddress`, `CameraName`, `Location`) VALUES
(1, '192.168.10.12', 'camera1', 'Home'),
(2, '1192.168.10.12', 'camera2', 'Home'),
(3, '192.168.10.12', 'Camer1', 'Home'),
(4, '192.168.1.12', 'camer1', 'Home'),
(5, '192.168.1.12', 'camera1 ', 'home'),
(6, '192.168.1.12', 'camera1', 'home'),
(7, '192.168.1.12', 'camera1', 'home'),
(8, 'rtsp://192.168.1', 'camera1', 'home'),
(9, 'rtsp://192.168.1', 'misha', 'home'),
(10, 'rtsp://192.168.1', 'camera1', 'home'),
(11, 'rtsp://192.168.1', 'camera', 'home'),
(12, 'rtsp://192.168.1', 'camera', 'home'),
(13, 'rtsp://192.168.1', 'camera', 'home'),
(14, 'rtsp://192.168.1', 'camera1', 'home '),
(15, 'rtsp://192.168.1', 'camera11', 'home'),
(16, 'rtsp://192.168.1', 'camera', 'home'),
(17, 'rtsp://192.168.1', 'camera1', 'home'),
(18, 'rtsp://192.186.1', 'camera1', 'home'),
(19, 'rtsp://192.168.1', 'camera1', 'home');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `ID` int(11) NOT NULL,
  `Email` varchar(20) NOT NULL,
  `Password` varchar(8) NOT NULL,
  `user_type` int(1) NOT NULL DEFAULT 1,
  `status` int(1) NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `modification_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`ID`, `Email`, `Password`, `user_type`, `status`, `creation_date`, `modification_date`) VALUES
(2, 'misha@gmail.com', '7890', 0, 1, '2024-04-17 16:54:24', '2024-04-17 16:54:24'),
(27, 'sajal05@gmail.com', '890abc@', 0, 1, '2024-04-19 07:09:45', '2024-04-19 07:09:45'),
(49, 'hey', 'abc', 1, 1, '2024-05-23 08:23:06', '2024-05-23 08:23:06'),
(50, 'iqra123@gmail.com', '123abc12', 1, 1, '2024-05-23 09:23:34', '2024-05-23 09:23:34'),
(51, 'umme123@gmail.com', 'ummeiop6', 1, 0, '2024-05-28 12:58:00', '2024-05-28 12:58:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cameraconfig`
--
ALTER TABLE `cameraconfig`
  ADD PRIMARY KEY (`CameraID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cameraconfig`
--
ALTER TABLE `cameraconfig`
  MODIFY `CameraID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
