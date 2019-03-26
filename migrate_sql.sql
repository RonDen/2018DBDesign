BEGIN;
--
-- Create model Accident
--
CREATE TABLE `Accident`
(
  `id`       integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `SGCNo`    varchar(20)            NOT NULL,
  `Time`     datetime(6)            NOT NULL,
  `Spot`     varchar(50)            NOT NULL,
  `Cause`    longtext               NOT NULL,
  `Money`    integer                NOT NULL,
  `isDelete` bool                   NOT NULL
);
--
-- Create model Car
--
CREATE TABLE `Car`
(
  `CNo`              varchar(20) NOT NULL PRIMARY KEY,
  `CType`            varchar(10) NOT NULL,
  `CNum`             integer     NOT NULL,
  `COilConsumpution` integer     NOT NULL,
  `isAvailable`      bool        NOT NULL
);
--
-- Create model Driver
--
CREATE TABLE `Driver`
(
  `id`          integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `DName`       varchar(10)            NOT NULL,
  `DSex`        bool                   NOT NULL,
  `DAge`        smallint               NOT NULL,
  `PhoneNum`    varchar(11)            NOT NULL,
  `Hiredata`    date                   NOT NULL,
  `isAvailable` bool                   NOT NULL
);
--
-- Create model Proposer
--
CREATE TABLE `Proposer`
(
  `id`        integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `CType`     varchar(10)            NOT NULL,
  `Num`       integer                NOT NULL,
  `Mileage`   integer                NOT NULL,
  `Date`      datetime(6)            NOT NULL,
  `isRecived` bool                   NOT NULL
);
--
-- Create model Record
--
CREATE TABLE `Record`
(
  `id`              integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `STime`           datetime(6)            NOT NULL,
  `ETime`           datetime(6)            NOT NULL,
  `OilConsumpution` integer                NOT NULL,
  `isDelete`        bool                   NOT NULL,
  `CNo_id`          varchar(20)            NOT NULL,
  `DName_id`        integer                NOT NULL,
  `DNo_id`          integer                NOT NULL
);
--
-- Add field ZSCNo to accident
--
ALTER TABLE `Accident`
  ADD COLUMN `ZSCNo_id` varchar(20) NOT NULL;
--
-- Add field ZSDName to accident
--
ALTER TABLE `Accident`
  ADD COLUMN `ZSDName_id` integer NOT NULL;
--
-- Add field ZSDNo to accident
--
ALTER TABLE `Accident`
  ADD COLUMN `ZSDNo_id` integer NOT NULL;
ALTER TABLE `Record`
  ADD CONSTRAINT `Record_CNo_id_5f972d32_fk_Car_CNo` FOREIGN KEY (`CNo_id`) REFERENCES `Car` (`CNo`);
ALTER TABLE `Record`
  ADD CONSTRAINT `Record_DName_id_a86aa16d_fk_Driver_id` FOREIGN KEY (`DName_id`) REFERENCES `Driver` (`id`);
ALTER TABLE `Record`
  ADD CONSTRAINT `Record_DNo_id_9850de20_fk_Driver_id` FOREIGN KEY (`DNo_id`) REFERENCES `Driver` (`id`);
ALTER TABLE `Accident`
  ADD CONSTRAINT `Accident_ZSCNo_id_03c692f0_fk_Car_CNo` FOREIGN KEY (`ZSCNo_id`) REFERENCES `Car` (`CNo`);
ALTER TABLE `Accident`
  ADD CONSTRAINT `Accident_ZSDName_id_d2f2c50e_fk_Driver_id` FOREIGN KEY (`ZSDName_id`) REFERENCES `Driver` (`id`);
ALTER TABLE `Accident`
  ADD CONSTRAINT `Accident_ZSDNo_id_17e6003e_fk_Driver_id` FOREIGN KEY (`ZSDNo_id`) REFERENCES `Driver` (`id`);
COMMIT;
