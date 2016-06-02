#!/usr/bin/python

import time 
import subprocess
import argparse
import pyperclip

# Address of my amazon-web-service downloading server 
aws="firearasi@52.53.224.102"

# use transmission [torrent file address]
parser=argparse.ArgumentParser(prog="My torrent downloader \
    through aws",prefix_chars='-')
parser.add_argument('torrent', help='torrent address',nargs='?',
    default=pyperclip.paste())
parser.add_argument('-o','--output_dir', default='.',
    help='set local destination dir')
parser.add_argument('-t','--title', help='directory title')
parser.add_argument('-k','--keep_in_aws',
    action='store_true',help='keep file in aws server')
args=parser.parse_args()

#parse torrent file name

torrent=args.torrent
index=torrent.find('.torrent')+8
torrent=torrent[0:index]

# create tmp dir on aws

tmpdir="tmpdir%s"%int(time.time()) if args.title is None else args.title

# download with transmission-cli 
transmission_cmd=["transmission-cli","-D","-f",
    "/home/firearasi/killtransmission","-w",tmpdir,torrent]
ssh_cmd=['ssh','-i','icearasi.pem',aws]+transmission_cmd
print("ssh_cmd: ",ssh_cmd)
ret_code=subprocess.run(ssh_cmd).returncode

# Copy downloaded dir to local dir
print("Return code:",ret_code)

if ret_code==255:
    print("AWS bt download succeeded...")
    print("Copying to local dir:",args.output_dir)
  
    #Get subdirectory of the tmpdir
    remote_files_tmp=aws+':'+tmpdir
    remote_files=aws+':'+tmpdir+'/\*'
    subprocess.run(['scp','-i','icearasi.pem',
        '-r',remote_files_tmp,args.output_dir])
else:
    print("Download failed!")

if not args.keep_in_aws:
    subprocess.run(['ssh',aws,'rm',tmpdir,'-rf'])
  







