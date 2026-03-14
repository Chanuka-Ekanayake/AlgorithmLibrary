# LZW Compressor Test Project

This simple test project demonstrates how LZW dictionary-based compression works on repetitive text data.

## Running the Demo

1. Open your terminal.
2. Navigate to this directory (`test-project`).
3. Run the application:
```bash
python app.py
```

## What to Expect

The application will read `sample_data.txt`, compress it into a list of integer codes, calculate a compression ratio estimate, and then immediately decompress it back to the original text. You will see a `SUCCESS` message confirming that LZW is perfectly lossless. Try modifying `sample_data.txt` with more repetitive text (like "ABABABABBB") to see the compression ratio improve!
