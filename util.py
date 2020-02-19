import adafruit_miniqr
import terminalio
import displayio


def generate_qr_code_display_group(pybadger, url):
    """Generate and display a QR code for the given URL"""
    qr_code = adafruit_miniqr.QRCode(qr_type=2)
    qr_code.add_data(bytearray(url))
    qr_code.make()

    palette = displayio.Palette(2)
    palette[0] = 0xFFFFFF
    palette[1] = 0x000000

    qr_bitmap = pybadger.bitmap_qr(qr_code.matrix)
    qr_img = displayio.TileGrid(
        qr_bitmap,
        pixel_shader=palette,
        x=int(qr_bitmap.width / 2),
        y=2,
    )

    qr_code = displayio.Group(scale=3)
    qr_code.append(qr_img)

    qr_and_text_group = displayio.Group()
    qr_and_text_group.append(qr_code)
    qr_and_text_group.append(
        pybadger._create_label_group(
            text=url,
            font=terminalio.FONT,
            scale=1,
            height_adjustment=0.84)
    )
    return qr_and_text_group
