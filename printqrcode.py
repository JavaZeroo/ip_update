from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
import io
import requests

def print_qrcode(image_url):
    image_content = requests.get(image_url).content
    # 将内容转换为字节流
    image_stream = io.BytesIO(image_content)

    # 使用Pillow打开图片流
    image = Image.open(image_stream)

    # 解析二维码
    decoded_objects = decode(image)

    # 打印解析结果
    # 通常二维码解析结果只有一个，如果有多个也全部打印出来
    qr_codes = decoded_objects[0].data.decode('utf-8')
    print(qr_codes)

    qr = qrcode.QRCode()
    qr.border = 1
    qr.add_data(qr_codes)
    qr.make()
    qr.print_ascii(out=None, tty=False, invert=False)
    return None

if __name__ == '__main__':
    image_path = 'https://th.bing.com/th/id/R.dcf4b6e228aef80dd1a58f4c76f07128?rik=Qj2LybacmBALtA&riu=http%3a%2f%2fpngimg.com%2fuploads%2fqr_code%2fqr_code_PNG25.png&ehk=eKH2pdoegouCUxO1rt6BJXt4avVYywmyOS8biIPp5zc%3d&risl=&pid=ImgRaw&r=0'
    print_qrcode(image_path)