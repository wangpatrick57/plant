#!/pkg/python/3.7.4/bin/python3
import subprocess

def run_cmd(cmd_str):
    proc = subprocess.Popen(cmd_str.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err
