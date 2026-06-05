"""
CONSISTENCY CHECKER
Validates that character looks the same across all panels using color and structure similarity
"""

import numpy as np

from PIL import Image

import os

import cv2

class ConsistencyChecker:

    def __init__(self):

        self.reference_features = None

    

    def extract_features(self, image_path):

        """Extract image features (color histogram + grayscale thumbnail) for comparison"""

        if not os.path.exists(image_path):

            raise FileNotFoundError(f"Image not found at {image_path}")

            

                                         

        img_cv = cv2.imread(image_path)

        if img_cv is None:

            raise ValueError(f"Could not read image at {image_path}")

            

        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

                                                                                                    

        hist = cv2.calcHist([hsv], [0, 1], None, [8, 8], [0, 180, 0, 256])

        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

        

                                                

        img_pil = Image.open(image_path).convert('L')

        img_resized = img_pil.resize((128, 128))

        pixels = np.array(img_resized).flatten()

        

        return {

            'histogram': hist,

            'pixels': pixels,

            'mean_brightness': np.mean(pixels),

            'size': img_pil.size

        }

    

    def set_reference(self, reference_image_path):

        """Set the reference character image"""

        self.reference_features = self.extract_features(reference_image_path)

        print(f"✅ Reference set: {reference_image_path}")

    

    def check_consistency(self, image_path, threshold=0.60):

        """Check if image matches reference character using color and structure similarity"""

        if self.reference_features is None:

            raise ValueError("No reference set. Call set_reference() first.")

            

        features = self.extract_features(image_path)

        

                                                 

        color_score = cv2.compareHist(

            self.reference_features['histogram'], 

            features['histogram'], 

            cv2.HISTCMP_CORREL

        )

                         

        color_score = max(0.0, min(1.0, color_score))

        

                                                                   

                                                                  

        p1 = self.reference_features['pixels']

        p2 = features['pixels']

        

                                

        std1, std2 = np.std(p1), np.std(p2)

        if std1 > 0 and std2 > 0:

            struct_score = np.corrcoef(p1, p2)[0, 1]

        else:

            struct_score = 0.0

        struct_score = max(0.0, min(1.0, struct_score))

        

                                                                                  

        overall_score = 0.7 * color_score + 0.3 * struct_score

        

        return {

            'consistent': overall_score >= threshold,

            'score': float(overall_score),

            'color_score': float(color_score),

            'struct_score': float(struct_score)

        }

    

    def validate_panels(self, panel_paths, reference_path):

        """Validate all panels against reference"""

        self.set_reference(reference_path)

        

        results = {}

        for path in panel_paths:

            results[path] = self.check_consistency(path)

        

        return results

def get_consistency_checker():

    return ConsistencyChecker()

