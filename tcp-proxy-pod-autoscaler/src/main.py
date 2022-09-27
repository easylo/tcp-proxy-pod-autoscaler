import argparse

from logger_toolbox import _logger
from proxy import Proxy
from watcher import Watcher
from scaler import Scaler


def parse_args():
    _logger.debug("START")

    parser = argparse.ArgumentParser()

    parser.add_argument("--namespace", help="", required=True)
    parser.add_argument(
        "--deployment", help="Name of Deployment to scale", required=True)
    parser.add_argument(
        "--endpoint", help="Name of Endpoints to watch for ready addresses", required=True)

    parser.add_argument("--local-address",   help="Proxy listen address",
                        default='',  required=False)
    parser.add_argument("--local-port", help="Proxy listen port",
                        type=int, default=80, required=False)

    parser.add_argument("--target-address", help="target address to which requests should be proxied (typically the Service name)",
                        dest="remote_address", required=True)
    parser.add_argument("--target-port", help="Target listen port",
                        dest="remote_port", type=int, default=80, required=False)

    parser.add_argument("--check-interval", help="Time between two checks",
                        dest="check_interval", type=int, default=60, required=False)
    parser.add_argument("--ttl", help="Idle duration before scaling to zero (in seconds)",
                        dest="ttl", type=int, required=False)
    parser.add_argument("--log-level", help="Set log level(DEBUG, INFO, WARNING, ERROR, CRITICAL)",
                        default="INFO", required=False)
    parser.add_argument("--max-retry", help="Number of attempts to wait for the endpoint to be available",
                        type=int, required=False)

    _args = parser.parse_args()

    return _args


def check_scale_down(_args, _scaler: Scaler):
    _logger.debug("START")
    is_expired = _scaler.is_expired()
    _logger.debug(f"is_expired: {is_expired}")
    if is_expired:
        _replica = _scaler.get_replica_number()
        if _replica > 0:
            _scaler.scale_down()


def main():
    _args = parse_args()
    _logger.set_level(_args.log_level)
    _logger.debug("START")
    _logger.debug(f"{_args =}")

    try:
        _scaler = Scaler(_args)
        _watcher = Watcher(_args.check_interval, check_scale_down, _args, _scaler)
        _proxy = Proxy(_args)
        _proxy.set_scaler(_scaler)
        _proxy.run()
    finally:
        _logger.info("STOP WATCHER")
        _watcher.stop()


if __name__ == "__main__":
    main()
