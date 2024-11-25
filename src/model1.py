import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def detect_and_save_tables_in_multiple_images(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png') or f.endswith('.jpg')]
    
    for image_file in image_files:
        # Construct full path to the image
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        original_image = image.copy()  # Keep a copy of the original image for visualization
        
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding for better contrast handling
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        # Use dilation to enhance the table lines
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        table_coords = []

        # Loop through contours to detect tables
        for contour in contours:
            # Get bounding box for each contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out small contours (noise) or very thin ones (not tables)
            if w > 100 and h > 100 and w < 1000 and h < 1000:
                # Draw a red bounding box around the detected table
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color (BGR)
                table_coords.append((x, y, w, h))
        
        # Save the image with the red borders
        output_image_path = os.path.join(output_folder, f"detected_{image_file}")
        cv2.imwrite(output_image_path, original_image)
        
        # Optionally visualize the result
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
        print(f"Processed and saved: {output_image_path}")


input_folder = 'output_images'  
output_folder = 'output_folder'  

detect_and_save_tables_in_multiple_images(input_folder, output_folder)
