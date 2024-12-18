from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit,
                            QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QFont, QIcon
import sys
import os
from functools import partial
import time

# 在文件开头添加获取图标路径的代码
ICON_PATH = os.path.join(os.path.dirname(__file__), 'icon.ico')

# 添加字体常量
FONT_FAMILY = "Microsoft YaHei UI"

class NumberExtractorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("提取数字")
        
        if parent:
            # 获取父窗口的位置和大小
            self.parent = parent
            self.updateGeometry()
            
            # 监听父窗口的大小变化
            parent.installEventFilter(self)
        else:
            self.setFixedSize(400, 700)
        
        # 移除所有边框，添加左边框
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: none;
                border-left: 1px solid #ddd;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("提取数字工具")
        title.setFont(QFont(FONT_FAMILY, 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 输入区域
        input_label = QLabel("请输入包含数字的文本：")
        input_label.setFont(QFont(FONT_FAMILY, 12))
        layout.addWidget(input_label)
        
        self.input_area = QTextEdit()
        self.input_area.setFont(QFont(FONT_FAMILY, 12))
        self.input_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                background-color: white;
                padding: 8px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::handle:vertical:pressed {
                background: rgba(0, 0, 0, 0.4);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        layout.addWidget(self.input_area)
        
        # 按钮区
        button_layout = QHBoxLayout()
        
        extract_btn = QPushButton("提取数字")
        extract_btn.setFont(QFont(FONT_FAMILY, 12))
        extract_btn.setFixedHeight(35)
        extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        extract_btn.clicked.connect(self.extract_numbers)
        button_layout.addWidget(extract_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont(FONT_FAMILY, 12))
        cancel_btn.setFixedHeight(35)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # 提示文本
        hint = QLabel("提示：将自动提取文本中的所有数字并用加号连接")
        hint.setFont(QFont(FONT_FAMILY, 10))
        hint.setStyleSheet("color: #666;")
        layout.addWidget(hint)
        
        self.result = None
    
    def updateGeometry(self):
        """更新对话框的位置和大小"""
        if not self.parent:
            return
        
        # 获取父窗口在屏幕上的位置和大小
        parent_pos = self.parent.pos()
        parent_size = self.parent.size()
        
        # 设置对话框高度与父窗口一致
        self.setFixedHeight(parent_size.height())
        
        # 计算对话框的位置
        dialog_x = parent_pos.x() + parent_size.width()  # 紧贴父窗口右边
        dialog_y = parent_pos.y()                        # 与父窗口顶部对齐
        
        # 设置对话框位置和大小
        self.move(dialog_x, dialog_y)
    
    def eventFilter(self, obj, event):
        """监听父窗口事件"""
        if obj == self.parent and event.type() in [event.Type.Resize, event.Type.Move]:
            self.updateGeometry()
        return super().eventFilter(obj, event)
    
    def showEvent(self, event):
        """重写显示事件，添加滑入动画"""
        super().showEvent(event)
        
        # 更新位置和大小
        if hasattr(self, 'parent'):
            self.updateGeometry()
        
        # 创建位置动画
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 设置起始和结束位置
        current_pos = self.pos()
        start_pos = QPoint(current_pos.x() - self.width(), current_pos.y())
        
        self.move(start_pos)  # 先移动到起始位置
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(current_pos)
        self.anim.start()
    
    def closeEvent(self, event):
        """重写关闭事件，添加滑出动画"""
        # 创建位置动画
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.Type.InCubic)
        
        # 设置起始和结束位置
        start_pos = self.pos()
        end_pos = QPoint(start_pos.x() + self.width(), start_pos.y())
        
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        
        # 动画完成后关闭窗口
        self.anim.finished.connect(super().closeEvent)
        self.anim.finished.connect(self.close)
        
        # 启动动画
        self.anim.start()
        event.ignore()
    
    def extract_numbers(self):
        try:
            text = self.input_area.toPlainText().strip()
            if not text:
                QMessageBox.warning(self, "提示", "请输入文本")
                return
            
            numbers = []
            current_num = ""
            
            for char in text:
                if char.isdigit():
                    current_num += char
                else:
                    if current_num:
                        numbers.append(int(current_num))
                        current_num = ""
            
            if current_num:
                numbers.append(int(current_num))
            
            if not numbers:
                QMessageBox.information(self, "提示", "未找到数字")
                return
            
            formatted_numbers = [f"{num:,}" for num in numbers]
            self.result = " + ".join(formatted_numbers)
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提取数字时出错：{str(e)}")

class CalculatorQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数字计算器")
        self.setMinimumSize(500, 600)  # 减小最小尺寸
        self.resize(500, 600)          # 设置初始大小
        
        # 设置窗口图标
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        
        # 移除固定大小的窗口标志
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 标题
        title = QLabel("数字计算器")
        title.setFont(QFont(FONT_FAMILY, 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 输入区域
        input_label = QLabel("请输入要计算的数字")
        input_label.setFont(QFont(FONT_FAMILY, 12))
        layout.addWidget(input_label)

        self.input_area = QTextEdit()
        self.input_area.setFont(QFont("Consolas", 14))
        self.input_area.setFixedHeight(120)
        self.input_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                background-color: white;
                padding: 8px;
                margin-bottom: 20px;  /* 增加底部边距到20px */
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::handle:vertical:pressed {
                background: rgba(0, 0, 0, 0.4);
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        layout.addWidget(self.input_area)

        # 在输入区域之后，创建一个按钮容器
        button_container = QWidget()
        button_container_layout = QVBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)  # 移除容器的内边距
        button_container_layout.setSpacing(5)  # 减小按钮组之间的间距

        # 运算符按钮区域
        operator_layout = QHBoxLayout()
        operator_layout.setSpacing(8)
        operator_layout.setContentsMargins(0, 0, 0, 0)
        operators = ['+', '-', '×', '÷']
        self.operator_buttons = []  # 保存运算符按钮的引用
        
        for operator in operators:
            btn = QPushButton(operator)
            btn.setFont(QFont(FONT_FAMILY, 12))
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
                QPushButton:focus {
                    outline: none;
                }
            """)
            btn.clicked.connect(lambda checked, op=operator: self.add_operator(op))
            operator_layout.addWidget(btn)
            self.operator_buttons.append(btn)  # 将按钮添加到列表中
        button_container_layout.addLayout(operator_layout)

        # 功能按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # 设置功能按钮之间的间距
        button_layout.setContentsMargins(0, 0, 0, 0)  # 移除功能按钮区域的边距
        buttons = [
            ("提取数字", "#9C27B0", self.extract_numbers),
            ("清除", "#F44336", self.clear),
            ("计算结果", "#4CAF50", self.calculate)
        ]
        for text, color, func in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont(FONT_FAMILY, 12))
            btn.setFixedHeight(40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                }}
                QPushButton:pressed {{
                    background-color: {color}aa;
                }}
            """)
            btn.clicked.connect(func)
            button_layout.addWidget(btn)
        button_container_layout.addLayout(button_layout)

        # 将���钮容器添加到主布局时设置固定的上边距
        button_container.setStyleSheet("""
            QWidget {
                margin-top: 10px;  /* 给按钮容器添加上边距 */
            }
        """)
        layout.addWidget(button_container)

        # 结果显示区域
        result_label = QLabel("计算结果")
        result_label.setFont(QFont(FONT_FAMILY, 12))
        layout.addWidget(result_label)

        self.result_display = QLineEdit()
        self.result_display.setFont(QFont("Consolas", 14))
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                background-color: white;
                padding: 8px;
            }
        """)
        layout.addWidget(self.result_display)

        # 计算过程显示区域
        process_label = QLabel("计算过程")
        process_label.setFont(QFont(FONT_FAMILY, 12))
        layout.addWidget(process_label)

        self.process_display = QTextEdit()
        self.process_display.setFont(QFont("Consolas", 11))  # 减小字号
        self.process_display.setFixedHeight(100)  # 调整高度
        self.process_display.setReadOnly(True)
        self.process_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                background-color: white;
                padding: 8px;
                margin-bottom: 5px;  /* 减小底部边距到5px */
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.3);
            }
            QScrollBar::handle:vertical:pressed {
                background: rgba(0, 0, 0, 0.4);
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        layout.addWidget(self.process_display)

        # 提示文本
        hints = [
            "• 支持直接输入数字，数字间用运算符分隔",
            "• 输入时会自动进行式化处理",
            "• 按Enter键以快速计算结果"
        ]
        hint_container = QWidget()
        hint_layout = QVBoxLayout(hint_container)
        hint_layout.setContentsMargins(0, 5, 0, 0)  # 减小顶部边距到5px
        hint_layout.setSpacing(2)

        for hint in hints:
            hint_label = QLabel(hint)
            hint_label.setFont(QFont(FONT_FAMILY, 10))
            hint_label.setStyleSheet("color: #666;")
            hint_layout.addWidget(hint_label)

        layout.addWidget(hint_container)

        # 设置窗口居中
        self.center_window()

        # 绑定车键
        self.input_area.installEventFilter(self)

        # 改用 textEdited 信号
        self.input_area.textChanged.connect(self.on_text_changed)

        # 添加一个标志位来防止递归
        self.is_formatting = False

        # 添加一个变量来跟踪上一次按下Backspace的时间
        self.last_backspace_time = 0

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def eventFilter(self, obj, event):
        if obj == self.input_area and event.type() == event.Type.KeyPress:
            # 处理回车键
            if event.key() == Qt.Key.Key_Return and not event.modifiers():
                self.calculate()
                return True
            
            # 处理乘除号的快捷键
            if event.key() == Qt.Key.Key_8 and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:  # Shift + 8 = *
                self.add_operator('×')
                return True
            if event.key() == Qt.Key.Key_Slash and not event.modifiers():  # /
                self.add_operator('÷')
                return True
            
            # 处理加减号的快捷键
            if event.key() == Qt.Key.Key_Equal and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:  # Shift + = (+)
                self.add_operator('+')
                return True
            if event.key() == Qt.Key.Key_Minus and not event.modifiers():  # -
                self.add_operator('-')
                return True
            
            # 处理Backspace键
            if event.key() == Qt.Key.Key_Backspace:
                text = self.input_area.toPlainText().strip()
                parts = text.split()
                
                # 如果没有内容，直接返回
                if not parts:
                    return False
                    
                # 如果最后一个是运算符，检查是否是双击Backspace
                if parts[-1] in ['+', '-', '×', '÷']:
                    current_time = time.time()
                    if current_time - self.last_backspace_time < 0.3:  # 300毫秒内的双击
                        parts = parts[:-1]
                        new_text = ' '.join(parts)
                        if new_text:
                            new_text += ' '  # 如果还有内容，添加一个空格
                        self.input_area.setPlainText(new_text)
                        
                        # 设置焦点并将光标移到末尾
                        self.input_area.setFocus()
                        cursor = self.input_area.textCursor()
                        cursor.movePosition(cursor.MoveOperation.End)
                        self.input_area.setTextCursor(cursor)
                        self.last_backspace_time = 0  # 重置时间
                        return True
                    self.last_backspace_time = current_time
                    return True  # 拦截第一次按下的Backspace
                else:
                    self.last_backspace_time = 0  # 如果不是运算符，重置时间
                    return False  # 让系统处理普通的删除操作
            
        return super().eventFilter(obj, event)

    def add_operator(self, operator):
        """添加运算符"""
        try:
            text = self.input_area.toPlainText().strip()
            parts = text.split()
            
            # 如果没有内容，不添加运算符
            if not parts:
                return
            
            # 如果最后一个是运算符，直接替换
            if parts[-1] in ['+', '-', '×', '÷']:
                parts[-1] = operator
            # 如果最后一个是数字，添加运算符
            elif parts[-1].replace(',', '').isdigit():
                parts.append(operator)
            
            # 更新显示
            new_text = ' '.join(parts) + ' '
            self.input_area.setPlainText(new_text)
            
            # 设置焦点并将光标移到末尾
            self.input_area.setFocus()
            cursor = self.input_area.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.input_area.setTextCursor(cursor)
            
        except Exception as e:
            print(f"Add operator error: {str(e)}")
            pass

    def on_text_changed(self):
        """处理文本变化事件"""
        if not self.is_formatting:
            self.is_formatting = True
            self.format_input()
            self.is_formatting = False

    def format_input(self):
        """格式化输入内容"""
        try:
            # 获取当前输入
            text = self.input_area.toPlainText().strip()
            if not text:
                return

            # 处理键入的 * 和 / 转换为 × 和 ÷
            text = text.replace('*', '×').replace('/', '÷')
            
            # 规范化运算符前后的空格
            for op in ['+', '-', '×', '÷']:
                text = text.replace(f' {op} ', op)  # 先移除已有的空格
                text = text.replace(op, f' {op} ')  # 再统一添加空格
            
            # 移除多余的空格和逗号
            parts = text.split()
            formatted_parts = []
            
            for part in parts:
                # 移除逗号
                part = part.replace(',', '')
                
                # 如果是运算符
                if part in ['+', '-', '×', '÷']:
                    # 如果已经有内容且最后一个不是运算符，添加运算符
                    if formatted_parts and not formatted_parts[-1] in ['+', '-', '×', '÷']:
                        formatted_parts.append(part)
                    # 如果最后一个是运算符，直接替换
                    elif formatted_parts and formatted_parts[-1] in ['+', '-', '×', '÷']:
                        formatted_parts[-1] = part
                # 如果是数字
                elif part.isdigit():
                    formatted_parts.append(f"{int(part):,}")
            
            # 组合格式化后的文本
            formatted_text = ' '.join(formatted_parts)
            
            # 如果最后一个字符是运算符，确保它后面有一个空格
            if formatted_text and formatted_text[-1] in ['+', '-', '×', '÷']:
                formatted_text += ' '
            
            # 更新显示
            self.input_area.setPlainText(formatted_text)
            
            # 设置焦点并将光标移到末尾
            self.input_area.setFocus()
            cursor = self.input_area.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.input_area.setTextCursor(cursor)
            
        except Exception as e:
            print(f"Format error: {str(e)}")
            pass

    def calculate(self):
        """计算结果"""
        try:
            expression = self.input_area.toPlainText().strip()
            
            # 移除所有空格和逗号
            expression = expression.replace(" ", "").replace(",", "")
            
            # 分割数字和运算符
            parts = []
            current_num = ""
            
            for char in expression:
                if char in ['+', '-', '×', '÷']:
                    if current_num:
                        parts.append(int(current_num))
                        current_num = ""
                    parts.append(char)
                elif char.isdigit():
                    current_num += char
            
            if current_num:
                parts.append(int(current_num))
            
            # 初始化过程文本
            process_text = ""
            
            # 处理乘除法
            i = 0
            has_multiply_divide = False
            while i < len(parts):
                if isinstance(parts[i], str) and parts[i] in ['×', '÷']:
                    if not has_multiply_divide:
                        process_text += "乘除运算：\n"
                        has_multiply_divide = True
                    
                    left = parts[i-1]
                    right = parts[i+1]
                    
                    if parts[i] == '×':
                        result = left * right
                        process_text += f"{left:,} × {right:,} = {result:,}\n"
                    else:  # 除法
                        if right == 0:
                            raise ValueError("除数不能为零")
                        result = left / right
                        if result.is_integer():
                            process_text += f"{left:,} ÷ {right:,} = {int(result):,}\n"
                        else:
                            process_text += f"{left:,} ÷ {right:,} = {result:.2f}\n"
                    
                    parts[i-1:i+2] = [result]
                    i -= 1
                i += 1
            
            # 处理加减法
            if len(parts) > 1:
                if has_multiply_divide:
                    process_text += "\n"  # 如果有乘除运算，添加空行
                process_text += "加减运算：\n"
                result = parts[0]
                i = 1
                while i < len(parts):
                    if parts[i] == '+':
                        process_text += f"{result:,} + {parts[i+1]:,} = "
                        result += parts[i+1]
                        process_text += f"{result:,}\n"
                    elif parts[i] == '-':
                        process_text += f"{result:,} - {parts[i+1]:,} = "
                        result -= parts[i+1]
                        process_text += f"{result:,}\n"
                    i += 2
            else:
                result = parts[0]
            
            # 显示计算过程
            self.process_display.setPlainText(process_text)
            
            # 显示最终结果
            if isinstance(result, int) or result.is_integer():
                result = int(result)
                self.result_display.setText(f"= {result:,}")
            else:
                # 处理小数，保留2位
                result = round(result, 2)
                if result == int(result):
                    self.result_display.setText(f"= {int(result):,}")
                else:
                    self.result_display.setText(f"= {result:,.2f}")
        
        except ValueError as ve:
            QMessageBox.critical(self, "错误", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "错误", 
                "计算出错：请确保输入格式正确\n例如：123 + 456 - 789")

    def clear(self):
        """清除输入和结果"""
        self.input_area.clear()
        self.process_display.clear()
        self.result_display.clear()

    def extract_numbers(self):
        dialog = NumberExtractorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.result:
            self.input_area.setPlainText(dialog.result)
            self.input_area.setFocus()
            cursor = self.input_area.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.input_area.setTextCursor(cursor)

def main():
    app = QApplication(sys.argv)
    # 设置应用程序图标（任务栏图标）
    if os.path.exists(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
    window = CalculatorQt()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 