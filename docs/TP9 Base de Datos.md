---
coverConfig:
  showCover: true
  title: Trabajo Practico 9
  subtitle: ''
  materia: Base de Datos
  coverStyle: barra_azul
  integrantes:
    - Chatelain Agustin
    - Galdini Jenaro
    - Hartmann Kevin
    - ''
  profesores:
    - Ing. Esteban Schab
    - Aus. Gabriel Caseres
    - Aux. Tomas Viñuela
    - ''
  sigla: TI
  fecha: 07/09/2026
  showHeader: false
  showFooter: false
activeTheme: minimal
---
## Punto 1
![Imagen](/uploads/img_1788828070069.png)

## Punto 2
El Diccionario lo entregamos aparte.
\newpage
## Punto 3

```SQL
VAR BASE RELATION Ciudad(CP int, nombre varchar(50), PRIMARY KEY(CP))

VAR BASE RELATION Sucursal(idSucursal int, nombre varchar(50), calle varchar(50),
numero int, CP int, PRIMARY KEY(idSucursal), FOREIGN KEY(CP) REFERENCES Ciudad)

VAR BASE RELATION Cliente(DNI int, apellido varchar(30), nombre varchar(30),
PRIMARY KEY(DNI))

VAR BASE RELATION TipoCuenta(codigo int, nombre varchar(30), PRIMARY KEY(codigo))

VAR BASE RELATION Cuenta(numero int, denominacion varchar(50), activa boolean, 
DNI int, codigoTipo int, idSucursal int, PRIMARY KEY(numero), 
FOREIGN KEY(DNI) REFERENCES Cliente,
FOREIGN KEY(codigoTipo) REFERENCES TipoCuenta, 
FOREIGN KEY(idSucursal) REFERENCES Sucursal)

VAR BASE RELATION TipoTransaccion(idTipo int, nombre varchar(30), categoria varchar(10),
PRIMARY KEY(idTipo))

VAR BASE RELATION Transaccion(idTransaccion int, fecha datetime, monto double,
descripcion varchar(100), numeroCuenta int, idTipo int, 
PRIMARY KEY(idTransaccion),
FOREIGN KEY(numeroCuenta) REFERENCES Cuenta, FOREIGN KEY(idTipo) 
REFERENCES TipoTransaccion)
```
## Punto 4,5,6 Se entregan Aparte
