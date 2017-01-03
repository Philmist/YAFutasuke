#!/usr/bin/python3

from futap2psv import ip_encrypt

import configparser

from logging import getLogger, DEBUG

logger = getLogger(__name__)
logger.setLevel(DEBUG)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(r"config.ini")
    initial_ip = ip_encrypt.parse_disp_p2pnode(config["P2P"]["InitialNode"])[1]
    inbound_ipport = config["P2P"]["InboundPort"]
    inbound_ipaddr = config["P2P"]["InboundAddress"]
