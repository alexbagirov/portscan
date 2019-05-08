import argparse
import socket
import time
from functools import partial
from multiprocessing.dummy import Pool
from typing import Tuple, NoReturn


class Scanner:
    @staticmethod
    def scan() -> NoReturn:
        host, start, end = Scanner.parse_args()
        ip = socket.gethostbyname(host)

        with Pool(700) as pool:
            pool.map(partial(Scanner.scan_tcp, ip), range(start, end + 1))

        with Pool(1) as pool:
            pool.map(partial(Scanner.scan_udp, ip), range(start, end + 1))

    @staticmethod
    def parse_args() -> Tuple[str, int, int]:
        parser = argparse.ArgumentParser()
        parser.add_argument('host', type=str)
        parser.add_argument('start_port', type=int)
        parser.add_argument('end_port', type=int)

        args = parser.parse_args()
        if args.end_port < args.start_port:
            print('End port can\'t precede the start port')
            exit(0)
        if args.start_port < 0 or args.end_port > 65535:
            print('Port number must be in range of 1-65535')
            exit(0)

        return args.host, args.start_port, args.end_port

    @staticmethod
    def scan_tcp(tcp_host: str, tcp_port: int) -> NoReturn:
        s = socket.socket()
        s.settimeout(3)

        result = s.connect_ex((tcp_host, tcp_port))
        if not result:
            print('Open TCP port {}'.format(tcp_port))
        s.close()

    @staticmethod
    def scan_udp(udp_host: str, udp_port: int) -> NoReturn:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.sendto(b'test', (udp_host, udp_port))
            s.settimeout(1)
            s.recvfrom(512)
        except socket.error:
            pass
        else:
            print('Open UDP port {}'.format(udp_port))
        finally:
            s.close()
            time.sleep(1)


if __name__ == '__main__':
    Scanner().scan()
