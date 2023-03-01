from blocker import SiteBlocker, ProcessBlocker
from monitor import Monitor

monitor_interval = 10
process_block_interval = 1


def main():
    while True:
        is_complete = Monitor.check()

        if is_complete:
            ProcessBlocker.free()
            SiteBlocker.free()
            Monitor.sleep_until(hour=8)

        else:
            SiteBlocker.block()
            Monitor.sleep(monitor_interval % process_block_interval)
            for _ in range(monitor_interval // process_block_interval):
                ProcessBlocker.block()
                Monitor.sleep(process_block_interval)


if '__main__' == __name__:
    main()
