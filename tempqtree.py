  
#! /usr/bin/env python3

"""
ONTAP REST API Sample Scripts
This script was developed by NetApp to help demonstrate NetApp
technologies.  This script is not officially supported as a
standard NetApp product.
Purpose: Script to list volumes using ONTAP REST API.
Usage: list_volumes.py [-h] -c CLUSTER -vs SVM_NAME [-u API_USER]
                       [-p API_PASS]
Copyright (c) 2020 NetApp, Inc. All Rights Reserved.
Licensed under the BSD 3-Clause “New” or Revised” License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
"""
import math
import base64
import argparse
from getpass import getpass
import logging
import texttable as tt
import requests
import urllib3 as ur
ur.disable_warnings()


def get_volumes(cluster: str, svm_name: str, headers_inc: str):
    """Get Volumes"""
    url = "https://{}/api/storage/volumes/?svm.name={}".format(cluster, svm_name)
    response = requests.get(url, headers=headers_inc, verify=False)
    return response.json()


def disp_vol(cluster: str, svm_name: str, headers_inc: str):
    """Display Volumes"""
    ctr = 0
    tmp = dict(get_volumes(cluster, svm_name, headers_inc))
    vols = tmp['records']
    tab = tt.Texttable()
    header = (['Volume name', 'Qtree'])
    tab.header(header)
    tab.set_cols_width([18,50])
    tab.set_cols_align(['c','c'])
    for volumelist in vols:
        nfl=dict(volumelist)
        #print (nfl)
        ven=nfl['name']
        print (ven)
    vid="https://{}/api/storage/volumes?name={}".format(cluster,ven)
    response = requests.get(vid, headers=headers_inc, verify=False)
    volt = response.json()
    vol1=dict(volt)
    voltemp=vol1['records']
    voltemp2=dict(voltemp)
    vuid=voltemp2['uuid']
    print(vuid)
    qr="https://{}/api/storage/qtrees/?id=!0".format(cluster)
    response = requests.get(qr, headers=headers_inc, verify=False)
    qres = response.json()
    qres2=dict(qres)
    qres3=qres2['records']
    for i in qres3:
        q2=dict(i)
        qtname=q2['name']
    nc="https://{}/api/storage/qtrees/?svm.name={}&volume.name={}".format(cluster,svm_name,ven)
    response = requests.get(nc, headers=headers_inc, verify=False)
    vuid12 = response.json()
    conn=dict(vuid12)
    conn1=conn['records']
    #for Volume UUID:-
    for k in conn1:
        connr=dict(k)
        convl=connr['volume']
        vuid=convl['uuid']
        print("volume UUID",vuid)
        print("qtree name", qtname)
        qind="https://{}/api/storage/quota/reports?qtree={}&volume.uuid={}".format(cluster,qtname,vuid)
        print("Qind",qind)
        qindres = requests.get(qind, headers=headers_inc, verify=False)
        qindtemp = response.json()
        print("qtindtem",qindtemp)
        qindtemp1=dict(qindtemp)
        qindtemp2=qindtemp1['records']
        #Qkid contains qtee index
        for q in qindtemp2:
            id=dict(q)
            print("variable",id)
            Qid=id['index']
            print("Qid")
    qid="https://{}/api/storage/quota/reports?qtree={}&volume.uuid={}".format(cluster,qtname,vuid)
    response = requests.get(qid, headers=headers_inc, verify=False)#print (qres3)
    qjason = response.json()#q2 contains qtree name
    pring("qjason",qjason)
    qti=dict(qjason)
    print("Qti Valuue", qti)
    qtr=qti['records']   
    qrep="https://{}/api/storage/qtrees/?svm.name={}&volume.name={}".format(cluster,svm_name,ven)
    response = requests.get(qrep, headers=headers_inc, verify=False)
    quorep = response.json()
    quotemp=dict(quorep)
    print(quotemp)
    conn11=quotemp['records']
    print("Sai" ,conn11)
    q1=dict(i)
    q2=q1['name']
    q3=q1['volume']
    q4=dict(q3)
    q5=q4['name']
    #print(q2)
    vid="https://{}/api/storage/volumes?name={}".format(cluster,q5)
    response = requests.get(vid, headers=headers_inc, verify=False)
    vol = response.json()
    vol1=dict(vol)
    vol3=vol1['records']
    #vol2 contains vol uuid.
    tab.set_cols_align(['c','c'])
    
        
    setdisplay = tab.draw()
    print(setdisplay)


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will list volumes in a SVM")
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details")
    parser.add_argument(
        "-vs", "--svm_name", required=True, help="SVM Name"
    )
    parser.add_argument(
        "-u",
        "--api_user",
        default="admin",
        help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )
    ARGS = parse_args()
    BASE_64_STRING = base64.encodebytes(
        ('%s:%s' %
         (ARGS.api_user, ARGS.api_pass)).encode()).decode().replace('\n', '')

    headers = {
        'authorization': "Basic %s" % BASE_64_STRING,
        'content-type': "application/json",
        'accept': "application/json"
    }

    disp_vol(ARGS.cluster, ARGS.svm_name, headers)
