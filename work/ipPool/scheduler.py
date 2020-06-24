from multiprocessing import Process
import api
import timed_check_db


def PR_1():
    timed_check_db.total()


def PR_2():
    api.app.run()


def proxypool_run():
    p1 = Process(target=PR_1)
    p2 = Process(target=PR_2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    proxypool_run()
