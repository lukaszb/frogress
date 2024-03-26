#!/usr/bin/env python
import frogress
import time

def cmd(s=0):
    time.sleep(s)


def main():
    with frogress.spinner("Waiting for response 1", done="OK"):
        cmd(0.5)
    with frogress.spinner("Waiting for response 2", done="Done"):
        cmd(0.5)
    with frogress.spinner("Waiting for response 3", done="All done, really!"):
        cmd(0.5)

if __name__ == '__main__':
    main()

