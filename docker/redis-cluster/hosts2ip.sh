# Usar nombres sin espacios
hostnames="redis_db
redis_cluster2
redis_cluster3
redis_cluster4
redis_cluster5
redis_cluster6"

IPs=""

while read name; do
	IP=$(getent hosts $name | awk '{print $1}')
	if [[ -n "$IPs" ]]; then
		IPs="$IPs ${IP}:6379"
	else
		IPs="${IP}:6379"
	fi
done <<< "$hostnames"

echo "$IPs"
