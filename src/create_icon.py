from PIL import Image, ImageDraw, ImageFont
import os

def create_calculator_icon():
    # 创建一个正方形的图像
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制计算器外框
    margin = 20
    draw.rectangle(
        [margin, margin, size-margin, size-margin],
        fill='#2196F3',  # 使用蓝色背景
        outline='#1976D2',
        width=8
    )
    
    # 绘制数字符号
    font_size = 120
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "123"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 添加文字阴影
    draw.text((x+3, y+3), text, fill='#1565C0', font=font)
    # 添加主文字
    draw.text((x, y), text, fill='white', font=font)
    
    # 确保src目录存在
    if not os.path.exists('src'):
        os.makedirs('src')
    
    # 保存��ICO文件
    image.save('src/icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_calculator_icon() 