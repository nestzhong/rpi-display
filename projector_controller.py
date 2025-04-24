#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from serial import Serial, SerialException
from PyQt6.QtCore import QTimer

class ProjectorController:
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

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.last_update_time = 0
        self.power_off_timer = QTimer()
        self.power_off_timer.timeout.connect(self.check_and_power_off)
        self.power_off_timer.start(1000)  # 每秒检查一次
        
        # 检查串口设备是否存在
        if not os.path.exists(self.port):
            print(f"错误：串口设备 {self.port} 不存在")
            return
            
        # 检查串口权限
        try:
            mode = os.stat(self.port).st_mode
            if not mode & 0o666:  # 检查读写权限
                print(f"警告：串口设备 {self.port} 权限不足")
                print("请执行以下命令添加权限：")
                print(f"sudo chmod 666 {self.port}")
                print("或添加用户到 dialout 组：")
                print("sudo usermod -a -G dialout $USER")
        except Exception as e:
            print(f"检查串口权限时出错: {str(e)}")
        
    def connect(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
            self.serial = Serial(self.port, self.baudrate, timeout=1)
            print(f"成功连接到投影仪串口: {self.port}")
            return True
        except SerialException as e:
            print(f"连接投影仪串口失败: {str(e)}")
            print("可能的原因：")
            print("1. 串口设备不存在")
            print("2. 串口被其他程序占用")
            print("3. 串口权限不足")
            print("4. 串口设备未正确连接")
            return False
            
    def send_command(self, command):
        if not self.serial or not self.serial.is_open:
            if not self.connect():
                return False
        try:
            # 确保串口是打开的
            if not self.serial.is_open:
                self.serial.open()
                
            # 清空串口缓冲区
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            
            command_bytes = command.encode('gbk')
            command_bytes += b'\x0D\x0A'
            self.serial.write(command_bytes)
            print(f"已发送投影仪命令: {command}")
            return True
        except SerialException as e:
            print(f"发送投影仪命令失败: {str(e)}")
            print("尝试重新连接串口...")
            self.serial = None
            return False
        except Exception as e:
            print(f"发送投影仪命令时发生未知错误: {str(e)}")
            return False
            
    def power_on(self):
        print("尝试打开投影仪...")
        return self.send_command(self.COMMANDS['power_on'])
        
    def power_off(self):
        print("尝试关闭投影仪...")
        return self.send_command(self.COMMANDS['power_off'])
        
    def flip_image(self):
        print("尝试翻转图像...")
        return self.send_command(self.COMMANDS['flip'])
        
    def brightness_up(self):
        print("尝试增加亮度...")
        return self.send_command(self.COMMANDS['brightness_up'])
        
    def brightness_down(self):
        print("尝试减少亮度...")
        return self.send_command(self.COMMANDS['brightness_down'])
        
    def contrast_up(self):
        print("尝试增加对比度...")
        return self.send_command(self.COMMANDS['contrast_up'])
        
    def contrast_down(self):
        print("尝试减少对比度...")
        return self.send_command(self.COMMANDS['contrast_down'])
        
    def sharpness_up(self):
        print("尝试增加锐度...")
        return self.send_command(self.COMMANDS['sharpness_up'])
        
    def sharpness_down(self):
        print("尝试减少锐度...")
        return self.send_command(self.COMMANDS['sharpness_down'])
        
    def hue_up(self):
        print("尝试增加色度...")
        return self.send_command(self.COMMANDS['hue_up'])
        
    def hue_down(self):
        print("尝试减少色度...")
        return self.send_command(self.COMMANDS['hue_down'])
        
    def saturation_up(self):
        print("尝试增加饱和度...")
        return self.send_command(self.COMMANDS['saturation_up'])
        
    def saturation_down(self):
        print("尝试减少饱和度...")
        return self.send_command(self.COMMANDS['saturation_down'])
        
    def keystone_vertical_up(self):
        print("尝试增加垂直梯形校正...")
        return self.send_command(self.COMMANDS['keystone_vertical_up'])
        
    def keystone_vertical_down(self):
        print("尝试减少垂直梯形校正...")
        return self.send_command(self.COMMANDS['keystone_vertical_down'])
        
    def keystone_horizontal_up(self):
        print("尝试增加水平梯形校正...")
        return self.send_command(self.COMMANDS['keystone_horizontal_up'])
        
    def keystone_horizontal_down(self):
        print("尝试减少水平梯形校正...")
        return self.send_command(self.COMMANDS['keystone_horizontal_down'])
        
    def light_axis_confirm(self):
        print("确认光轴调整...")
        return self.send_command(self.COMMANDS['light_axis_confirm'])
        
    def light_axis_positive(self):
        print("正向调整光轴...")
        return self.send_command(self.COMMANDS['light_axis_positive'])
        
    def light_axis_negative(self):
        print("负向调整光轴...")
        return self.send_command(self.COMMANDS['light_axis_negative'])
        
    def phase_exit(self):
        print("退出相位校正...")
        return self.send_command(self.COMMANDS['phase_exit'])
        
    def phase_positive(self):
        print("正向校正相位...")
        return self.send_command(self.COMMANDS['phase_positive'])
        
    def phase_negative(self):
        print("负向校正相位...")
        return self.send_command(self.COMMANDS['phase_negative'])
        
    def update_last_activity(self):
        self.last_update_time = time.time()
        
    def check_and_power_off(self):
        if self.last_update_time > 0 and time.time() - self.last_update_time > 30:
            print("检测到30秒无活动，准备关闭投影仪...")
            self.power_off()
            self.last_update_time = 0 