from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Image
from .serializers import ImageSerializer
import cv2
import numpy as np
import os
from django.conf import settings


# http://127.0.0.1:8000/api/images/        //post image in this url 
# http://127.0.0.1:8000/api/images/{id}/detect_circles/     


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(detail=True, methods=['get'])
    def detect_circles(self, request, pk=None):
        image = self.get_object()
        img_path = os.path.join(settings.MEDIA_ROOT, image.image.name)  
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.blur(gray, (3, 3))

        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=43, minRadius=1, maxRadius=40)

        response_data = {
            "image": image.image.url,
            "circles_detected": 0,
            "circles": []
        }

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            response_data["circles_detected"] = len(detected_circles[0, :])
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                response_data["circles"].append({"center": (a, b), "radius": r})
                cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            output_path = os.path.join(settings.MEDIA_ROOT, 'store/images', f'detected_{os.path.basename(image.image.name)}')
            cv2.imwrite(output_path, img)
            response_data["processed_image"] = settings.MEDIA_URL + 'store/images/' + f'detected_{os.path.basename(image.image.name)}'

        return Response(response_data, status=status.HTTP_200_OK)
