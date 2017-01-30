import lluv.lluv_tui as lt
import lluv.lluv_cli as lc
import lluv.lluv_simple_cli as lsc
import lluv.lluvconsole as lconsole


def tui():
    lt.start()


def cli():
    lc.start()


def simple_cli():
    lsc.start()


def console():
    lconsole.start()
