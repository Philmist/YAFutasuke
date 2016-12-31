#!/usr/bin/python3
# vim: fileencoding=utf-8
"""オリジナル双助のIPアドレス暗号化モジュール移植です。"""

import hashlib
import base64
import socket
import binascii
import ipaddress


def get_swap_list(seed, count):
    """MD5 Base Randomizer"""
    ret = []
    seed = seed.encode("utf-8")
    while 1:
        md5obj = hashlib.md5(seed)
        md5obj.update(seed)
        seed = md5obj.digest()
        for i in range(8):
            ret.append((seed[i], seed[i + 8]))
            count -= 1
            if count == 0:
                return ret


def crypt_md5swap(plain_str, is_enc=0):
    """is_enc=1 encryption; is_enc=0 decryption"""
    s = list(plain_str)
    plain_str_len = len(plain_str)
    weight = 0
    for c in plain_str:
        weight += ord(c) + 1
    chgl = get_swap_list(str(weight), plain_str_len * 11)
    if is_enc:
        chgl.reverse()
    for m1, m2 in chgl:
        if is_enc:
            m2, m1 = m1, m2
        m1 %= plain_str_len
        m2 %= plain_str_len
        s[m1], s[m2] = s[m2], s[m1]
    return "".join(s)


def crypt_md5swap2(plain_str, is_enc=0, pw=""):
    """is_enc=1 encryption; is_enc=0 decryption"""
    s = list(plain_str)
    plain_str_len = len(plain_str)
    weight = 0
    for c in plain_str:
        weight += ord(c) + 1
    chgl = get_swap_list(str(weight) + pw, plain_str_len * 11)
    if is_enc:
        chgl.reverse()
    for m1, m2 in chgl:
        if is_enc:
            m2, m1 = m1, m2
        m1 %= plain_str_len
        m2 %= plain_str_len
        s[m1], s[m2] = s[m2], s[m1]
    return "".join(s)


def base64flatencode(s):
    ret = base64.encodestring(s)
    ret = ret.replace('\n', '')
    return ret


def pack_ippt(ip, port):
    nip = socket.inet_aton(ip)
    aip = binascii.hexlify(nip)
    return "%s%04x" % (aip, port)


def unpack_ippt(ippt):
    aip = ippt[:8]
    port = int(ippt[8:], 16)
    nip = binascii.unhexlify(aip)
    ip = socket.inet_ntoa(nip)
    return (ip, port)


def parse_disp_p2pnode(node):
    node = node[1:-1]
    node = node.split(":", 1)
    ver = node[0][5:]
    pplain_str = crypt_md5swap(node[1], 0)
    return ver, unpack_ippt(pplain_str)


def sprintf_disp_p2pnode(prxsver, ip, port):
    ippt = pack_ippt(ip, port)
    cippt = crypt_md5swap(ippt, 1)
    return "=%s:%s=" % (prxsver, cippt)


def get_my_ip():
    ip = socket.gethostbyname(socket.gethostname())
    addr_obj = ipaddress.ip_address(ip)
    return ip if addr_obj.is_global else ""


def iptoint(ip):
    ipaddr = ipaddress.ip_address(ip)
    return int(ipaddr)


def reverse_fqdn(fqdn):
    revfqdns = fqdn.split(".")
    revfqdns.reverse()
    revfqdn = ".".join(revfqdns)
    return revfqdn


def masking(fqdnip):
    _fqdnip = fqdnip.split('.')
    _fqdnip[-1] = '*'
    return '.'.join(_fqdnip)
