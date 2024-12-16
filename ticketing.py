from PIL import Image, ImageDraw, ImageFont
import os
import qrcode
import random
import uuid
import csv

csv_file_path = 'people.csv'

people = []
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        people.append({
            "name": row["Name"],
            "phone": row["Phone"],
            "drama": row["Drama"]
        })

folder_name = "tickets"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for i, person in enumerate(people):
    unique_id = str(uuid.uuid4())[:8]
    
    qr_data = (
        f"ID: {unique_id}\n"
        f"Name: {person['name']}\n"
        f"Phone: {person['phone']}\n"
        f"Drama: {person['drama']}"
    )
    
    random_number = random.randint(1000, 9999)
    
    file_name = f"{person['name'].replace(' ', '_')}_{i+1}-{random_number}.png"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill='black', back_color='white')

    image_width = 720
    image_height = 405
    final_img = Image.new('RGB', (image_width, image_height))

    gradient = Image.new('RGB', (1, image_height), color=0) 

    draw_gradient = ImageDraw.Draw(gradient)
    start_color = (230, 230, 255)
    end_color = (200, 210, 240)  

    for y in range(image_height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * y / image_height)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * y / image_height)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * y / image_height)
        draw_gradient.line((0, y, 1, y), fill=(r, g, b))

    gradient = gradient.resize((image_width, image_height))
    final_img.paste(gradient)

    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))

    qr_padding = 30
    final_img.paste(qr_img, (image_width - qr_size - qr_padding, (image_height - qr_size) // 2))

    draw = ImageDraw.Draw(final_img)

    # Load fonts
    try:
        font_showtime = ImageFont.truetype("arial.ttf", 60)  
        font_details = ImageFont.truetype("arial.ttf", 40) 
    except IOError:
        font_showtime = ImageFont.load_default()
        font_details = ImageFont.load_default()

    text_showtime = "SHOWTIME"
    showtime_bbox = draw.textbbox((0, 0), text_showtime, font=font_showtime)
    showtime_width, showtime_height = showtime_bbox[2] - showtime_bbox[0], showtime_bbox[3] - showtime_bbox[1]
    showtime_x = 25
    showtime_y = (image_height - showtime_height) // 3.3  

    draw.text((showtime_x, showtime_y), text_showtime, font=font_showtime, fill='black')

    text_details = f"{person['name']}\n{unique_id}\n{person['drama']}"
    details_lines = text_details.split("\n")
    details_y = showtime_y + showtime_height + 10 
    for line in details_lines:
        draw.text((showtime_x, details_y), line, font=font_details, fill='black')
        details_y += font_details.size + 1  

    file_path = os.path.join(folder_name, file_name)
    final_img.save(file_path)

print(f"QR codes have been saved to the '{folder_name}' folder.")
