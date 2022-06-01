from concurrent.futures.process import _system_limits_checked
import os

dir = "./instances/"
for root, dirs, files in os.walk(dir):
    for name in files:
        # linux系统
        # command = "sed -i  '1,8d' {}{}".format(dir, name)
        # mac系统
        command = "sed -i '' '1,8d' {}{}".format(dir, name)
        os.system(command)
