class LZWCompressor:
    """
    Lempel-Ziv-Welch (LZW) lossless data compression algorithm.
    """

    def compress(self, uncompressed: str) -> tuple[list[int], float]:
        """
        Compresses a string using LZW.
        Returns a tuple containing:
        1. A list of integer codes representing the compressed data.
        2. The compression ratio (compressed size / original size).
        """
        if not uncompressed:
            return [], 0.0

        # Validate that all characters are within the initial dictionary alphabet (0–255).
        # This algorithm operates on single-byte character values and does not support
        # arbitrary Unicode code points outside the Latin-1 range.
        for ch in uncompressed:
            if ord(ch) > 255:
                raise ValueError(
                    f"Unsupported character {ch!r} (code point {ord(ch)}). "
                    "LZWCompressor only supports characters with ord(c) <= 255."
                )

        # Initialize the dictionary with single character strings
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}

        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c

        # Output the code for remaining w.
        if w:
            result.append(dictionary[w])

        # Calculate a simple compression ratio estimate
        # Assuming original is UTF-8 encoded text
        # and compressed codes take 2 bytes (16-bit integers)
        original_size = len(uncompressed.encode("utf-8"))
        compressed_size = len(result) * 2
        ratio = compressed_size / original_size if original_size > 0 else 0

        return result, round(ratio, 2)

    def decompress(self, compressed: list[int]) -> str:
        """
        Decompresses a list of LZW integer codes back to the original string.
        """
        if not compressed:
            return ""

        # Initialize the dictionary with single character strings
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}

        w = chr(compressed[0])
        result = [w]

        for k in compressed[1:]:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError(f"Bad compressed code: {k}")

            result.append(entry)

            # Add w + entry[0] to the dictionary
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            w = entry

        return "".join(result)
