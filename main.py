from blocker import SiteBlocker, ProcessBlocker
from monitor import Monitor

monitor_interval = 10
block_interval = 1


def main():
    while True:
        is_complete = Monitor.check()

        if is_complete:
            ProcessBlocker.free()
            SiteBlocker.free()
            Monitor.sleep_until(hour=8)

        else:
            for _ in range(monitor_interval // block_interval):
                ProcessBlocker.block()
                SiteBlocker.block()
                Monitor.sleep(block_interval)
            Monitor.sleep(monitor_interval % block_interval)


if '__main__' == __name__:
    main()
