#!/usr/bin/env python3
import sys
import os
import base64
import json
import signal
from io import BytesIO
from threading import Thread
from flask import Flask, request, jsonify
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
import markdown2
import matplotlib.pyplot as plt
import re
# from projector_controller import ProjectorController  # 注释掉投影仪控制器导入

class DisplaySignals(QObject):
    update_content = pyqtSignal(str, str)  # content, content_type
    next_page = pyqtSignal()
    prev_page = pyqtSignal()

class DisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = DisplaySignals()
        self.signals.update_content.connect(self.update_content)
        self.signals.next_page.connect(self.next_page)
        self.signals.prev_page.connect(self.prev_page)
        
        # 注释掉投影仪相关代码
        # self.projector = ProjectorController()
        # self.projector.power_off()
        
        # 设置固定分辨率
        self.setFixedSize(720, 1560)
        self.setWindowTitle("显示服务")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 设置背景色为黑色
        self.setStyleSheet("background-color: black;")
        self.central_widget.setStyleSheet("background-color: black;")
        
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.content_label.setWordWrap(True)
        # 调整字体大小以适应竖屏显示
        self.content_label.setFont(QFont("Arial", 20))
        self.content_label.setStyleSheet("color: white; padding: 20px; text-align: left;")
        self.layout.addWidget(self.content_label)
        
        # 分页相关变量
        self.current_content = ""
        self.current_type = ""
        self.pages = []
        self.current_page = 0
        self.page_timer = QTimer()
        self.page_timer.timeout.connect(self.auto_next_page)
        self.page_interval = 5000  # 5秒
        
        self.showFullScreen()
    
    def cleanup(self):
        """清理资源"""
        print("正在清理资源...")
        # 停止分页计时器
        if hasattr(self, 'page_timer'):
            self.page_timer.stop()
        # 注释掉投影仪相关清理代码
        # if hasattr(self, 'projector') and hasattr(self.projector, 'power_off_timer'):
        #     self.projector.power_off_timer.stop()
        # if hasattr(self, 'projector') and hasattr(self.projector, 'serial') and self.projector.serial:
        #     try:
        #         self.projector.serial.close()
        #     except:
        #         pass
        print("资源清理完成")
    
    def split_content(self, content):
        """将内容分页"""
        # 获取屏幕高度
        screen_height = self.height() - 40  # 减去padding
        test_label = QLabel()
        test_label.setFont(self.content_label.font())
        test_label.setWordWrap(True)
        test_label.setFixedWidth(self.width() - 40)  # 减去padding
        
        pages = []
        current_page = []
        current_height = 0
        
        # 按行分割内容
        lines = content.split('\n')
        
        for line in lines:
            test_label.setText('\n'.join(current_page + [line]))
            new_height = test_label.sizeHint().height()
            
            if current_height > 0 and new_height > screen_height:
                # 当前页已满，保存当前页并开始新页
                pages.append('\n'.join(current_page))
                current_page = [line]
                current_height = test_label.setText(line)
                current_height = test_label.sizeHint().height()
            else:
                current_page.append(line)
                current_height = new_height
        
        # 添加最后一页
        if current_page:
            pages.append('\n'.join(current_page))
        
        return pages
    
    def update_content(self, content, content_type):
        # 注释掉投影仪相关代码
        # self.projector.power_on()
        # self.projector.update_last_activity()
        
        self.current_content = content
        self.current_type = content_type
        
        if content_type == "image":
            try:
                # 移除 data:image/jpeg;base64, 前缀
                if content.startswith('data:image'):
                    content = content.split(',', 1)[1]
                    
                image_data = base64.b64decode(content)
                image = QImage.fromData(image_data)
                if image.isNull():
                    raise Exception("无法从数据创建QImage")
                    
                pixmap = QPixmap.fromImage(image)
                if pixmap.isNull():
                    raise Exception("无法从QImage创建QPixmap")
                
                # 使用固定的显示屏分辨率
                scaled_pixmap = pixmap.scaled(
                    720, 1560,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # 计算居中显示的位置
                x_offset = (720 - scaled_pixmap.width()) // 2
                y_offset = (1560 - scaled_pixmap.height()) // 2
                
                self.content_label.setPixmap(scaled_pixmap)
                self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.content_label.setContentsMargins(x_offset, y_offset, x_offset, y_offset)
                print("图片显示成功")
            except Exception as e:
                error_msg = f"图片显示错误: {str(e)}"
                print(error_msg)
                self.content_label.setText(error_msg)
        else:
            # 处理文本或Markdown内容
            if content_type == "text":
                # 处理纯文本
                content = content.replace('\n', '<br>')
                processed_content = f'<div style="text-align: left;">{content}</div>'
            elif content_type == "markdown":
                # 处理Markdown
                try:
                    def latex_to_image(match, is_block=False):
                        latex = match.group(1)
                        before_newline = match.string[max(0, match.start() - 2):match.start()].endswith('\n')
                        after_newline = match.string[match.end():min(len(match.string), match.end() + 2)].startswith('\n')
                        should_center = before_newline and after_newline
                        
                        print(f"正在渲染{'块级' if should_center else '行内'}公式: {latex}")
                        try:
                            if should_center:
                                plt.figure(figsize=(2, 1), facecolor='none')
                                fontsize = 24
                                scale_width, scale_height = 200, 100
                            else:
                                plt.figure(figsize=(1, 0.5), facecolor='none')
                                fontsize = 20
                                scale_width, scale_height = 100, 50
                                
                            plt.text(0.5, 0.5, f'${latex}$', fontsize=fontsize, ha='center', va='center', color='white')
                            plt.axis('off')
                            
                            buf = BytesIO()
                            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
                            plt.close()
                            buf.seek(0)
                            image = QImage.fromData(buf.getvalue())
                            pixmap = QPixmap.fromImage(image)
                            
                            scaled_pixmap = pixmap.scaled(scale_width, scale_height, Qt.AspectRatioMode.KeepAspectRatio)
                            print(f"公式渲染成功: {latex}")
                            
                            if should_center:
                                return f'<div style="text-align: center; margin: 10px 0;"><img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}" style="background-color: transparent;" /></div>'
                            else:
                                return f'<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}" style="background-color: transparent; vertical-align: middle;" />'
                                
                        except Exception as e:
                            print(f"公式渲染失败: {latex}, 错误: {str(e)}")
                            return f'<div class="math">Error: {latex}</div>'
                    
                    print("开始处理 LaTeX 公式...")
                    content = re.sub(r'\$\$(.*?)\$\$', lambda m: latex_to_image(m, True), content)
                    content = re.sub(r'\$(.*?)\$', lambda m: latex_to_image(m, False), content)
                    print("LaTeX 公式处理完成")
                    
                    processed_content = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])
                    processed_content = f'<div style="text-align: left;">{processed_content}</div>'
                except Exception as e:
                    processed_content = f"Markdown渲染错误: {str(e)}"
            
            # 分页显示
            self.pages = self.split_content(processed_content)
            self.current_page = 0
            self.show_current_page()
            
            # 如果有多页，启动自动翻页计时器
            if len(self.pages) > 1:
                self.page_timer.start(self.page_interval)
            else:
                self.page_timer.stop()
    
    def show_current_page(self):
        """显示当前页"""
        if 0 <= self.current_page < len(self.pages):
            self.content_label.setText(self.pages[self.current_page])
            print(f"显示第 {self.current_page + 1} 页，共 {len(self.pages)} 页")
    
    def next_page(self):
        """显示下一页"""
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_current_page()
            # 重置计时器
            if self.page_timer.isActive():
                self.page_timer.start(self.page_interval)
    
    def prev_page(self):
        """显示上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()
            # 重置计时器
            if self.page_timer.isActive():
                self.page_timer.start(self.page_interval)
    
    def auto_next_page(self):
        """自动显示下一页"""
        if self.current_page < len(self.pages) - 1:
            self.next_page()
        else:
            # 最后一页显示完后停止计时器
            self.page_timer.stop()

# 全局变量用于优雅退出
display_window = None
server_thread = None
interrupted = False

def signal_handler(signum, frame):
    """信号处理器"""
    global interrupted, display_window
    print(f"\n接收到信号 {signum}，正在优雅退出...")
    interrupted = True
    
    if display_window:
        display_window.cleanup()
    
    # 退出Qt应用
    if QApplication.instance():
        QApplication.instance().quit()
    
    print("程序已退出")
    sys.exit(0)

def run_display():
    app = QApplication(sys.argv)
    window = DisplayWindow()
    sys.exit(app.exec())

def run_server(display_window):
    flask_app = Flask(__name__)
    
    @flask_app.route('/display', methods=['POST'])
    def display():
        try:
            data = request.get_json()
            if not data or 'content' not in data or 'type' not in data:
                return jsonify({'error': 'Invalid request format'}), 400
            
            content = data['content']
            content_type = data['type']
            
            if content_type not in ['image', 'text', 'markdown']:
                return jsonify({'error': 'Invalid content type'}), 400
            
            display_window.signals.update_content.emit(content, content_type)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @flask_app.route('/page/next', methods=['POST'])
    def next_page():
        """手动显示下一页"""
        display_window.signals.next_page.emit()
        return jsonify({'status': 'success'})
    
    @flask_app.route('/page/prev', methods=['POST'])
    def prev_page():
        """手动显示上一页"""
        display_window.signals.prev_page.emit()
        return jsonify({'status': 'success'})
    
    flask_app.run(host='0.0.0.0', port=5000)

def main():
    global display_window, server_thread
    
    # 设置信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 设置环境变量
    os.environ['QT_QPA_PLATFORM'] = 'wayland'
    os.environ['QT_QPA_WAYLAND_DISABLE_WINDOWDECORATION'] = '1'
    os.environ['XDG_RUNTIME_DIR'] = '/run/user/1002'
    os.environ['WAYLAND_DISPLAY'] = 'wayland-0'
    
    # 创建显示窗口
    app = QApplication(sys.argv)
    display_window = DisplayWindow()
    
    # 启动HTTP服务器
    server_thread = Thread(target=run_server, args=(display_window,))
    server_thread.daemon = True
    server_thread.start()
    
    print("显示服务已启动，按 Ctrl+C 退出")
    
    try:
        # 运行显示窗口
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\n接收到键盘中断信号")
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 