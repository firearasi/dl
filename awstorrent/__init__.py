#!/usr/bin/python

import time 
import subprocess
import pyperclip


# create tmp dir on aws
def download(aws,torrent,title,output_dir,keep_in_aws=False):
    subprocess.run(['chmod','400','icearasi.pem'])
    tmpdir="tmpdir%s"%int(time.time()) if title is None else title
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
            '-r',remote_files_tmp,output_dir])
    else:
        print("Download failed!")

    if not keep_in_aws:
        subprocess.run(['ssh',aws,'rm',tmpdir,'-rf'])
  




