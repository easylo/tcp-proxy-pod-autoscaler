
from time import sleep
from logger_toolbox import _logger
from toolbox import _toolbox
from kubernetes_toolbox import KubernetesToolbox
from datetime import datetime, timezone, timedelta


class Scaler(object):
    _k8s: KubernetesToolbox
    _last_call_at_annotation = 'tcp-proxy-pod-autoscaler/last-call-at'
    _scale_down_at_annotation = 'tcp-proxy-pod-autoscaler/scale-down-at'

    _namespace = ""
    _deployment_name = ""
    _endpoint_name = ""
    _check_ttl: int
    _replicas = None
    _max_retry: int = 30
    _waiting_time: int = 1000
    _factor = 1  # timeout series: 1s, 2s, 3s.... 10m

    def __init__(self, args):
        _logger.debug("START")

        if "check_ttl" in args:
            self._check_ttl = args.check_ttl

        if "namespace" in args:
            self._namespace = args.namespace

        if "deployment" in args:
            self._deployment_name = args.deployment

        if "endpoint" in args:
            self._endpoint_name = args.endpoint

        if "waiting_time" in args:
            self._waiting_time = args.waiting_time

        if "max_retry" in args:
            self._max_retry = args.max_retry

        _logger.info(f"Watching namespace: {self._namespace}")
        _logger.info(f"Watching deployment: {self._deployment_name}")
        _logger.info(f"Watching endpoint: {self._endpoint_name}")
        _logger.info(f"TTL: {self._check_ttl}")
        _logger.info(
            f"Waiting time (Time in ms between 2 checks): {self._waiting_time}")
        _logger.info(f"Max retries: {self._max_retry}")

        self._k8s = KubernetesToolbox()

    def scale_down(self, _replica=0):
        _logger.debug("START")
        self.update_scale_down()
        self._k8s.update_replica_number(
            self._namespace, self._deployment_name, _replica)

    def update_scale_down(self):
        _logger.debug("START")
        return self._update_annotation_call(self._scale_down_at_annotation)

    def update_last_call(self):
        _logger.debug("START")
        return self._update_annotation_call(self._last_call_at_annotation)

    def _update_annotation_call(self, _annotation):
        _logger.debug("START")
        _now_UTC = _toolbox.get_date_now_utc()
        _updated_annotation = self._k8s.update_deployment_annotation(
            self._namespace, self._deployment_name, _annotation, _now_UTC.isoformat())
        return _updated_annotation

    def is_expired(self):
        _logger.debug("START")
        _last_call_annotation = self._k8s.get_deployment_annotation(
            self._namespace, self._deployment_name, self._last_call_at_annotation)
        _logger.debug(f"_last_call_annotation {_last_call_annotation}")

        if _last_call_annotation is not None:
            _last_call_UTC = _toolbox.get_date_utc_from_string(
                _last_call_annotation)

            _now_UTC = _toolbox.get_date_now_utc()

            if (_last_call_UTC + timedelta(seconds=self._check_ttl)) < _now_UTC:
                return True

        return False

    def get_replica_number(self):
        _logger.debug("START")
        self._replicas = self._k8s.get_replica_number(
            self._namespace, self._deployment_name)
        return self._replicas

    def make_target_available(self):
        _logger.debug("START")
        self.get_replica_number()

        _logger.debug(f"Current replica number: {self._replicas}")

        if self._replicas == 0 or self._replicas is None:
            self._k8s.update_replica_number(
                self._namespace, self._deployment_name, 1)
            # wait endpoint is available
            __waiting_time_ms = self._waiting_time
            for i in range(1, self._max_retry):
                _endpoint_status = self._k8s.check_endpoint_available(
                    self._namespace, self._endpoint_name)
                if _endpoint_status:
                    return True
                else:
                    __timer = (__waiting_time_ms/1000)
                    _logger.debug(f"Wait {__timer}s before next retry")
                    sleep(__timer)
                    __waiting_time_ms = __waiting_time_ms * self._factor
            return False
