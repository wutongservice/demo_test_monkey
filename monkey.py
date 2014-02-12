import subprocess
import re
import signal
from time import time

def list3rdPartyPackages():
    proc = subprocess.Popen(['adb', 'shell', 'pm', 'list', 'packages', '-3'], stdout=subprocess.PIPE)
    out = proc.communicate()[0].decode('utf-8')
    packages = []
    for line in out.splitlines():
        m = re.match(r"^package:(\w+(?:\.\w+)*)", line)
        if m:
            packages.append(m.group(1))
    return packages

proc = None
def handler(signum, frame):
    print("Handle SINGTERM...")
    global proc
    if proc is not None:
        proc.kill()


def main():
    global proc
    signal.signal(signal.SIGTERM, handler)
    for package in list3rdPartyPackages():
        print("Monkey test package %s" % package)
        proc = subprocess.Popen(['adb', 'shell', 'monkey', '-p', package, '--throttle', '200', '-s', '%d' % int(time()), '10000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode != 0:
            exit(-1)
        proc = None


if __name__ == '__main__':
    main()
