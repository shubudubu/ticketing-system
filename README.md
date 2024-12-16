# ticketing
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("Your data here")
qr.make(fit=True)

# Create the QR code image
qr_img = qr.make_image(fill='black', back_color='white')

# Create a blank image with a 16:9 ratio (e.g., 480x270)
image_width = 480
image_height = 270
final_img = Image.new('RGB', (image_width, image_height), color='white')

# Resize QR code to fit within the image
qr_size = 180  # Adjust QR size to fit well on the right side
qr_img = qr_img.resize((qr_size, qr_size))

# Paste the QR code on the right side of the image (with padding)
qr_padding = 20  # Padding between the QR code and the edge
final_img.paste(qr_img, (image_width - qr_size - qr_padding, (image_height - qr_size) // 2))

# Add "SHOWTIME" text on the left side
draw = ImageDraw.Draw(final_img)

# Load a font (you can change the font and size)
try:
    font = ImageFont.truetype("arial.ttf", 40)  # You can change the font size and style here
except IOError:
    font = ImageFont.load_default()

# Text to display
text = "SHOWTIME"

# Use textbbox to get the size of the text
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

# Calculate position for the text
text_x = 20  # Padding from the left side
text_y = (image_height - text_height) // 2  # Vertically center the text

draw.text((text_x, text_y), text, font=font, fill='black')

# Save the final image
final_img.save("showtime_qr_code_16_9.png")

# Show the final image (optional)
final_img.show()
