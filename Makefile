
run-local-rabbit:
	-docker rm -f local-rabbit 2>/dev/null
	docker run -d --rm --hostname=local-rabbit --name=local-rabbit -v $(PWD)/_local/rabbit:/var/lib/rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq:3-management

