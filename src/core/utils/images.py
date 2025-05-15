import logging
import os

from PIL import Image, ImageEnhance

from django.conf import settings


class ImageProcessor:
    """Performs different image manipulations:
    - crop (if necessary)
    - resize
    """

    def __init__(self, image_path: str) -> None:
        self.image_path = image_path

    def create_thumbnail(
            self,
            width: int,
            height: int
    ) -> None:
        """
        Performs image resize to predefined width
        """

        try:
            file_name, file_extension = os.path.splitext(self.image_path)
            with Image.open(self.image_path) as image:
                # Obtain image original format and dimensions
                img_format = image.format
                image_ratio = image.size[0] / image.size[1]
                resize_ratio = width / height

                # Check original image proportions vs needed
                if image_ratio > resize_ratio:
                    # Need to crop left and right edges
                    resize_factor = height / image.size[1]
                    cropped_width = width / resize_factor
                    edge = int((image.size[0] - cropped_width) / 2)
                    cropped_image = image.crop(
                        (edge, 0, image.size[0] - edge, image.size[1])
                    )
                else:
                    # Need to crop from top and bottom
                    resize_factor = width / image.size[0]
                    cropped_height = height / resize_factor
                    edge = int((image.size[1] - cropped_height) / 2)
                    cropped_image = image.crop(
                        (0, edge, image.size[0], image.size[1] - edge)
                    )

                # Create thumbnail for requested width and height
                thumbnail_image = cropped_image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS
                )
                # Save it into images folder
                outfile = settings.MEDIA_ROOT.joinpath(
                    "{}_{}x{}{}".format(
                        file_name,
                        str(width),
                        str(height),
                        file_extension
                    )
                )
                # Apply filters
                enhancer = ImageEnhance.Sharpness(thumbnail_image)
                thumbnail_image = enhancer.enhance(2)

                # And save result
                thumbnail_image.save(
                    outfile,
                    format=img_format,
                    quality=settings.IMAGE_QUALITY,
                    dpi=(settings.IMAGE_DPI, settings.IMAGE_DPI),
                    progressive=True
                )
        except OSError as error:
            logging.error(
                "Cannot resize photo {}: {}".format(
                    self.image_path,
                    error
                )
            )
