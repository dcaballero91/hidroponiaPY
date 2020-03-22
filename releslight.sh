#!/bin/bash
#Se activan o desactivan los reles
#Conexion a base de datos
while true
do
MASTER_DB_USER='slave'
MASTER_DB_PASSWD='sup3rPw#'
MASTER_DB_PORT=23306
MASTER_DB_HOST='5.189.148.10'
MASTER_DB_NAME='hidroponia'
#Prepare sql query

SQL_Query='select estado from Rele where id_sensor=8'

light=$(mysql -u$MASTER_DB_USER -p$MASTER_DB_PASSWD -P$MASTER_DB_PORT -h$MASTER_DB_HOST -D$MASTER_DB_NAME --ssl-ca=/etc/certs/ca.pem --ssl-cert=/etc/certs/client-cert.pem --ssl-key=/etc/certs/client-key2.pem<<EOF) 
$SQL_Query
EOF
limite="D"
echo $light | awk '{print$2}' >/opt/estadolight
while IFS= read -r line
do
  echo " $line"
  if [ "$limite" = "$line" ]; then
    echo "Desactivando....."
    	#Desactivar fan
	curl -d '{"mod":"light","est":"D"}' -H 'Content-Type: application/json' http://localhost:5000/setrest04
else
    echo "Activando"
    	#Activar fan
	curl -d '{"mod":"light","est":"P"}' -H 'Content-Type: application/json' http://localhost:5000/setrest06
fi
done < /opt/estadolight

sleep 30
done
