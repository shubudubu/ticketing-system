import qrcode
import os
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

folder_name = "qr_codes"
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
    
    img = qr.make_image(fill='black', back_color='white')
    
    img.save(os.path.join(folder_name, file_name))

print(f"QR codes have been saved to the '{folder_name}' folder.")
