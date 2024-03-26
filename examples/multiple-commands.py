#!/usr/bin/env python
import frogress
import time



def cmd(s=0):
    time.sleep(s)


def main():
    with frogress.spinner("Doing some stuff", done="OK"):
      cmd(0.5)
    with frogress.spinner("Doing more stuff for 2s", done="Finally!"):
      cmd(2)
    with frogress.spinner("Doing some stuff", title_on_done="Oh, I got replaced"):
      cmd(0.5)


if __name__ == '__main__':
    main()

