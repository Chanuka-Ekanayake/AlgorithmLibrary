# Algorithm Logic: LZW (Lempel-Ziv-Welch) Compression

## 1. The Core Objective

The goal of LZW compression is to reduce the size of data by finding repeated sequences of characters and replacing them with shorter, fixed-length integer codes. It is a completely **lossless** process.

---

## 2. Dynamic Dictionary Building

Unlike Huffman coding which requires a pre-computed frequency table, LZW is a **dictionary-based** algorithm that builds its dictionary *dynamically* "on the fly". 

* Both the compressor and the decompressor start with the exact same initial dictionary (usually the 256 standard ASCII characters).
* As data is processed, new sequences are added to the dictionary simultaneously on both ends.
* This means the dictionary itself does **not** need to be transmitted with the compressed data!

---

## 3. Compression Logic

The algorithm works sequentially:

1. **Initialize:** Start with a dictionary containing all possible single characters (codes 0-255).
2. **Track Current Match:** Use a string `w` to track the longest match found in the dictionary so far. Set `w` to empty.
3. **Iterate Input:** Read a character `c` from the input stream.
    * If `w + c` is in the dictionary, it means we have seen this sequence before. Update `w` to `w + c`.
    * If `w + c` is **not** in the dictionary, it means we found a *new* sequence.
        * Output the integer code for `w`.
        * Add the new sequence `w + c` to the dictionary and give it the next available code.
        * Reset `w` to just `c` (start building a new sequence).
4. **Finalize:** At the end of the input, output the code for whatever is left in `w`.

---

## 4. Decompression Logic

Decompression is remarkably clever because it rebuilds the exact same dictionary just by looking at the incoming codes.

1. **Initialize:** Start with the same standard dictionary of single characters (0-255).
2. **First Code:** Read the first integer code. It must be a standard character. Output it. Let's call this `w`.
3. **Iterate Codes:** Read the next code `k`.
    * If `k` is in the dictionary, output the string for `k` (let's call it `entry`).
    * **Edge Case:** If `k` is exactly equal to the next available dictionary code, it means the sequence is `w + w[0]` (the previous match plus its own first character).
    * Add `w + entry[0]` to the dictionary.
    * Update `w` to `entry`.

---

## 5. Industrial Application

In your 2026 software marketplace project, this logic is useful for:

* **Image Compression:** LZW is famously the underlying algorithm for the GIF image format.
* **Archive Formats:** The classic Unix `compress` tool (`.Z` files) uses LZW.
* **Document Compression:** Employed in formats like TIFF and early versions of PDF for highly repetitive data streams.
