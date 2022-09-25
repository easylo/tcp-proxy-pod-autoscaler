import time
# from pprint import pprint
import argparse
# from kubernetes.client.rest import ApiException
# import kubernetes.client
# from kubernetes import client, config, watch
# from kubernetes import client, config

from logger_toolbox import _logger
from proxy import Proxy
from watcher import Watcher
from scaler import Scaler
# import threading

# _scaler: Scaler


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--namespace", help="", required=True)
    parser.add_argument("--deployment", help="", required=True)
    parser.add_argument("--endpoint", help="", required=True)

    parser.add_argument("--local-address",   help="Verbosity",
                        default='',  required=False)
    parser.add_argument("--local-port", help="Verbosity",
                        type=int, default=80, required=False)

    parser.add_argument("--target-address", help="the SVC",
                        dest="remote_address", required=True)
    parser.add_argument("--target-port", help="Verbosity",
                        dest="remote_port", type=int, default=80, required=False)

    parser.add_argument("--check-interval", help="Verbosity",
                        dest="check_interval", type=int, default=30, required=False)
    parser.add_argument("--ttl", help="idle duration before scaling to zero (in seconds)",
                        dest="check_ttl", type=int, default=1800, required=False)

    _args = parser.parse_args()

    return _args


def check_scale_down(_args, _scaler: Scaler):
    _logger.info("check_scale_down")
    _ttl = _args.check_ttl
    is_expired = _scaler.is_expired()
    _logger.debug(f"is_expired: {is_expired}")
    if is_expired:
        _replica = _scaler.get_replica_number()
        if _replica > 0:
            _scaler.scale_down()
    # get object scaler
    # get number of replica
    # if replica > 0
    # get anotation value last request
    # compare to _ttl
    # if more than TTL update replica to 0


def main():
    _args = parse_args()
    _logger.debug(f"{_args =}")
    try:
        _scaler = Scaler(_args)
        _watcher = Watcher(_args.check_interval,
                           check_scale_down, _args, _scaler)
        _proxy = Proxy(_args)
        _proxy.set_scaler(_scaler)
        _proxy.run()
    finally:
        _logger.info("STOP WATCHER")
        _watcher.stop()


if __name__ == "__main__":
    main()
