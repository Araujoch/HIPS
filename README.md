

# Sistema de Prevención y Detección de Intrusos: HIPS.

### Proyecto para la materia Sistemas Operativos 2. Universidad Nuestra Señora de la Asunción. Facultad de Ciencias y Tecnologia.
Desarrollado por:
- José Alarcón
- Ramón Araujo
#### Asunción, Paraguay. Año 2022.

El proyecto esta diseñado para correr sobre un sistema CentOS 8, desarrollado principalmente en Python, con la utilizacion de las herramientas Django y PostgreSQL. Las funcionalidades implementadas estan
detalladas en el documento de **[requerimientos.](https://drive.google.com/file/d/141qbkyMJk1pZSEaTXLePYMuaU909uMvg/view?usp=sharing)** Mas abajo se detalla el
manual de instalación y los requerimientos previos.

## Manual de Instalación:

Para el correcto funcionamiento de la HIPS, primero necesitaremos las siguientes herrmanientas:
- Python
- PostgreSQL
- Django
- Psycopg2
- Lsof
#### Podemos instalar mediante los comandos:
```
sudo dnf install git
sudo dnf install lsof
sudo dnf install python38
sudo dnf install python3-pip
pip3 install django
cp /usr/local/bin/django-admin /usr/bin/ (Pasamos django al usr/bin)
sudo dnf module list postgresql
sudo dnf enable postgresql:14
```
En caso de que postgresql 14 no sea un modulo disponible, podemos instalar cualquier version y luego **[reemplazarla](https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-install-postgresql-on-rhel-8.html)**:
```
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo dnf -qy module disable postgresql
sudo dnf install -y postgresql14-server
```
Para instalar **[psycopg2 compatible con postgreSQL 14](https://www.crunchydata.com/developers/download-postgres/binaries/psycopg2)**:
```
wget https://api.developers.crunchydata.com/downloads/repo/rpm-centos/postgresql14/crunchypg14.repo
wget https://api.developers.crunchydata.com/downloads/gpg/RPM-GPG-KEY-crunchydata-dev
mv RPM-GPG-KEY-crunchydata-dev /etc/pki/rpm-gpg
mv crunchypg14.repo /etc/yum.repos.d/crunchypg14.repo
dnf repolist
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
dnf -qy module disable postgresql
dnf list postgresql14
dnf install postgresql14\* python3-psycopg2\*
```
Iniciamos postgresql:
```
/usr/pgsql-14/bin/postgresql-14-setup initdb
systemctl start postgresql-14
systemctl enable postgresql-14
systemctl status postgresql-14
```
Modificamos el archivo de configuracion de postgres y reiniciamos el servicio:
```
vi /var/lib/pgsql/14/data/postgresql.conf
>>>   listen_addresses = '*'
```
Creamos la Database del sistema:
```
su postgres
psql
CREATE DATABASE dbso2;
CREATE USER so2 WITH PASSWORD '2022';
ALTER ROLE so2 SET client_encoding TO 'utf8';
ALTER ROLE so2 SET default_transaction_isolation TO 'read committed';
ALTER ROLE so2 SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dbso2 TO so2;
\q
exit
```
Descargamos mediante git:
```
cd /root
git clone https://github.com/Araujoch/HIPS.git
```
Agregamos nuestra direccion IP al archivo settings.py:
```
cd hips
vi settings.py
>>>   ALLOWED_HOSTS = [ 'your_ip' ]
```
Creamos un superuser y ejecutamos el manage.py:
```
python3 manage.py createsuperuser
python3 manage.py migrate
python3 manage.py runserver [your_ip]:80
```
(Verificar que el puerto 80 se encuentre **[abierto](https://linuxconfig.org/redhat-8-open-http-port-80-and-https-port-443-with-firewalld))

## Uso del HIPS
Una vez que el servicio Django se esta ejecutando, podemos acceder a el mediante cualquier navegador.
#### El HIPS se maneja mediante el uso de un chatbot, el cual recibe instrucciones en formato de texto, luego de autenticarte (utilizando las credenciales creadas para el superuser) verás está pantalla:
![image](https://user-images.githubusercontent.com/61550659/177173539-d232b113-7d68-4dca-9f71-3569ded43df0.png)

#### Para ejecutar la configuracion inicial, utilizamos la opcion "13"
![image](https://user-images.githubusercontent.com/61550659/177174885-f91fd777-30e0-4d9d-87d6-82131b4698ef.png)

#### Ahora podemos ejecutar la instruccion "help", para entender las funcionalidades:
![image](https://user-images.githubusercontent.com/61550659/177175695-ecb07561-9e38-489e-890b-dc195fe3a3fd.png)







