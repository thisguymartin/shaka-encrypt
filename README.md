# Content Packaging and Encryption System

## Description
This project automates the process of packaging video and audio files for streaming (using DASH) and optionally encrypts the content using Nagra Solutions. It utilizes Shaka Packager for media packaging and supports dynamic encryption of content.

## Requirements
- Python 3
- httplib2
- Shaka Packager installed and accessible at `~/bin/packager-linux`
- Access to Nagra Solutions API

## Setup
1. Ensure Python 3 and all required libraries (httplib2, xml.etree.ElementTree) are installed.
2. Place the script in a suitable directory.
3. Ensure Shaka Packager (`packager-linux`) is installed and located in `~/bin`.

## Usage
Run the script with the following command:
```bash
python3 [script_name].py
```

### Steps:
1. **Input Video and Audio Files**: Enter the names of the video and audio files you want to package, including the file format (e.g., `.mp4`).
2. **Encryption Decision**: Choose whether to encrypt the content. If yes, you will be prompted to enter a content key.
3. **Content Packaging**: The script will package the content into DASH format, saving the results in the `chunked_content` directory.
4. **Encryption (Optional)**: If encryption is chosen, the script will encrypt the content using the provided content key and save the encrypted files in the `encrypted_content` directory.

### Output
- Packaged content in `chunked_content` or `encrypted_content` directory.
- An MPD (Media Presentation Description) file for streaming.
- Encryption details saved in `encrypt_details.txt` (if encryption is chosen).

## Additional Notes
- Ensure proper permissions for the script and output directories (`chmod 777` is used in the script).
- For further assistance with Shaka Packager, refer to the official [Shaka Packager Documentation](https://github.com/google/shaka-packager).
- The `myCinema Portal` link is provided for managing content keys.

---

Make sure to replace `[script_name]` with the actual name of your script. Also, consider adding more information about the configuration and any prerequisites needed, such as API keys or specific environment setups.
