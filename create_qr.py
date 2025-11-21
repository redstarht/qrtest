
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import os
import datetime
# フォントの読み込み
pdfmetrics.registerFont(TTFont("msgothic", "C:/Windows/Fonts/msgothic.ttc"))
# 指定のデータからQRコードを作成する

# QRコード画像を生成
data_list = [
    {'qr_data': 'https://example.com/1', 'text1': '棚：A', 'text2': '位置：A'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：A', 'text2': '位置：B'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：A', 'text2': '位置：C'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：A', 'text2': '位置：D'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：A', 'text2': '位置：E'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：A', 'text2': '位置：F'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：A', 'text2': '位置：G'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：A', 'text2': '位置：H'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：A', 'text2': '位置：I'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：B', 'text2': '位置：A'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：B', 'text2': '位置：B'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：B', 'text2': '位置：C'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：B', 'text2': '位置：D'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：B', 'text2': '位置：E'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：B', 'text2': '位置：F'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：B', 'text2': '位置：G'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：B', 'text2': '位置：H'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：C', 'text2': '位置：A'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：C', 'text2': '位置：B'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：C', 'text2': '位置：C'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：C', 'text2': '位置：D'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：C', 'text2': '位置：E'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：C', 'text2': '位置：F'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：C', 'text2': '位置：G'},
    {'qr_data': 'https://example.com/1', 'text1': '棚：', 'text2': '位置：'},
    {'qr_data': 'https://example.com/2', 'text1': '棚：', 'text2': '位置：'},
    {'qr_data': 'https://example.com/3', 'text1': '棚：', 'text2': '位置：'},
    {'qr_data': 'https://example.com/4', 'text1': '棚：', 'text2': '位置：'},
]
qr_images = []
for data in data_list:
    qr = qrcode.QRCode(box_size=20, border=1)
    qr.add_data(data['qr_data'])
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_images.append(img)

now = datetime.datetime.now()
timestamp = datetime.datetime.strftime(now, "%Y-%m-%d,%H-%M-%S")

pdf_file = "qrcodes_list.pdf"
if os.path.exists("qrcodes_list.pdf"):
    pdf_file = f"{timestamp}.pdf"


c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4
# レイアウト設定
qr_size = 40 * mm   # QRコード画像のサイズ
margin_x = 30 * mm
margin_y = 30 * mm
gap_x = 10 * mm
gap_y = 10 * mm
text_font = "msgothic"
text_size = 10  # 文字サイズ
text_gap = 4 * mm  # テキスト行間
cols = 3
rows = 4
print(f"1P配置数：{cols * rows}")

"""
width:595
height 841
qr_size:不変 113
group_height：不変 161
group_width:不変 113
x 56
margin x y 56
"""
for idx, (img, item) in enumerate(zip(qr_images, data_list)):
    row = ((idx%(cols * rows) )// cols) 
    col = idx % cols
    # グループ枠のサイズ
    group_width = qr_size
    group_height = (text_size * 2 + text_gap) + \
        qr_size + 6 * mm  # テキスト2行＋QR画像＋余白
    # 左下基準　col と row の番地で指定
    x = margin_x + col * (qr_size + gap_x)
    y = height - margin_y - (row + 1) * (group_height + gap_y) + gap_y
    # 枠線
    c.setLineWidth(1)
    c.rect(x, y, group_width, group_height)
    # テキスト描画
    c.setFont(text_font, text_size)
    text1_y = y + group_height - text_size - 2 * mm
    text2_y = text1_y - text_size - text_gap
    c.drawCentredString(x + group_width / 2, text1_y, item['text1'])
    c.drawCentredString(x + group_width / 2, text2_y, item['text2'])
    # QR画像描画
    img_io = io.BytesIO()
    img = img.resize((int(qr_size), int(qr_size)), Image.LANCZOS)
    img.save(img_io, format='PNG')
    img_io.seek(0)
    image_reader = ImageReader(img_io)
    qr_y = y + 3 * mm  # 下余白を少し空ける
    c.drawImage(image_reader, x, qr_y, qr_size, qr_size)
    # ページ切り替え
    print(f"idx:{idx}")
    print((idx+1) % (cols * rows) )
    if (idx+1) % (cols * rows) == 0 and idx + 1 < len(qr_images):
        c.showPage()
c.save()
print("PDF作成完了:", pdf_file)
