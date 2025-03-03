from PIL import Image, ImageFont, ImageDraw

font = {
    'lisa': "/Users/honglab/Desktop/lofi-takoyaki/Lisa.ttf"
}

def webp_to_jpg(webp_file, jpg_file):
    img = Image.open(webp_file)
    img.save(jpg_file, "jpeg")

def add_text_in_image(img_draw, text, position, font_path, font_size, font_color=(237, 230, 211)):
    font = ImageFont.truetype(font=font_path, size=font_size)
    img_draw.text(position, text=text, fill=font_color, font=font)

def create_thumbnail(image_file, thumbnail_file, font_name="lisa"):    
    
    img = Image.open(image_file)
    img_draw = ImageDraw.Draw(img)

    font_path = font[font_name]
    
    add_text_in_image(img_draw, "LOFI TAKOYAKI", (75,75), font_path, 100)
    
    
    img_width, img_height = img.size

    bbox = img_draw.textbbox((0, 0), "PLAYLIST", font=ImageFont.truetype(font=font_path, size=200))
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    position = ((img_width - text_width) // 2, (img_height - text_height) // 2)
    
    add_text_in_image(img_draw, "PLAYLIST", position, font_path, 200)
    
    
    img.save(thumbnail_file)

