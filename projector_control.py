#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from serial import Serial, SerialException
except ImportError:
    print("错误：请先安装 pyserial 库")
    print("安装命令：pip install pyserial")
    sys.exit(1)

import sys
import argparse

# 投影仪指令映射表
COMMANDS = {
    'power_on': '开机',
    'power_off': '关机',
    'flip': 'A图像翻转',
    'brightness_up': 'B增加亮度',
    'brightness_down': 'C减少亮度',
    'contrast_up': 'D对比度加',
    'contrast_down': 'E对比度减',
    'sharpness_up': 'F增加锐度',
    'sharpness_down': 'G减少锐度',
    'hue_up': 'H色度增加',
    'hue_down': 'I色度减少',
    'saturation_up': 'J饱和度加',
    'saturation_down': 'K饱和度减',
    'keystone_vertical_up': 'L梯形上下加',
    'keystone_vertical_down': 'M梯形上下减',
    'keystone_horizontal_up': 'N梯形左右加',
    'keystone_horizontal_down': 'O梯形左右减',
    'light_axis_confirm': 'P光轴调整/确认',
    'light_axis_positive': 'Q光轴正向调整',
    'light_axis_negative': 'R光轴负向调整',
    'phase_exit': 'S相位校正/退出',
    'phase_positive': 'T相位正向校正',
    'phase_negative': 'U相位负向校正'
}

def send_command(port, command):
    """
    发送命令到投影仪
    
    Args:
        port: 串口对象
        command: 命令字符串
    """
    try:
        # 将命令转换为GBK编码
        command_bytes = command.encode('gbk')
        # 添加结束符 0D 0A
        command_bytes += b'\x0D\x0A'
        # 发送命令
        port.write(command_bytes)
        print(f"已发送命令: {command}")
    except Exception as e:
        print(f"发送命令时出错: {str(e)}")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='投影仪控制程序')
    parser.add_argument('command', choices=COMMANDS.keys(), help='要执行的命令')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='串口设备路径 (默认: /dev/ttyUSB0)')
    parser.add_argument('--baudrate', type=int, default=115200, help='串口波特率 (默认: 115200)')
    
    args = parser.parse_args()
    
    try:
        # 打开串口
        with Serial(args.port, args.baudrate, timeout=1) as ser:
            # 获取对应的命令字符串
            command_str = COMMANDS[args.command]
            # 发送命令
            send_command(ser, command_str)
    except SerialException as e:
        print(f"串口错误: {str(e)}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == '__main__':
    main() 