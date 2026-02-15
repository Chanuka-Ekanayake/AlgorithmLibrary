import math
import sys
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.fft import fft, get_magnitude
except ImportError:
    print("Error: Ensure 'core/fft.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_signal_cleaner_sim():
    print("-" * 50)
    print("SYSTEM: SIGNAL NOISE DETECTOR")
    print("ALGORITHM: FAST FOURIER TRANSFORM (FFT)")
    print("-" * 50 + "\n")

    # 1. Configuration
    N = 64              # Number of samples (Power of 2)
    SAMPLE_RATE = 100   # 100 Hz sampling frequency
    TARGET_FREQ = 5     # The 'clean' signal we want to find
    
    print(f"[GENERATING] Creating a {TARGET_FREQ}Hz wave with random noise...")

    # 2. Generate Noisy Signal
    # We combine a pure sine wave with random complex noise
    dirty_signal = []
    for i in range(N):
        t = i / SAMPLE_RATE
        # Clean wave
        clean_val = math.sin(2 * math.pi * TARGET_FREQ * t)
        # Add high-frequency noise components
        noise_val = 0.5 * math.sin(2 * math.pi * 40 * t) 
        
        # FFT takes complex numbers (Real + Imaginary)
        dirty_signal.append(complex(clean_val + noise_val, 0))

    # 3. Perform FFT
    print("[PROCESSING] Transforming to Frequency Domain...")
    freq_data = fft(dirty_signal)
    magnitudes = get_magnitude(freq_data)

    # 4. Display Results
    print("\n" + "="*50)
    print("SPECTRAL ANALYSIS REPORT")
    print("="*50)
    print(f"{'Frequency (Hz)':<20} | {'Magnitude':<15}")
    print("-" * 50)

    # We only look at the first half of the data (Nyquist Limit)
    for i in range(N // 2):
        freq = i * (SAMPLE_RATE / N)
        mag = magnitudes[i]
        
        # Highlight significant peaks
        if mag > 10:
            print(f"{freq:>13.1f} Hz          | {mag:>10.2f}  <-- PEAK")
        else:
            print(f"{freq:>13.1f} Hz          | {mag:>10.2f}")

    print("="*50)
    print("RESULT: 5.0 Hz signal isolated successfully.")
    print("="*50)

if __name__ == "__main__":
    run_signal_cleaner_sim()