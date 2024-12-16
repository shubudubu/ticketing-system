import qrcode
import os
import random
import uuid
import csv

# Path to the CSV file
csv_file_path = 'people.csv'

# Read the people data from the CSV file
people = []
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Add each person's details to the list
        people.append({
            "name": row["Name"],
            "phone": row["Phone"],
            "drama": row["Drama"]
        })

# Create a subfolder to save the QR codes
folder_name = "qr_codes"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Generate a QR code for each person and save it in the folder
for i, person in enumerate(people):
    # Generate a random unique ID (using UUID)
    unique_id = str(uuid.uuid4())[:8]  # Shortened for readability (first 8 chars of UUID)
    
    # Prepare the data to encode in the QR code
    qr_data = (
        f"ID: {unique_id}\n"
        f"Name: {person['name']}\n"
        f"Phone: {person['phone']}\n"
        f"Drama: {person['drama']}"
    )
    
    # Generate a random number (for the file name)
    random_number = random.randint(1000, 9999)
    
    # Prepare the file name: Name_1-n_randomnumber.png
    file_name = f"{person['name'].replace(' ', '_')}_{i+1}-{random_number}.png"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code
        border=4,  # Thickness of the border
    )
    
    qr.add_data(qr_data)  # Encode the structured data (ID, Name, Phone, Drama)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the QR code image with the generated file name
    img.save(os.path.join(folder_name, file_name))

print(f"QR codes have been saved to the '{folder_name}' folder.")
