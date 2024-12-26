import sys
import os
import cv2
from src.fruits import DetectedFruits

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1) 

    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
         print(f"Error: File path '{file_path}' doesn't exist.")
         sys.exit(1)
    
    if not os.path.isfile(file_path):
         print(f"Error: '{file_path}' isn't a file.")
         sys.exit(1)

    try:
        cv_image = cv2.imread(file_path)

    except Exception:
        print(f"Error: can't open file '{file_path}'.")
        sys.exit(1)

if __name__ == "__main__":
    main()