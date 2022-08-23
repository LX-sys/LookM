# -*- coding:utf-8 -*-
# @time:2022/5/916:50
# @author:LX
# @file:ssh_reset_machine.py
# @software:PyCharm
'''


'''
import paramiko

def _machine(mode="state",number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc"):
    '''
            指定编号的机器
        :param number: 机器编号
        :return:
        '''
    cmd = {
        "reset":"vim-cmd vmsvc/power.reset $(vim-cmd vmsvc/getallvms | awk '$2==<@> {print $1}')",
        "off":"vim-cmd vmsvc/power.off $(vim-cmd vmsvc/getallvms | awk '$2==<@> {print $1}')",
        "on": "vim-cmd vmsvc/power.on $(vim-cmd vmsvc/getallvms | awk '$2==<@> {print $1}')",
        "state": "vim-cmd vmsvc/power.getstate $(vim-cmd vmsvc/getallvms | awk '$2==<@> {print $1}')",
        "ssl":"vim-cmd vmsvc/getallvms"
    }
    data = "MVware远程连接错误"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password,timeout=7)
        if mode == "ssl":
            cmd_shutdown = cmd[mode]
        else:
            cmd_shutdown = cmd[mode].replace("<@>",number)
        stdin, stdout, stderr = ssh.exec_command(cmd_shutdown)
        data = stdout.read()
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        ssh.close()
        print("执行命令成功")
    except (Exception,EOFError):
        pass
    return data


# 重启指定编号的机器
def reset_machine(number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc")->None:
    _machine("reset",number,hostname,port,username,password)

# 关闭指定编号的机器
def off_machine(number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc")->None:
    _machine("off",number,hostname,port,username,password)


# 打开指定编号的机器
def on_machine(number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc")->None:
    _machine("off",number,hostname,port,username,password)

# 检查的机器的状态
def state_machine(number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc")->bool:
    '''
        检查机器的运行状态 (开或关闭)
    '''
    data=_machine("state",number,hostname,port,username,password)
    if "Powered on" in data.decode("utf8"):
        return True
    return False

# 检测ssl是否打开
def is_ssl_machine(number="", hostname="", port=22, username="dingzj", password="VYVQ2HsWeVraH0Za7Yxc")->bool:
    '''
        检查机器的运行状态 (开或关闭)
    '''
    try:
        _machine("state",number,hostname,port,username,password)
        return True
    except Exception as e:
        return False

