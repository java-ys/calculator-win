import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("数字计算器")
        self.root.geometry("600x800")
        
        # 设置主题样式
        style = ttk.Style()
        style.configure(".", font=("Microsoft YaHei UI", 12))
        
        # 配置现代风格滚动条样式
        style.layout("Vertical.TScrollbar", 
            [('Vertical.Scrollbar.trough',
                {'children': 
                    [('Vertical.Scrollbar.thumb', 
                        {'sticky': 'nswe'})],
                 'sticky': 'ns'})])

        # 配置滚动条颜色和样式
        style.configure("Vertical.TScrollbar",
            troughcolor='#F5F5F5',          # 滚动槽为浅灰色背景
            background='rgba(0,0,0,0.2)',   # 滑块为半透明黑色
            relief="flat",                  # 扁平化
            borderwidth=0,                  # 无边框
            arrowsize=0,                    # 无箭头
            width=8                         # 滚动条宽度
        )

        # 鼠标悬停和按压效果
        style.map("Vertical.TScrollbar",
            background=[
                ('pressed', 'rgba(0,0,0,0.4)'),    # 按压时更深的半透明
                ('active', 'rgba(0,0,0,0.3)')      # 悬停时的半透明
            ]
        )
        
        # 创建主容器
        container = ttk.Frame(root, padding="15")
        container.pack(fill=BOTH, expand=YES)
        
        # 创建标题
        title = ttk.Label(
            container,
            text="数字计算器",
            font=("Microsoft YaHei UI", 24, "bold"),
            bootstyle="primary",
            justify="center"
        )
        title.pack(pady=(0, 15))
        
        # 创建输入框容器
        input_frame = ttk.LabelFrame(
            container,
            text="请输入要计算的数字",
            padding="8",
            bootstyle="primary"
        )
        input_frame.pack(fill=X, pady=(0, 15))
        
        # 创建输入框和滚动条
        input_scroll = ttk.Scrollbar(
            input_frame,
            orient="vertical",
            style="Vertical.TScrollbar"
        )
        input_scroll.pack(side=RIGHT, fill=Y, padx=0)
        
        self.display = tk.Text(
            input_frame,
            font=("Consolas", 14),
            wrap=tk.WORD,
            height=6,
            relief="flat",
            borderwidth=0,
            background="#ffffff",
            highlightthickness=0,
            yscrollcommand=input_scroll.set
        )
        self.display.pack(fill=X, padx=(2, 0))
        input_scroll.config(command=self.display.yview)
        
        # 创建运算符按钮容器
        operator_frame = ttk.Frame(container)
        operator_frame.pack(fill=X, pady=(0, 15))
        
        # 配置列的权重,使按钮均匀分布
        operator_frame.columnconfigure(0, weight=1)
        operator_frame.columnconfigure(1, weight=1)
        operator_frame.columnconfigure(2, weight=1)
        operator_frame.columnconfigure(3, weight=1)
        
        # 创建运算符按钮
        operators = [
            ("+", "primary"),
            ("-", "primary"),
            ("×", "primary"),
            ("÷", "primary")
        ]
        
        for i, (op, style) in enumerate(operators):
            btn = ttk.Button(
                operator_frame,
                text=op,
                command=lambda x=op: self.add_operator(x),
                bootstyle=style
            )
            # 使用grid布局,并设置sticky使按钮填充空间
            btn.grid(row=0, column=i, padx=5, sticky='ew')
        
        # 创建功能按钮容器
        button_frame = ttk.Frame(container)
        button_frame.pack(fill=X, pady=(0, 15))
        
        # 创建提取、清除和计算按钮
        extract_btn = ttk.Button(
            button_frame,
            text="提取数字",
            command=self.extract_numbers,
            bootstyle="info",
            width=15
        )
        extract_btn.pack(side=LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(
            button_frame,
            text="清除",
            command=self.clear,
            bootstyle="danger",
            width=15
        )
        clear_btn.pack(side=LEFT, padx=(0, 10))
        
        calculate_btn = ttk.Button(
            button_frame,
            text="计算结果",
            command=self.calculate,
            bootstyle="success",
            width=15
        )
        calculate_btn.pack(side=LEFT)
        
        # 创建最终结果显示区域
        result_frame = ttk.LabelFrame(
            container,
            text="计算结果",
            padding="12",
            bootstyle="primary"
        )
        result_frame.pack(fill=X, pady=(0, 15))
        
        self.result_display = ttk.Entry(
            result_frame,
            font=("Consolas", 14, "bold"),
            justify="right",
            state="readonly",
            style="Borderless.TEntry"
        )
        self.result_display.pack(fill=X, padx=5, pady=8)
        
        # 创建计算过程显示区域
        process_frame = ttk.LabelFrame(
            container,
            text="计算过程",
            padding="8",
            bootstyle="primary"
        )
        process_frame.pack(fill=X)  # 移除 expand=YES
        
        # 创建计算过程显示框和滚动条
        process_scroll = ttk.Scrollbar(
            process_frame,
            orient="vertical",
            style="Vertical.TScrollbar"
        )
        process_scroll.pack(side=RIGHT, fill=Y, padx=0)
        
        self.process_display = tk.Text(
            process_frame,
            font=("Consolas", 12),
            wrap=tk.WORD,
            height=2,
            relief="flat",
            borderwidth=0,
            background="#ffffff",
            highlightthickness=0,
            state="disabled",
            yscrollcommand=process_scroll.set
        )
        self.process_display.pack(fill=X, padx=(2, 0))
        process_scroll.config(command=self.process_display.yview)
        
        # 添加提示文本
        hint_frame = ttk.Frame(container)
        hint_frame.pack(fill=X, pady=(15, 0))
        
        hints = [
            "• 支持直接输入数字，数字之间用运算符分隔",
            "• 输入时会自动进行格式化处理",
            "• 按Enter键以快速计算结果"
        ]
        
        for hint in hints:
            ttk.Label(
                hint_frame,
                text=hint,
                font=("Microsoft YaHei UI", 10),
                bootstyle="secondary"
            ).pack(anchor=W)
        
        # 绑定快捷键和格式化
        root.bind('<Return>', lambda e: self.calculate())
        self.display.bind('<KeyRelease>', self.format_input)
        self.display.bind('<FocusOut>', self.format_input)
        
        # 设置窗口居中
        self.center_window()
        
        # 添加滚动事件绑定
        def on_mousewheel(event):
            # Windows平台
            if event.delta:
                if event.delta > 0:
                    event.widget.yview_scroll(-1, "units")
                else:
                    event.widget.yview_scroll(1, "units")
            # Linux/Mac平台
            else:
                if event.num == 4:
                    event.widget.yview_scroll(-1, "units")
                elif event.num == 5:
                    event.widget.yview_scroll(1, "units")
            return "break"
        
        self.display.bind("<MouseWheel>", on_mousewheel)  # Windows
        self.display.bind("<Button-4>", on_mousewheel)    # Linux/Mac scroll up
        self.display.bind("<Button-5>", on_mousewheel)    # Linux/Mac scroll down

        self.process_display.bind("<MouseWheel>", on_mousewheel)
        self.process_display.bind("<Button-4>", on_mousewheel)
        self.process_display.bind("<Button-5>", on_mousewheel)
    
    def add_operator(self, operator):
        """添加运算符"""
        try:
            text = self.display.get("1.0", tk.END).strip()
            if not text:
                return
                
            # 如果最后一个字符是运算符，则替换它
            if text[-1] in ['+', '-', '×', '÷']:
                text = text[:-1]
                
            # 添加新运算符
            text += f" {operator} "
            
            # 更新显示
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", text)
            
            # 让输入框获得焦点并将光标移到末尾
            self.display.focus_set()
            self.display.see(tk.END)
            self.display.mark_set(tk.INSERT, tk.END)
        except:
            pass
    
    def format_input(self, event=None):
        """格式化输入内容"""
        try:
            # 获取当前输入
            text = self.display.get("1.0", tk.END).strip()
            if not text:
                return
            
            # 移除所有空格和逗号
            text = text.replace(" ", "").replace(",", "")
            
            # 分割数字和运算符
            parts = []
            current_num = ""
            
            for char in text:
                if char in ['+', '-', '×', '÷']:
                    if current_num:
                        parts.append(current_num)
                        current_num = ""
                    parts.append(char)
                elif char.isdigit():
                    current_num += char
            
            if current_num:
                parts.append(current_num)
            
            # 格式化每个部分
            formatted_parts = []
            for part in parts:
                if part in ['+', '-', '×', '÷']:
                    formatted_parts.append(f" {part} ")
                else:
                    try:
                        num = int(part)
                        formatted_parts.append(f"{num:,}")
                    except:
                        formatted_parts.append(part)
            
            # 组合格式化后的文本
            formatted_text = "".join(formatted_parts)
            
            # 更新显示
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", formatted_text)
                
        except Exception:
            pass
    
    def calculate(self):
        """计算结果"""
        try:
            expression = self.display.get("1.0", tk.END).strip()
            
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
            
            # 准备计算过程显示
            process_text = ""
            for i, part in enumerate(parts):
                if isinstance(part, (int, float)):
                    process_text += f"{part:,}"
                else:
                    process_text += f" {part} "
            
            self.process_display.configure(state="normal")
            self.process_display.delete("1.0", tk.END)
            self.process_display.insert("1.0", process_text)
            self.process_display.configure(state="disabled")
            
            # 算结果
            # 先处理除法
            i = 0
            while i < len(parts):
                if isinstance(parts[i], str) and parts[i] in ['×', '÷']:
                    left = parts[i-1]
                    right = parts[i+1]
                    
                    if parts[i] == '×':
                        result = left * right
                    else:  # 除法
                        if right == 0:
                            raise ValueError("除数不能为零")
                        result = left / right
                    
                    # 替换计算结果
                    parts[i-1:i+2] = [result]
                    i -= 1
                i += 1
            
            # 再处理加减法
            result = parts[0]
            i = 1
            while i < len(parts):
                if parts[i] == '+':
                    result += parts[i+1]
                elif parts[i] == '-':
                    result -= parts[i+1]
                i += 2
            
            # 显示最终结果
            self.result_display.configure(state="normal")
            self.result_display.delete(0, tk.END)
            
            if isinstance(result, int) or result.is_integer():
                result = int(result)
                self.result_display.insert(0, f"= {result:,}")
            else:
                # 处理小数，保2位
                result = round(result, 2)
                if result == int(result):
                    self.result_display.insert(0, f"= {int(result):,}")
                else:
                    self.result_display.insert(0, f"= {result:,.2f}")
            
            self.result_display.configure(state="readonly")
            
        except ValueError as ve:
            messagebox.showerror("错误", str(ve))
        except Exception as e:
            messagebox.showerror(
                "错误",
                "计算出错：请确保输入格式正确\n例如：123 + 456 - 789"
            )
    
    def clear(self):
        """清除输入和结果"""
        self.display.delete("1.0", tk.END)
        self.process_display.configure(state="normal")
        self.process_display.delete("1.0", tk.END)
        self.process_display.configure(state="disabled")
        
        self.result_display.configure(state="normal")
        self.result_display.delete(0, tk.END)
        self.result_display.configure(state="readonly")
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def select_all(self, event=None):
        """选择所有文本"""
        self.display.tag_add('sel', '1.0', 'end')
        return 'break'  # 防止默认行为
    
    def extract_numbers(self):
        """打开提取数字对话框"""
        from number_extractor import NumberExtractor
        
        def update_display(result):
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", result)
        
        NumberExtractor(self.root, update_display)

def main():
    root = ttk.Window(
        title="数字计算器",
        themename="cosmo",
        resizable=(True, True)
    )
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 