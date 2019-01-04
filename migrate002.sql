BEGIN;
--
-- Remove field CNum from car
--
ALTER TABLE `Car`
  DROP COLUMN `CNum`;
--
-- Alter field ZSDName on accident
--
ALTER TABLE `Accident`
  DROP FOREIGN KEY `Accident_ZSDName_id_d2f2c50e_fk_Driver_id`;
DROP INDEX `Accident_ZSDName_id_d2f2c50e_fk_Driver_id` ON `Accident`;
ALTER TABLE `Accident`
  CHANGE `ZSDName_id` `ZSDName` varchar(20) NOT NULL;
ALTER TABLE `Accident`
  MODIFY `ZSDName` varchar(20) NOT NULL;
--
-- Alter field DName on record
--
ALTER TABLE `Record`
  DROP FOREIGN KEY `Record_DName_id_a86aa16d_fk_Driver_id`;
DROP INDEX `Record_DName_id_a86aa16d_fk_Driver_id` ON `Record`;
ALTER TABLE `Record`
  CHANGE `DName_id` `DName` varchar(20) NOT NULL;
ALTER TABLE `Record`
  MODIFY `DName` varchar(20) NOT NULL;
COMMIT;
