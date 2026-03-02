# LED-Matrix-Visualizer

A microcontroller project, written in CircuitPython, designed to produce various visual effects based on audio input on an LED Matrix. This system utilizes real-time Fast Fourier Transform (FFT) to process ambient sound and map frequency data to dynamic visual patterns.

---

## Project Visuals

<details>
  <summary>Example 1</summary>
  <img src="https://github.com/4csullivan/LED-Matrix-Visualizer/blob/main/examples/EXAMPLE1.JPEG" style="height:500px">
</details>
<details>
  <summary>Example 2</summary>
  <img src="https://github.com/4csullivan/LED-Matrix-Visualizer/blob/main/examples/EXAMPLE2.JPEG" style="height:500px">
</details>
<details>
  <summary>Example 3</summary>
  <img src="https://github.com/4csullivan/LED-Matrix-Visualizer/blob/main/examples/EXAMPLE3.JPEG" style="height:500px">
</details>

---

## Features

* **Multiple designs** that have unique interactions with audio
* **Color gradients** to further visualize the audio effects
* **Button controls** to cycle through the designs and colors

---

## Hardware Components

* **Microcontroller:** Adafruit MatrixPortal M4 (SAMD51)
* **Display:** 2 x 64x32 RGB LED Matrices (Chained for 64x64 resolution)
* **Audio Input:** MAX9814 Electret Microphone Amplifier with Auto Gain Control (AGC)
* **Power:** 5V 4A DC Power Supply (Recommended for high-density LED driving)

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
