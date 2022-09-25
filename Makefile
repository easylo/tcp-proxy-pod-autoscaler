.PHONY: build_app
build_app:
	docker build tcp-proxy-pod-autoscaler -t tcp-proxy-pod-autoscaler

.PHONY: k_apply
k_apply:
	kubectl apply -f example --recursive

.PHONY: k_delete
k_delete:
	kubectl delete deploy frontend -n webapp
	kubectl delete deploy tcp-proxy-pod-autoscaler -n webapp
	kubectl delete deploy redis-replica -n webapp
	kubectl delete deploy redis-master -n webapp
	kubectl delete ingress webapp-ingress -n webapp

.PHONY: k_namespace
k_namespace:
	kubectl config set-context --current --namespace=webapp

.PHONY: k_ingress_logs
k_ingress_logs:
	kubectl  logs -n ingress-nginx -f ingress-nginx-controller-AAAAAAA
