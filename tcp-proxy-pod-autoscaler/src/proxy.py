import socket
import socks
import threading
import select
import sys

from logger_toolbox import _logger
from scaler import Scaler


class Proxy(object):
    local_address = ''
    local_port = 9000
    remote_address = "-svc"
    remote_port = 80
    lsock = []
    msg_queue = {}
    _scaler: Scaler

    def __init__(self, args):

        if "local_address" in args:
            self.local_address = args.local_address

        if "local_port" in args:
            self.local_port = args.local_port

        if "remote_address" in args:
            self.remote_address = args.remote_address

        if "remote_port" in args:
            self.remote_port = args.remote_port

        # super(ClassName, self).__init__(*args))

    def set_scaler(self, _scaler: Scaler):
        self._scaler = _scaler

    def run(self):
        _logger.debug("START RUN")
        return self.tcp_server()

    def tcp_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setblocking(0)
            sock.bind((self.local_address, int(self.local_port)))
            sock.listen(3)
            self.lsock.append(sock)

            _logger.info(
                f'[*] Listening on {self.local_address} {self.local_port}')

            while True:
                readable, writable, exceptional = select.select(
                    self.lsock, [], [])
                for s in readable:
                    if s == sock:
                        self.hit_request()
                        rserver = self.remote_conn()
                        if rserver:
                            client, addr = sock.accept()
                            _logger.info('Accepted connection {0} {1}'.format(
                                addr[0], addr[1]))
                            self.store_sock(client, addr, rserver)
                            break
                        else:
                            _logger.info('the connection with the remote server can\'t be \
                            established')
                            _logger.info(
                                'Connection with {} is closed'.format(addr[0]))
                            client.close()
                    data = self.received_from(s, 3)
                    self.msg_queue[s].send(data)
                    if len(data) == 0:
                        self.close_sock(s)
                        break
                    else:
                        _logger.info(
                            'Received {} bytes from client '.format(len(data)))
                        # here if we want to update reponse
        except KeyboardInterrupt:
            _logger.info('Ending server')
        except:
            _logger.error('Failed to listen on {}:{}'.format(
                self.local_address, self.local_port))
            # sys.exit(0)
            return 1
        finally:
            # sys.exit(0)
            return 1

    def remote_conn(self):
        _logger.debug("remote_conn")
        try:
            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((self.remote_address, int(self.remote_port)))
            return remote_sock
        except Exception as e:
            _logger.error(e)
            return False

    def store_sock(self, client, addr, rserver):
        self.lsock.append(client)
        self.lsock.append(rserver)

        try:
            self.msg_queue[client] = rserver
            self.msg_queue[rserver] = client
        except Exception as e:
            _logger.error(e)

    def received_from(self, sock, timeout):
        data = ""
        sock.settimeout(timeout)
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                data = + data
        except:
            pass
        return data

    def close_sock(self, sock):
        _logger.info(
            'End of connection with {}'.format(sock.getpeername()))
        self.lsock.remove(self.msg_queue[sock])
        self.lsock.remove(self.msg_queue[self.msg_queue[sock]])
        serv = self.msg_queue[sock]
        self.msg_queue[serv].close()
        self.msg_queue[sock].close()
        del self.msg_queue[sock]
        del self.msg_queue[serv]

    def hit_request(self, data='', length=16):
        _logger.info(f"HIT REQUEST")
        try:
            self._scaler.update_last_call()
            self._scaler.make_target_available()
        except Exception as e:
            _logger.error(e)

        # get object scaler
        # check endpoint/replica is available
        # if not update replica to 1
        # update anonation with time
        pass
