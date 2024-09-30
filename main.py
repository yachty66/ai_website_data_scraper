import screenshots
import data_extractor

def main():
    # Hardcoded URL
    url = "https://ishosting.com"  # Replace with your desired URL
    
    # Step 1: Capture screenshots
    print("Capturing screenshots...")
    screenshots.main(url)

    # Step 2: Extract data from screenshots
    print("Extracting data from screenshots...")
    data_extractor.extract_data_from_screenshots("screenshots")

if __name__ == "__main__":
    main()