# 树莓派投影仪控制系统

这是一个基于树莓派的投影仪控制系统，支持通过串口控制投影仪，并提供Web界面进行内容显示和控制。

## 功能特点

- 通过串口控制投影仪
- 支持所有投影仪控制命令（开关机、亮度、对比度等）
- 自动30秒无活动关机
- Web界面显示内容
- 支持文本、Markdown和图片显示
- 自动分页和翻页功能

## 硬件要求

- 树莓派（推荐树莓派5）
- USB转串口模块
- 投影仪（支持串口控制）

## 软件依赖

- Python 3.x
- PyQt6
- Flask
- pyserial
- markdown2
- matplotlib

## 安装步骤

1. 安装系统依赖：
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pyqt6
```

2. 安装Python依赖：
```bash
pip install flask pyserial markdown2 matplotlib
```

3. 设置串口权限：
```bash
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB0
```

4. 重启系统使权限生效：
```bash
sudo reboot
```

## 使用方法

1. 启动服务：
```bash
sudo python display_service.py
```

2. 使用curl测试显示功能：
```bash
# 显示文本
curl -X POST http://localhost:5000/display \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "content": "测试文本"
  }'

# 显示Markdown
curl -X POST http://localhost:5000/display \
  -H "Content-Type: application/json" \
  -d '{
    "type": "markdown",
    "content": "# 标题\n## 子标题\n- 列表项"
  }'

# 显示图片
curl -X POST http://localhost:5000/display \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "content": "base64编码的图片数据"
  }'
```

3. 手动翻页控制：
```bash
# 下一页
curl -X POST http://localhost:5000/page/next

# 上一页
curl -X POST http://localhost:5000/page/prev
```

## 投影仪控制命令

投影仪支持以下控制命令：

- 开机/关机
- 图像翻转
- 亮度调节（增加/减少）
- 对比度调节（增加/减少）
- 锐度调节（增加/减少）
- 色度调节（增加/减少）
- 饱和度调节（增加/减少）
- 梯形校正（上下/左右）
- 光轴调整（确认/正向/负向）
- 相位校正（退出/正向/负向）

## 文件说明

- `display_service.py`: 主程序文件，包含显示服务和Web服务器
- `projector_controller.py`: 投影仪控制模块，处理串口通信
- `README.md`: 项目说明文档

## 注意事项

1. 确保串口设备正确连接
2. 检查串口权限设置
3. 确保投影仪支持串口控制
4. 串口波特率默认为115200

## 故障排除

如果遇到串口通信问题，请检查：

1. 串口设备是否存在：
```bash
ls -l /dev/ttyUSB0
```

2. 串口是否被占用：
```bash
sudo lsof /dev/ttyUSB0
```

3. USB设备是否被识别：
```bash
dmesg | grep ttyUSB
```

4. 使用minicom测试串口：
```bash
sudo apt-get install minicom
sudo minicom -D /dev/ttyUSB0 -b 115200
```

## 许可证

MIT License 