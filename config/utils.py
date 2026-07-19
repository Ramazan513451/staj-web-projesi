import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile

def optimize_image(image_field, max_width=1920, quality=85):
    """
    Optimizes the given image field.
    Returns the optimized InMemoryUploadedFile or the original if it couldn't be processed.
    """
    if not image_field:
        return image_field

    # Only process newly uploaded files, not existing FieldFiles
    if not isinstance(image_field.file, UploadedFile):
        return image_field

    try:
        img = Image.open(image_field)
        
        if img.format not in ['JPEG', 'PNG', 'WEBP']:
            if img.mode != 'RGB':
                img = img.convert('RGB')
        else:
            if img.mode != 'RGB' and img.format == 'JPEG':
                img = img.convert('RGB')

        if img.width > max_width:
            output_size = (max_width, int(img.height * (max_width / img.width)))
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            
        img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        filename = image_field.name.rsplit('.', 1)[0] + '.jpg'
        
        return InMemoryUploadedFile(
            output, 'ImageField', filename, 'image/jpeg',
            sys.getsizeof(output), None
        )
    except Exception:
        # If any error occurs during processing (e.g. invalid image), return original
        return image_field
