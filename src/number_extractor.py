import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import re

class NumberExtractor:
    def __init__(self, parent, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("提取数字")
        self.dialog.geometry("800x700")  # 进一步增加窗口高度
        
        # 使对话框居中
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 创建主容器，减少上下边距
        main_frame = ttk.Frame(self.dialog, padding="20 10 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title = ttk.Label(
            main_frame,
            text="提取数字工具",
            font=("Microsoft YaHei UI", 20, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))
        
        # 创建输入区域容器
        input_frame = ttk.LabelFrame(
            main_frame,
            text="请输入包含数字的文本",
            padding="15",
            bootstyle="primary"
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 创建文本输入框和滚动条
        text_scroll = ttk.Scrollbar(input_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_input = ttk.Text(
            input_frame,
            font=("Microsoft YaHei UI", 12),
            wrap=tk.WORD,
            height=10,  # 减小高度
            yscrollcommand=text_scroll.set
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_scroll.config(command=self.text_input.yview)
        
        # 创建按钮容器
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 创建一个居中的按钮容器
        btn_container = ttk.Frame(btn_frame)
        btn_container.pack(expand=True)  # 使用expand=True来居中
        
        # 创建按钮
        ttk.Button(
            btn_container,
            text="提取数字",
            command=lambda: self.extract(callback),
            bootstyle="primary",
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_container,
            text="取消",
            command=self.dialog.destroy,
            bootstyle="secondary",
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        # 添加提示文本
        hint = ttk.Label(
            main_frame,
            text="提示：将自动提取文本中的所有数字并用加号连接",
            font=("Microsoft YaHei UI", 10),
            bootstyle="secondary"
        )
        hint.pack(anchor=tk.W, pady=(0, 20))  # 增加底部边距
        
        # 设置对话框位置
        self.center_dialog()
        
        # 设置焦点到输入框
        self.text_input.focus_set()
    
    def extract(self, callback):
        """提取数字并通过回调函数返回结果"""
        try:
            # 获取输入的文本
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("警告", "请输入文本")
                return
                
            # 提取数字
            numbers = re.findall(r'\d+', text)
            if not numbers:
                messagebox.showinfo("提示", "未找到数字")
                return
                
            # 格式化数字并添加加号
            formatted_numbers = []
            for num in numbers:
                try:
                    formatted_num = "{:,}".format(int(num))
                    formatted_numbers.append(formatted_num)
                except:
                    continue
            
            result = " + ".join(formatted_numbers)
            
            # 通过回调函数返回结果
            callback(result)
            
            # 关闭对话框
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("错误", f"提取数字时出错：{str(e)}")
    
    def center_dialog(self):
        """将对话框居中显示"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y)) 