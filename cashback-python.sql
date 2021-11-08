-- MySQL Script generated by MySQL Workbench
-- Sun Nov  7 20:57:45 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `pvalue` FLOAT NULL,
  `productType` VARCHAR(1) NOT NULL,
  PRIMARY KEY (`idproduct`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`customer` (
  `idcustomer` INT NOT NULL AUTO_INCREMENT,
  `cname` VARCHAR(45) NULL,
  `document` DOUBLE NULL,
  PRIMARY KEY (`idcustomer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sale`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`sale` (
  `idsale` INT NOT NULL AUTO_INCREMENT,
  `customer_idcustomer` INT NULL,
  `sold_at` DATETIME NULL,
  `cashback` FLOAT NULL,
  PRIMARY KEY (`idsale`),
  INDEX `fk_selling_costumer1_idx` (`customer_idcustomer` ASC) VISIBLE,
  CONSTRAINT `fk_selling_costumer1`
    FOREIGN KEY (`customer_idcustomer`)
    REFERENCES `mydb`.`customer` (`idcustomer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`product_has_sale`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`product_has_sale` (
  `idproduct_has_sale` INT NOT NULL AUTO_INCREMENT,
  `product_idproduct` INT NOT NULL,
  `sale_idsale` INT NOT NULL,
  PRIMARY KEY (`idproduct_has_sale`),
  INDEX `fk_product_has_selling_product1_idx` (`product_idproduct` ASC) VISIBLE,
  INDEX `fk_product_has_selling_selling1_idx` (`sale_idsale` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_selling_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `mydb`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_selling_selling1`
    FOREIGN KEY (`sale_idsale`)
    REFERENCES `mydb`.`sale` (`idsale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;