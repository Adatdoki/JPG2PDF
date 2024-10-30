######### 2024.10.29 17:15:00 ################################## ADATDOKI ######
# Képfájlok PDF-be konvertálása EXIF automatikus és manuális forgatási opciókkal.
# A program először automatikusan alkalmazza az EXIF alapján szükséges forgatásokat,
# majd kérdés alapján kínálja fel a manuális forgatási lehetőségeket.
# Folyamatjelzést nyújt minden kép feldolgozásáról, külön a PDF mentése előtt is.
# Időmérés a PDF létrehozásának kezdetéről és végéről. 300 DPI-re konvertál.
# EXIF orientációs információk és képadatok jelennek meg a PDF oldalain.
# Képmegjelenítés a képernyőn 300 pixeles magassággal, 300 DPI felbontással
# Most az aktuális mappából dolgozik. 0 foknál forgatásnál nem ront a képen.
# Folyamatjelzések az EXIF forgatás és PDF generálás közben.
# Az output PDF fájl: "JPG2PDF_YYMMDD-HHMM.PDF" és a megadott mappába másolódik.
#########1#########2#########3#########4#########5#########6#########7#########8

from PIL import Image, ExifTags
from fpdf import FPDF
import os
from datetime import datetime
from IPython.display import display, IFrame, clear_output
import ipywidgets as widgets

def get_image_creation_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        return datetime.fromtimestamp(os.path.getmtime(image_path))
    except Exception as e:
        print(f"Hiba a dátum lekérésénél: {e}")
        return None

def apply_exif_rotation(image):
    """Automatikus forgatás az EXIF adatok alapján."""
    exif = getattr(image, '_getexif', lambda: None)()
    exif_orientation_info = "Not Available"
    if exif:
        orientation = next((tag for tag, value in exif.items() if ExifTags.TAGS.get(tag, tag) == 'Orientation'), None)
        if orientation:
            exif_orientation_info = "Available"
            orientation_value = exif[orientation]
            if orientation_value == 3:
                return image.rotate(180, expand=True), exif_orientation_info
            elif orientation_value == 6:
                return image.rotate(270, expand=True), exif_orientation_info
            elif orientation_value == 8:
                return image.rotate(90, expand=True), exif_orientation_info
    return image, exif_orientation_info

def process_images_to_pdf(folder_path, output_pdf_path):
    start_time = datetime.now()
    pdf = FPDF()
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]
    )

    rotated_images = []
    print("Feldolgozom a képeket:", end=" ")

    for index, image_file in enumerate(image_files, start=1):
        image_path = os.path.abspath(os.path.join(folder_path, image_file))
        image = Image.open(image_path)
        image, exif_orientation_info = apply_exif_rotation(image)

        # 300 DPI-re csökkentés, ha nagyobb lenne az eredeti felbontás
        target_dpi = 300
        image.thumbnail((int(target_dpi * 8.27), int(target_dpi * 11.7)))  # A4 méretarány

        rotated_images.append((image, image_path, exif_orientation_info))
        print(f"{index}", end=", " if index < len(image_files) else "\n")

    def save_image_to_pdf(pdf, image, image_path, exif_orientation_info, index):
        creation_date = get_image_creation_date(image_path)
        creation_date_str = creation_date.strftime("%Y-%m-%d %H:%M:%S") if creation_date else "N/A"

        pdf.add_page()
        pdf.set_xy(10, 10)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"Full Path: {image_path}", ln=True)
        pdf.cell(0, 5, f"Date: {creation_date_str} EXIF Orientation: {exif_orientation_info}", ln=True)

        image_width, image_height = image.size
        pdf_width, pdf_height = 190, (image_height * 190) / image_width

        image_path_temp = os.path.join(folder_path, f"temp_{os.path.basename(image_path)}")
        image.save(image_path_temp, "JPEG", quality=85)
        pdf.image(image_path_temp, 10, 25, pdf_width, pdf_height)
        os.remove(image_path_temp)
        
        print(f"{index}", end=", " if index < len(rotated_images) else "\n")

    def generate_pdf_without_manual_rotation():
        print("Készítem a PDF-et:", end=" ")
        for index, (image, image_path, exif_orientation_info) in enumerate(rotated_images, start=1):
            save_image_to_pdf(pdf, image, image_path, exif_orientation_info, index)
        finalize_pdf()

    def process_image_with_manual_rotation(index):
        if index >= len(rotated_images):
            finalize_pdf()
            return

        clear_output(wait=True)
        print(f"Képfeldolgozás: {index + 1}")

        image, image_path, exif_orientation_info = rotated_images[index]
        fixed_height = 400
        width_ratio = fixed_height / image.height
        display(image.resize((int(image.width * width_ratio), fixed_height)))

        def rotate_and_save(rotation_degrees):
            clear_output(wait=True)
            rotated_image = image.rotate(rotation_degrees, expand=True) if rotation_degrees != 0 else image
            save_image_to_pdf(pdf, rotated_image, image_path, exif_orientation_info, index + 1)
            process_image_with_manual_rotation(index + 1)

        button_rotate_0 = widgets.Button(description="0°")
        button_rotate_90_left = widgets.Button(description="Balra 90°")
        button_rotate_90_right = widgets.Button(description="Jobbra 90°")
        button_rotate_180 = widgets.Button(description="180°")

        button_rotate_0.on_click(lambda b: rotate_and_save(0))
        button_rotate_90_left.on_click(lambda b: rotate_and_save(90))
        button_rotate_90_right.on_click(lambda b: rotate_and_save(-90))
        button_rotate_180.on_click(lambda b: rotate_and_save(180))

        display(widgets.HBox([button_rotate_0, button_rotate_90_left, button_rotate_90_right, button_rotate_180]))

    import shutil

    def finalize_pdf():
        print("Mentem a PDF-et...")  # Üzenet a PDF mentése előtt
        pdf.output(output_pdf_path)
        end_time = datetime.now()
        processing_time = end_time - start_time
        print(f"\nA PDF sikeresen elkészült: {output_pdf_path}")

        # Fájl másolása a megadott célmappába
        destination_path = input_folder + os.path.basename(output_pdf_path)
        try:
            shutil.copy(output_pdf_path, destination_path)
            print(f"A PDF sikeresen átmásolva ide: {destination_path}")
        except Exception as e:
            print(f"Hiba a PDF másolása közben: {e}")

        print(f"Kezdési idő: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Befejezési idő: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        processing_time_formatted = str(processing_time).split('.')[0]
        print(f"Feldolgozási idő: {processing_time_formatted}")
        display(IFrame(output_pdf_path, width=1400, height=1200))


    def on_yes_clicked(b):
        clear_output(wait=True)
        process_image_with_manual_rotation(0)

    def on_no_clicked(b):
        clear_output(wait=True)
        generate_pdf_without_manual_rotation()

    button_yes = widgets.Button(description="Igen")
    button_no = widgets.Button(description="Nem")
    button_yes.on_click(on_yes_clicked)
    button_no.on_click(on_no_clicked)

    display(widgets.HTML(value="<b>Szükséges a manuális forgatás?</b>"))
    display(widgets.HBox([button_yes, button_no]))

input_folder = "."  # a mappa elérési útvonala, amely tartalmazza a képeket.
output_pdf = f"JPG2PDF_{datetime.now().strftime('%y%m%d-%H%M')}.PDF"
process_images_to_pdf(input_folder, output_pdf)
