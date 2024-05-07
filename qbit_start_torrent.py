import os
import time
import sys


def main():
    if len(sys.argv) >= 2:
        filepath = fr"{sys.path[0]}/timepoint/{sys.argv[1]}"
        if not os.access(filepath, os.F_OK):
            print("no")
            writetime(filepath, time.localtime())
    else:
        print("no torrent name")


def writetime(filepath, timenow):
    file = open(filepath, mode="w+")
    file.write(f"{timenow.tm_sec},"
               f"{timenow.tm_min},"
               f"{timenow.tm_hour},"
               f"{timenow.tm_yday},"
               f"{timenow.tm_year}")
    print(f"torrent start at {time.asctime(time.localtime(time.time()))}")
    file.close()


if __name__ == '__main__':
    main()
