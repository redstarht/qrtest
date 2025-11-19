import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
# 1. QRコード画像を生成
data_list = ['https://example.com/1', 'https://example.com/2', 'https://example.com/3', 'https://example.com/4']
qr_images = []
for data in data_list:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_images.append(img)
# 2. PDFへ配置
pdf_file = "qrcodes_list.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4
# レイアウト設定
qr_size = 40 * mm   # 1つのQRコードのサイズ
margin_x = 20 * mm
margin_y = 20 * mm
gap_x = 10 * mm
gap_y = 10 * mm
cols = 3  # 1行あたりのQRコード数
rows = 4  # 1ページあたりの行数
for idx, img in enumerate(qr_images):
    row = idx // cols
    col = idx % cols
    x = margin_x + col * (qr_size + gap_x)
    y = height - margin_y - (row + 1) * (qr_size + gap_y) + gap_y
    # PIL画像をバイナリにしてPDFに貼り付け
    img_io = io.BytesIO()
    img = img.resize((int(qr_size), int(qr_size)), Image.LANCZOS)
    img.save(img_io, format='PNG')
    img_io.seek(0)
    image_reader = ImageReader(img_io) 
    c.drawImage(image_reader, x, y, qr_size, qr_size)
    # ページ切り替え
    if (idx + 1) % (cols * rows) == 0 and idx + 1 < len(qr_images):
        c.showPage()
c.save()
print("PDF作成完了:", pdf_file)