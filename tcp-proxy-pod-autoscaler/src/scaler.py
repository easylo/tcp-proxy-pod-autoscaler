
from time import sleep
from logger_toolbox import _logger
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

    def __init__(self, args):

        if "check_ttl" in args:
            self._check_ttl = args.check_ttl

        if "namespace" in args:
            self._namespace = args.namespace

        if "deployment" in args:
            self._deployment_name = args.deployment

        if "endpoint" in args:
            self._endpoint_name = args.endpoint

        self._k8s = KubernetesToolbox()

    def scale_down(self, _replica=0):
        self.update_scale_down()
        self._k8s.update_replica_number(
            self._namespace, self._deployment_name, _replica)

    def update_scale_down(self):
        return self._update_annotation_call(self._scale_down_at_annotation)

    def update_last_call(self):
        return self._update_annotation_call(self._last_call_at_annotation)

    def _update_annotation_call(self, _annotation):
        _now_UTC = datetime.now(timezone.utc)
        _updated_annotation = self._k8s.update_deployment_annotation(
            self._namespace, self._deployment_name, _annotation, _now_UTC.isoformat())
        return _updated_annotation

    def is_expired(self):
        _last_call_annotation = self._k8s.get_deployment_annotation(
            self._namespace, self._deployment_name, self._last_call_at_annotation)
        _logger.debug(
            f"is_expired::_last_call_annotation {_last_call_annotation}")
        if _last_call_annotation is not None:
            _last_call_UTC = datetime.fromisoformat(_last_call_annotation)

            _now_UTC = datetime.now(timezone.utc)

            if (_last_call_UTC + timedelta(seconds=self._check_ttl)) < _now_UTC:
                return True

        return False

    def get_replica_number(self):
        self._replicas = self._k8s.get_replica_number(
            self._namespace, self._deployment_name)
        return self._replicas

    def make_target_available(self):
        self.get_replica_number()

        _logger.debug(f"get_replica_number: {self._replicas}")

        if self._replicas == 0 or self._replicas is None:
            self._k8s.update_replica_number(
                self._namespace, self._deployment_name, 1)
            # wait endpoint is available
            for i in range(1, 10):
                _endpoint_status = self._k8s.check_endpoint_available(
                    self._namespace, self._endpoint_name)
                if _endpoint_status:
                    return True
                else:
                    sleep(1)
            return False
