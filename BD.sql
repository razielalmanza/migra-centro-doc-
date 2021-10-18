-- MySQL Script generated by MySQL Workbench
-- Fri Feb 12 02:28:09 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema documentacion
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `documentacion` ;

-- -----------------------------------------------------
-- Schema documentacion
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `documentacion` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `documentacion` ;

-- -----------------------------------------------------
-- Table `documentacion`.`cat_values`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cat_values` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cat_values` (
  `tname` VARCHAR(50) NOT NULL,
  `fname` VARCHAR(50) NOT NULL,
  `val` VARCHAR(80) NOT NULL,
  `display_value` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`tname`, `fname`, `val`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_cat_personalidades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_cat_personalidades` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_cat_personalidades` (
  `idcd_cat_personalidades` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre_artistico` VARCHAR(100) NOT NULL,
  `nombre_verdadero` VARCHAR(100) NULL,
  `sobrenombre` VARCHAR(100) NULL,
  `a_r_acervo_repetido` INT NULL,
  PRIMARY KEY (`idcd_cat_personalidades`),
  INDEX `idx_nombre_art` (`nombre_artistico` ASC) VISIBLE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_cat_titulos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_cat_titulos` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_cat_titulos` (
  `idcd_cat_titulos` BIGINT NOT NULL AUTO_INCREMENT,
  `titulo_original` VARCHAR(250) NOT NULL,
  `titulo_en_espa` VARCHAR(250) NOT NULL DEFAULT '',
  `anio` SMALLINT NOT NULL DEFAULT 0,
  `anio_fin` SMALLINT NULL DEFAULT NULL COMMENT 'Si es un rango de años',
  `pais_de_realizacion` VARCHAR(70) NULL DEFAULT NULL,
  `circa` BIT(1) NOT NULL DEFAULT b'0' COMMENT 'Si el año o rango de años es estimado',
  PRIMARY KEY (`idcd_cat_titulos`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_contenedores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_contenedores` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_contenedores` (
  `id_contenedor` VARCHAR(13) NOT NULL,
  `id_hex_lto` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`id_contenedor`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_interpretes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_interpretes` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_interpretes` (
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`nombre`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item` (
  `idcd_item` BIGINT NOT NULL AUTO_INCREMENT,
  `idcd_cat_titulos` BIGINT NULL,
  `idcd_cat_personalidades` BIGINT NULL,
  `fechaHoraInsercion` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `tipo_item` VARCHAR(45) NOT NULL COMMENT 'Se obtiene de cat_values {cartel, fotomontaje, personalidad, still, fotografía de rodaje, video}',
  `imagen_digital` VARCHAR(50) NULL,
  `campos_comunes` VARCHAR(45) NULL DEFAULT NULL,
  `foto_old_interpretes` VARCHAR(500) NULL DEFAULT NULL,
  `activo` TINYINT(1) NOT NULL DEFAULT 1,
  `colocacion` VARCHAR(100) NULL,
  `notas` VARCHAR(350) NULL,
  PRIMARY KEY (`idcd_item`),
  INDEX `fk_cd_item_cd_cat_titulos1_idx` (`idcd_cat_titulos` ASC) VISIBLE,
  INDEX `fk_cd_item_cd_item_personalidades1_idx` (`idcd_cat_personalidades` ASC) VISIBLE,
  CONSTRAINT `fk_cd_item_cd_cat_titulos1`
    FOREIGN KEY (`idcd_cat_titulos`)
    REFERENCES `documentacion`.`cd_cat_titulos` (`idcd_cat_titulos`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_cd_item_cd_item_personalidades1`
    FOREIGN KEY (`idcd_cat_personalidades`)
    REFERENCES `documentacion`.`cd_cat_personalidades` (`idcd_cat_personalidades`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item_cartel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item_cartel` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item_cartel` (
  `idcd_item` BIGINT NOT NULL,
  `institucion` VARCHAR(500) NULL,
  `pais` VARCHAR(62) NULL,
  `tama` VARCHAR(37) NULL,
  `ejemplares` VARCHAR(62) NULL,
  `diseniador` VARCHAR(112) NULL,
  `tecnica` VARCHAR(250) NULL,
  `estado_fisico` VARCHAR(25) NULL,
  `car_consulta` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idcd_item`),
  INDEX `fk_cd_item_cartel_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  CONSTRAINT `fk_cd_item_cartel_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item_digital`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item_digital` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item_digital` (
  `idcd_item` BIGINT NOT NULL,
  `extension` VARCHAR(10) NOT NULL DEFAULT '' COMMENT 'Usa cat_values {TIFF, JPEG, PNG, ...}',
  `resolucion` VARCHAR(20) NOT NULL DEFAULT '' COMMENT 'Usa cat_values',
  `dpi` INT NULL,
  `espacio_color` VARCHAR(20) NULL COMMENT 'Usa cat_values',
  `profundidad_bits` SMALLINT NULL,
  `nombre_archivo` VARCHAR(100) NOT NULL,
  `nombre_proxy` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idcd_item`),
  INDEX `fk_cd_imagen_digital_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  CONSTRAINT `fk_cd_imagen_digital_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item_fotomontajes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item_fotomontajes` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item_fotomontajes` (
  `idcd_item` BIGINT NOT NULL,
  `ejemplares` VARCHAR(100) NULL,
  `pais` VARCHAR(70) NULL,
  INDEX `fk_cd_item_fotomontajes_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  PRIMARY KEY (`idcd_item`),
  CONSTRAINT `fk_cd_item_fotomontajes_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item_fotos_rodaje`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item_fotos_rodaje` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item_fotos_rodaje` (
  `idcd_item` BIGINT NOT NULL,
  `tama` VARCHAR(40) NULL,
  `color` VARCHAR(50) NULL,
  PRIMARY KEY (`idcd_item`),
  INDEX `fk_cd_item_fotos_rodaje_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  CONSTRAINT `fk_cd_item_fotos_rodaje_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_item_stills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_item_stills` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_item_stills` (
  `idcd_item` BIGINT NOT NULL,
  `a_r_` INT NULL,
  `a_f_total_ejemplares` VARCHAR(50) NULL,
  INDEX `fk_cd_item_stills_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  PRIMARY KEY (`idcd_item`),
  CONSTRAINT `fk_cd_item_stills_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_personas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_personas` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_personas` (
  `idcd_personas` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(350) NOT NULL,
  `tipo_persona` CHAR(1) NOT NULL DEFAULT 'F' COMMENT '{F=Fisica, M=Moral}',
  PRIMARY KEY (`idcd_personas`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_trans_item_digital_contenedores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_trans_item_digital_contenedores` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_trans_item_digital_contenedores` (
  `idcd_item` BIGINT NOT NULL,
  `id_contenedor` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`idcd_item`, `id_contenedor`),
  INDEX `fk_cd_item_digital_has_cd_contenedores_cd_contenedores1_idx` (`id_contenedor` ASC) VISIBLE,
  INDEX `fk_cd_item_digital_has_cd_contenedores_cd_item_digital1_idx` (`idcd_item` ASC) VISIBLE,
  CONSTRAINT `fk_cd_item_digital_has_cd_contenedores_cd_item_digital1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item_digital` (`idcd_item`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_cd_item_digital_has_cd_contenedores_cd_contenedores1`
    FOREIGN KEY (`id_contenedor`)
    REFERENCES `documentacion`.`cd_contenedores` (`id_contenedor`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_trans_item_interpretes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_trans_item_interpretes` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_trans_item_interpretes` (
  `idcd_item` BIGINT NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `xy_start` VARCHAR(20) NULL DEFAULT NULL,
  `xy_end` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`idcd_item`, `nombre`),
  INDEX `fk_cd_item_has_cd_interpretes_cd_interpretes1_idx` (`nombre` ASC) VISIBLE,
  INDEX `fk_cd_item_has_cd_interpretes_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  CONSTRAINT `fk_cd_item_has_cd_interpretes_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_cd_item_has_cd_interpretes_cd_interpretes1`
    FOREIGN KEY (`nombre`)
    REFERENCES `documentacion`.`cd_interpretes` (`nombre`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_trans_personas_cat_titulos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_trans_personas_cat_titulos` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_trans_personas_cat_titulos` (
  `idcd_cat_titulos` BIGINT NOT NULL,
  `idcd_personas` BIGINT NOT NULL,
  `rol` VARCHAR(80) NOT NULL COMMENT 'Usa cat_values {Realizador, Productor, Guionista, Fotógrafo, ...} ',
  PRIMARY KEY (`idcd_cat_titulos`, `idcd_personas`),
  INDEX `fk_cd_personas_has_cd_cat_titulos_cd_cat_titulos1_idx` (`idcd_cat_titulos` ASC) VISIBLE,
  INDEX `fk_cd_personas_has_cd_cat_titulos_cd_personas_idx` (`idcd_personas` ASC) VISIBLE,
  CONSTRAINT `fk_cd_personas_has_cd_cat_titulos_cd_personas`
    FOREIGN KEY (`idcd_personas`)
    REFERENCES `documentacion`.`cd_personas` (`idcd_personas`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_cd_personas_has_cd_cat_titulos_cd_cat_titulos1`
    FOREIGN KEY (`idcd_cat_titulos`)
    REFERENCES `documentacion`.`cd_cat_titulos` (`idcd_cat_titulos`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `documentacion`.`cd_vhs_dvd`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentacion`.`cd_vhs_dvd` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `documentacion`.`cd_vhs_dvd` (
  `idcd_item` BIGINT NOT NULL,
  `formato` VARCHAR(10) NULL,
  `color` VARCHAR(100) NULL,
  `audio` VARCHAR(50) NULL,
  `idioma` VARCHAR(100) NULL,
  `subtitulos` VARCHAR(200) NULL,
  `intertitulos` VARCHAR(50) NULL,
  `norma` VARCHAR(4) NULL,
  `duracion` TIME NULL,
  `region` VARCHAR(16) NULL,
  `pantalla` VARCHAR(100) NULL,
  `observaciones` VARCHAR(800) NULL,
  `extras` VARCHAR(50) NULL,
  INDEX `fk_cd_vhs_dvd_cd_item1_idx` (`idcd_item` ASC) VISIBLE,
  PRIMARY KEY (`idcd_item`),
  CONSTRAINT `fk_cd_vhs_dvd_cd_item1`
    FOREIGN KEY (`idcd_item`)
    REFERENCES `documentacion`.`cd_item` (`idcd_item`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
