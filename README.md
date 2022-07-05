

# Sistema de Prevención y Detección de Intrusos: HIPS.

### Proyecto para la materia Sistemas Operativos 2. Universidad Nuestra Señora de la Asunción. Facultad de Ciencias y Tecnologia.
Desarrollado por:
- José Alarcón
- Ramón Araujo
#### Asunción, Paraguay. Año 2022.

El proyecto esta desarrollado principalmente en Python, con la utilizacion de las herramientas Django y PostgreSQL. Las funcionalidades implementadas estan
detalladas en el documento de **[requerimientos.](https://drive.google.com/file/d/141qbkyMJk1pZSEaTXLePYMuaU909uMvg/view?usp=sharing)** Mas abajo se detalla el
manual de instalación y los requerimientos previos.

### Pre-Requisitos:

_Para el correcto funcionamiento de la HIPS, necesitamos instalar las siguiente librerias_
```
sudo apt-get install python3
sudo apt-get install django
```
_Tener instalado Postgres y ejecutar el siguiente script en consola_
```
sudo su  - postgres
psql
create user so2 with password '2022';
create database dbso2;
grant all privileges on database dbso2 to so2;


```
_Antes de empezar con la instalación es importante crear un log de usuarios del shell, en el directorio /var/log/shell_

```
$touch /var/log/shell/usario_horario.log
$touch /var/log/shell/horario_de_trabajo.log
$touch /var/log/shell/movimientos.log
$touch /var/log/shell/sistema_error.log
$touch /var/log/shell/transferencia.log
```
_Nos aseguramos de que el directorio tenga todos los permisos_
```
$chmod -R 777 /var/log/shell
```

### Instalación 🔧

_Una serie de  paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_


_Mediante el uso de un dispotivo de almacenamiento usb copiamos los archivos del Shell al directorio /_

```
$cp -r /media/usb/Shell_LFS-main/shell.py /
```

_Asumiendo que el dispositivo se encuentra montado en /media/usb
Desde el directorio / ($cd / ) creamos un script de ejecucion del shell_

```
$vi shell.sh
  #!/bin/bash
  python3 shell.py
```

_Ahora solo queda agregar el shell al archivo /etc/profile_
```
$echo "bash /shell.sh" >> /etc/profile
```
_Reiniciamos el sistema_
```
$shutdown -r now
```
_Ahora el shell deberia de cargarse automaticamente y esta listo para utilizar._

## Uso del Shell ⌨️
