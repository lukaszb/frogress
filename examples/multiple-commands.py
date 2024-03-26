#!/usr/bin/env python
import frogress
import time



def cmd(s=0):
    time.sleep(s)


@frogress.spinner('Doing some stuff as decorator', done="Well done")
def cmd1():
   cmd(0.5)


@frogress.spinner('Doing some stuff as decorator v2')
def cmd2():
   cmd(0.5)



def main():
    with frogress.spinner("Doing some stuff", done="OK"):
      cmd(0.5)
    with frogress.spinner("Doing more stuff for 2s", done="Finally!"):
      cmd(2)
    with frogress.spinner("Doing some stuff", title_on_done="Oh, I got replaced"):
      cmd(0.5)

    cmd1()
    cmd2()


if __name__ == '__main__':
    main()

