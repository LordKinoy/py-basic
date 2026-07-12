-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 11, 2026 at 11:59 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_oop`
--

-- --------------------------------------------------------

--
-- Table structure for table `barang`
--

CREATE TABLE `barang` (
  `id` int NOT NULL,
  `kode_barang` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nama_barang` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `satuan_barang` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `harga_barang` int NOT NULL,
  `stock` int DEFAULT NULL,
  `diskon` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang`
--

INSERT INTO `barang` (`id`, `kode_barang`, `nama_barang`, `satuan_barang`, `harga_barang`, `stock`, `diskon`) VALUES
(1, 'BRG0001', 'Keyboard Press Play Rover 84 Lightyear Edition', 'Pcs', 1800000, 4, 0),
(2, 'BRG0002', 'Mouse Razer Deathadder', 'Pcs', 350000, 9, 0),
(3, 'BRG0003', 'Monitor MSI MAG 25 200Hz 2K', 'Pcs', 2500000, 13, 0),
(4, 'BRG0004', 'HDMI to VGA Adapter', 'Pcs', 150000, 8, 0),
(5, 'BRG0005', 'TWS Moondrop Space Travel', 'Pcs', 300000, 18, 10),
(6, 'BRG0006', 'Mouse Pad Rexus KVLAR', 'Pcs', 100000, 10, 0),
(7, 'BRG0007', 'Acer Nitro V15 i5-13th RTX2050 DDR5 8GB SSD 512GB', 'Pcs', 10000000, 10, 0);

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id` int NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` varchar(20) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id`, `nama`, `no_hp`) VALUES
(1, 'Panjul', '08994566179'),
(2, 'Teddy', '08994566178'),
(3, 'Prabowo', '8994566177'),
(4, 'Pigai', '08994566176'),
(5, 'Bahlil', '08994566175'),
(6, 'Owibowo', '082731456684'),
(7, 'Febrie UPDATED', '089287377227');

-- --------------------------------------------------------

--
-- Table structure for table `penjualan`
--

CREATE TABLE `penjualan` (
  `id` int NOT NULL,
  `tanggal` datetime DEFAULT NULL,
  `pelanggan` int DEFAULT NULL,
  `sales` int DEFAULT NULL,
  `jenis_pembayaran` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `total` int DEFAULT NULL,
  `bayar` int DEFAULT NULL,
  `kembali` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penjualan`
--

INSERT INTO `penjualan` (`id`, `tanggal`, `pelanggan`, `sales`, `jenis_pembayaran`, `total`, `bayar`, `kembali`) VALUES
(19, '2026-07-07 09:41:21', NULL, 1, 'TUNAI', 2575200, 2600000, 24800),
(20, '2026-07-07 10:59:30', NULL, 1, 'TUNAI', 3108000, 3200000, 92000),
(21, '2026-07-07 11:02:52', 5, 1, 'TUNAI', 4502715, 5000000, 497285),
(22, '2026-07-07 11:11:06', NULL, 1, 'TUNAI', 4573200, 5000000, 426800),
(23, '2026-07-07 11:13:28', NULL, 1, 'TUNAI', 2519700, 3000000, 480300),
(24, '2026-07-07 11:35:37', NULL, 1, 'TUNAI', 2186700, 2200000, 13300),
(25, '2026-07-07 11:42:07', NULL, 1, 'TUNAI', 4961700, 5000000, 38300),
(26, '2026-07-07 11:47:03', NULL, 1, 'TUNAI', 2353200, 5000000, 2646800),
(27, '2026-07-07 13:09:57', 5, 1, 'TUNAI', 2077365, 2100000, 22635),
(28, '2026-07-07 13:16:54', NULL, 1, 'TUNAI', 1964700, 2000000, 35300),
(29, '2026-07-07 13:21:17', 5, 1, 'TUNAI', 2077365, 2100000, 22635),
(30, '2026-07-07 13:26:55', 5, 1, 'TUNAI', 527250, 600000, 72750),
(31, '2026-07-07 13:33:33', 5, 1, 'TUNAI', 4502715, 5000000, 497285),
(32, '2026-07-07 13:41:14', NULL, 1, 'TUNAI', 4739700, 5000000, 260300),
(33, '2026-07-07 13:43:35', NULL, 1, 'TUNAI', 2353200, 5000000, 2646800),
(34, '2026-07-07 13:49:53', NULL, 1, 'TUNAI', 5516700, 6000000, 483300),
(35, '2026-07-07 14:00:58', 5, 1, 'TUNAI', 2182815, 2200000, 17185),
(36, '2026-07-07 14:03:08', NULL, 1, 'TUNAI', 2353200, 2500000, 146800);

-- --------------------------------------------------------

--
-- Table structure for table `penjualan_detail`
--

CREATE TABLE `penjualan_detail` (
  `id` int NOT NULL,
  `penjualan_id` int NOT NULL,
  `kode_barang` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nama_barang` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jumlah` int NOT NULL,
  `satuan` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `harga` int NOT NULL,
  `diskon` int NOT NULL,
  `after_diskon` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penjualan_detail`
--

INSERT INTO `penjualan_detail` (`id`, `penjualan_id`, `kode_barang`, `nama_barang`, `jumlah`, `satuan`, `harga`, `diskon`, `after_diskon`) VALUES
(13, 19, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(14, 19, 'BRG0002', 'Mouse', 2, 'Pcs', 350000, 0, 350000),
(15, 20, 'BRG0004', 'HDMI to VGA Adapter', 2, 'Pcs', 150000, 0, 150000),
(16, 20, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(17, 21, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(18, 21, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(19, 21, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(20, 22, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(21, 22, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(22, 23, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(23, 23, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(24, 23, 'BRG0005', 'TWS', 1, 'Pcs', 300000, 0, 300000),
(25, 24, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(26, 24, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(27, 25, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(28, 25, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(29, 25, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(30, 26, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(31, 26, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(32, 26, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(33, 27, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(34, 27, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(35, 28, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(36, 28, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(37, 29, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(38, 29, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(39, 30, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(40, 30, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(41, 31, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(42, 31, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(43, 31, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(44, 32, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(45, 32, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(46, 32, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(47, 33, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(48, 33, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000),
(49, 33, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(50, 34, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(51, 34, 'BRG0002', 'Mouse', 2, 'Pcs', 350000, 0, 350000),
(52, 34, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(53, 34, 'BRG0003', 'Monitor', 1, 'Pcs', 2500000, 0, 2500000),
(54, 35, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(55, 35, 'BRG0005', 'TWS', 1, 'Pcs', 300000, 0, 300000),
(56, 35, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(57, 36, 'BRG0001', 'Keyboard', 1, 'Pcs', 1800000, 10, 1620000),
(58, 36, 'BRG0004', 'HDMI to VGA Adapter', 1, 'Pcs', 150000, 0, 150000),
(59, 36, 'BRG0002', 'Mouse', 1, 'Pcs', 350000, 0, 350000);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `is_lock` int DEFAULT NULL,
  `login_attempt` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `is_lock`, `login_attempt`) VALUES
(1, 'krisna', '$2b$12$08yL12Zey3dVmnnLVb3uOuJ5oKHHMgodWnAXjQVXkKb1iUxIBg6ce', 'krisna.unyu8@gmail.com', NULL, 0),
(2, 'kinoy', '$2b$12$bQ7K4SvtamAFFRBrkfdE8OqTZ2L37ty2D.DwnIrchn3rtlsK9IE7e', 'kinoy@gmail.com', NULL, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `no_hp` (`no_hp`);

--
-- Indexes for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_penjualan_sales` (`sales`);

--
-- Indexes for table `penjualan_detail`
--
ALTER TABLE `penjualan_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pd_penjualan` (`penjualan_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barang`
--
ALTER TABLE `barang`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `penjualan`
--
ALTER TABLE `penjualan`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `penjualan_detail`
--
ALTER TABLE `penjualan_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD CONSTRAINT `fk_penjualan_sales` FOREIGN KEY (`sales`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `penjualan_detail`
--
ALTER TABLE `penjualan_detail`
  ADD CONSTRAINT `fk_pd_penjualan` FOREIGN KEY (`penjualan_id`) REFERENCES `penjualan` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
