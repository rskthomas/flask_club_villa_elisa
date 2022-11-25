import qrcode
from io import BytesIO
from flask import send_from_directory, current_app
from flask import Blueprint,url_for,send_file,current_app
from src.web.controllers.auth import login_required

cdn_blueprint = Blueprint(
    "cdn",
    __name__,
    url_prefix="/cdn")


@cdn_blueprint.get('/file/<path:filename>')
@login_required()
def file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@cdn_blueprint.get('/qrcode/<int:member_id>')
def qr_code(member_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(url_for('member.show_license', id=member_id))
    pil_img = qr.make_image(fill_color="white", back_color="black")

    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')
