import os
import subprocess
import threading
import soundcloud
import time

import sys

import g


class PlayWithMpv(threading.Thread):
    def __init__(self, cmd):
        self.stdout = None
        self.stderr = None
        self.cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        g.p = subprocess.Popen(cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

        self.stdout, self.stderr = g.p.communicate()

    def stop(self):
        self.p.kill()


class TerminalColors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def fmt_time(seconds):
    """ Format number of seconds to %H:%M:%S. """
    hms = time.strftime('%H:%M:%S', time.gmtime(int(seconds)))
    H, M, S = hms.split(":")

    if H == "00":
        hms = M + ":" + S

    elif H == "01" and int(M) < 40:
        hms = str(int(M) + 60) + ":" + S

    elif H.startswith("0"):
        hms = ":".join([H[1], M, S])

    return hms


with open(os.path.join(g.__location__, '.secret')) as f:
    cid = f.readline().strip()
    cs = f.readline().strip()
    f.close()

client = soundcloud.Client(
    client_id=cid,
    client_secret=cs
)

while True:
    if not g.isPlaying:
        command = input(TerminalColors.BOLD + "\n> " + TerminalColors.ENDC)
        if command:
            if g.tracks and represents_int(command):
                try:
                    track = g.tracks[int(command) - 1]
                    track_url = track.permalink_url
                    track_pic = track.artwork_url
                    track_title = track.title
                    cmd = which('mpv')
                    cmd += ' ' + track_url
                    g.playWithMpv = PlayWithMpv(cmd)
                    g.playWithMpv.start()
                    print(TerminalColors.BOLD + '"' + track_title + '"' + TerminalColors.ENDC + ' playing...')
                    g.isPlaying = True

                except IndexError:
                    print ('Please enter a valid number')

            elif command[0] == '/' and len(command) > 1:
                g.tracks = client.get('/tracks', q=command[1:], limit=g.page_size)
                for i in range(0, len(g.tracks) - 1):
                    formattedOrderNum = str(i + 1)
                    if len(formattedOrderNum) == 1:
                        formattedOrderNum = '0' + formattedOrderNum
                    print (
                    TerminalColors.OKBLUE + formattedOrderNum + TerminalColors.ENDC + TerminalColors.OKGREEN + ' ' + \
                    g.tracks[i].title + TerminalColors.ENDC)

            elif command == 'quit' or command == 'exit':
                break
            else:
                print ('Command not accepted')

    else:
        if g.p:
            if g.p.poll() is None:
                if not g.elapsed_time:
                    g.elapsed_time = 0

                g.elapsed_time += 1
                print(fmt_time(g.elapsed_time), end="\r")
                sys.stdout.flush()
                time.sleep(1)
            else:
                g.elapsed_time = None
                g.isPlaying = False

