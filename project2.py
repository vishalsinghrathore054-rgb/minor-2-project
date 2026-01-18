import struct
import math

# Function 1: Logic to decide which character to use based on brightness
def get_char_for_pixel(brightness):
    """
    Determines the character based on brightness levels.
    """
    if brightness < 25: return "@"
    elif brightness < 50: return "#"
    elif brightness < 75: return "8"
    elif brightness < 100: return "&"
    elif brightness < 125: return "o"
    elif brightness < 150: return ":"
    elif brightness < 175: return "*"
    elif brightness < 200: return "."
    else: return " "

def main():
    filename = "devdutt.bmp"
    new_width = 100

    try:
        with open(filename, "rb") as f:
            # --- HEADER PARSING ---
            # BMP files have a header. We need to skip the first 10 bytes, 
            # then read the location of the pixel data.
            header_field = f.read(2)
            if header_field != b'BM':
                print("Error: File is not a valid BMP.")
                return

            f.seek(10)
            # unpack reads binary data. 'I' means unsigned int (4 bytes)
            pixel_data_start = struct.unpack('<I', f.read(4))[0]

            f.seek(18)
            # Read width and height (signed integers 'i')
            width = struct.unpack('<i', f.read(4))[0]
            height = struct.unpack('<i', f.read(4))[0]
            
            # --- RESIZING LOGIC ---
            aspect_ratio = height / width
            # Terminal characters are taller than wide, so we correct by 0.55
            new_height = int(aspect_ratio * new_width * 0.55)
            
            print(f"Original: {width}x{height} -> ASCII: {new_width}x{new_height}")

            # Calculate padding
            # In BMP, every row must be a multiple of 4 bytes. 
            # If width*3 is not divisible by 4, bytes are added to the end of the row.
            row_padding = (4 - (width * 3) % 4) % 4
            row_size = (width * 3) + row_padding

            ascii_image = ""

            # --- PIXEL EXTRACTION LOOP ---
            # We loop through the TARGET (resized) dimensions
            for y in range(new_height):
                for x in range(new_width):
                    
                    # NEAREST NEIGHBOR INTERPOLATION
                    # We calculate which pixel from the original image corresponds 
                    # to the current pixel in the tiny ASCII version.
                    src_x = int(x * (width / new_width))
                    src_y = int(y * (height / new_height))

                    # BMPs store images upside down (bottom to top). 
                    # We flip the Y-axis to read it correctly.
                    actual_y = height - 1 - src_y

                    # Calculate exact byte position in the file
                    # Position = Start + (Row Number * Bytes per Row) + (Column * 3 bytes for RGB)
                    position = pixel_data_start + (actual_y * row_size) + (src_x * 3)
                    
                    f.seek(position)
                    pixel = f.read(3) # Read 3 bytes: Blue, Green, Red

                    if len(pixel) == 3:
                        # BMP stores colors as BGR, not RGB
                        b = pixel[0]
                        g = pixel[1]
                        r = pixel[2]

                        # Standard grayscale formula
                        # Weights: Red 30%, Green 59%, Blue 11% (approx human eye perception)
                        brightness = int(0.299*r + 0.587*g + 0.114*b)
                        
                        ascii_image += get_char_for_pixel(brightness)
                    
                ascii_image += "\n"

        # --- OUTPUT ---
        print(ascii_image)

        with open("devdutt_ascii_art.txt", "w") as out_f:
            out_f.write(ascii_image)
        print("Project completed! Saved to devdutt_ascii_art.txt")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Make sure you saved it as a .bmp file!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()