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

SQL_Query='select estado from Rele where id_sensor=9'

motor=$(mysql -u$MASTER_DB_USER -p$MASTER_DB_PASSWD -P$MASTER_DB_PORT -h$MASTER_DB_HOST -D$MASTER_DB_NAME --ssl-ca=/etc/certs/ca.pem --ssl-cert=/etc/certs/client-cert.pem --ssl-key=/etc/certs/client-key2.pem<<EOF) 
$SQL_Query
EOF
limite="D"
echo $motor | awk '{print$2}' >/opt/estadomotor
while IFS= read -r line
do
  echo " $line"
  if [ "$limite" = "$line" ]; then
    echo "Desactivando....."
    	#Desactivar fan
	curl -d '{"mod":"motor","est":"D"}' -H 'Content-Type: application/json' http://localhost:5000/setrest04
else
    echo "Activando"
    	#Activar fan
	curl -d '{"mod":"motor","est":"P"}' -H 'Content-Type: application/json' http://localhost:5000/setrest06
fi
done < /opt/estadomotor

sleep 30
done
