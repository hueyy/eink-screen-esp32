const DITHER_THRESHOLD = 128

const WIDTH = 800
const HEIGHT = 480

const colourPalette: Colour[] = [
  [0, 0, 0],
  [255, 255, 255],
  [255, 0, 0],
]

const determineBit = (
  red: number,
  green: number,
  blue: number,
  alpha: number
): boolean => {
  // true is white
  // false is black
  if (alpha < 127) {
    return true
  } else if ((red + blue + green) / 3 > DITHER_THRESHOLD) {
    return true
  } else {
    return false
  }
}

const getAverageLuminosity = ([r, g, b]: Colour): number => (
  (r + g + b) / 3
)

const getNearest = (palette: Colour[], inputColour: Colour): number => {
  const distances = palette.map((p) => getColourDistance(p, inputColour))
  const lowest = Math.min(...distances)
  const index = distances.findIndex(d => lowest === d)
  return index
}

const isRed = (red: number, green: number, blue: number, threshold = 50): boolean => {
  return red >= (255 - threshold) && green <= threshold && blue <= threshold
}

const getColourDistance = ([r1, g1, b1]: Colour, [r2, g2, b2]: Colour): number => (
  Math.pow(r2 - r1, 2) + Math.pow(g2 - g1, 2) + Math.pow(b2 - b1, 2)
)

export const convertImageDataToMonoHLSB = (
  inputBuffer: Uint8ClampedArray,
  width: number,
  height: number
): Uint8Array => {
  // Buffer should contain a 1-dimensional array of integers from 0-255
  // in the RGBA format, representing pixels proceeding from left to
  // right and then downwards

  // Output should be in the MONO_HLSB format whereby bits in a byte are
  // horizontally mapped with bit 7 being the leftmost.
  // Subsequent bytes appear at successive horizontal locations until
  // the rightmost edge is reached. Further bytes are rendered on the
  // next row, one pixel lower.

  let currentByte = 0
  let byteIndex = 7

  const newByteBuffer = new Uint8Array(width * height / 8)
  for (let i = 0; i < inputBuffer.length; i += 4) {
    const red = inputBuffer[i]
    const green = inputBuffer[i + 1]
    const blue = inputBuffer[i + 2]
    const alpha = inputBuffer[i + 3]
    currentByte += determineBit(red, green, blue, alpha)
      ? 2 ** byteIndex
      : 0

    if (byteIndex === 0) {
      newByteBuffer[(i - 28) / 32] = currentByte // one iteration before 32
      currentByte = 0
      byteIndex = 7
    } else {
      byteIndex--
    }
  }

  return newByteBuffer
}

export const convertImageDataToMonoRedHLSB = (
  inputBuffer: Uint8ClampedArray,
  width: number,
  height: number
): Uint8Array => {
  // Buffer should contain a 1-dimensional array of integers from 0-255
  // in the RGBA format, representing pixels proceeding from left to
  // right and then downwards

  // Output should be in the MONO_HLSB format whereby bits in a byte are
  // horizontally mapped with bit 7 being the leftmost.
  // Subsequent bytes appear at successive horizontal locations until
  // the rightmost edge is reached. Further bytes are rendered on the
  // next row, one pixel lower.
  // Output contains the same image in concatenated black and red arrays

  let currentBlackByte = 0
  let currentRedByte = 0
  let byteIndex = 7

  const blackByteBuffer = new Uint8Array(width * height / 8)
  const redByteBuffer = new Uint8Array(width * height / 8)
  for (let i = 0; i < inputBuffer.length; i += 4) {
    const red = inputBuffer[i]
    const green = inputBuffer[i + 1]
    const blue = inputBuffer[i + 2]
    const alpha = inputBuffer[i + 3]

    if (isRed(red, green, blue, 40)) {
      currentRedByte += 0
      currentBlackByte += 2 ** byteIndex
    } else {
      currentRedByte += 2 ** byteIndex
      currentBlackByte += determineBit(red, green, blue, alpha)
        ? 2 ** byteIndex
        : 0
    }

    if (byteIndex === 0) {
      blackByteBuffer[(i - 28) / 32] = currentBlackByte // one iteration before 32
      redByteBuffer[(i - 28) / 32] = currentRedByte // one iteration before 32
      currentBlackByte = 0
      currentRedByte = 0
      byteIndex = 7
    } else {
      byteIndex--
    }
  }

  const result = new Uint8Array(blackByteBuffer.length + redByteBuffer.length)
  result.set(blackByteBuffer)
  result.set(redByteBuffer, blackByteBuffer.length)
  return result
}

export const ditherImageData = async (imageData: ImageData, ditherMode: Store['dithering']): Promise<ImageData> => {
  const { data, width } = imageData
  switch (ditherMode) {
    // TODO: Bill Atkinson dithering and Riemersma dithering?
    case 'none': {
      return imageData
    }
    case 'binary': {
      for (let currentPixel = 0; currentPixel <= data.length; currentPixel += 4) {
        const averageLuminosity = (data[currentPixel] + data[currentPixel + 1] + data[currentPixel + 2]) / 3
        data[currentPixel] = averageLuminosity < DITHER_THRESHOLD ? 0 : 255
        data[currentPixel + 1] = data[currentPixel]
        data[currentPixel + 2] = data[currentPixel]
      }
      return imageData
    }
    case 'ternary': {
      for (let currentPixel = 0; currentPixel <= data.length; currentPixel += 4) {
        if (isRed(data[currentPixel], data[currentPixel + 1], data[currentPixel + 2])) {
          data[currentPixel] = 255
          data[currentPixel + 1] = data[currentPixel + 2] = 0
        } else {
          const averageLuminosity = (data[currentPixel] + data[currentPixel + 1] + data[currentPixel + 2]) / 3
          data[currentPixel] = averageLuminosity < DITHER_THRESHOLD ? 0 : 255
          data[currentPixel + 1] = data[currentPixel]
          data[currentPixel + 2] = data[currentPixel]
        }
      }
      return imageData
    }
    case 'floydSteinberg': {
      for (let currentPixel = 0; currentPixel < data.length; currentPixel += 4) {
        const averageLuminosity = getAverageLuminosity([
          data[currentPixel],
          data[currentPixel + 1],
          data[currentPixel + 2]
        ])
        if (averageLuminosity < 240 && averageLuminosity > 20) {
          const newPixel = data[currentPixel] < DITHER_THRESHOLD ? 0 : 255
          const err = Math.floor((data[currentPixel] - newPixel) / 16)
          imageData.data[currentPixel] = newPixel
          imageData.data[currentPixel + 4] += err * 7
          imageData.data[currentPixel + 4 * width - 4] += err * 3
          imageData.data[currentPixel + 4 * width] += err * 5
          imageData.data[currentPixel + 4 * width + 4] += err * 1
          imageData.data[currentPixel + 1] = data[currentPixel]
          imageData.data[currentPixel + 2] = data[currentPixel]
        }
      }
      return imageData
    }
    case 'floydSteinbergRed': {
      for (let currentPixel = 0; currentPixel < data.length; currentPixel += 4) {

        const nearestColourIndex = getNearest(
          colourPalette,
          [data[currentPixel], data[currentPixel + 1], data[currentPixel + 2]]
        )
        const newColour = colourPalette[nearestColourIndex]

        const quantError: Colour = [
          data[currentPixel] - newColour[0],
          data[currentPixel + 1] - newColour[1],
          data[currentPixel + 2] - newColour[2]
        ]

        imageData.data[currentPixel] = newColour[0]
        imageData.data[currentPixel + 1] = newColour[1]
        imageData.data[currentPixel + 2] = newColour[2]

        const x = (currentPixel / 4) % WIDTH;
        const y = Math.floor((currentPixel / 4) / WIDTH);

        for (let [DX, DY, fraction] of [
          [1, 0, 7 / 16],
          [-1, 1, 3 / 16],
          [0, 1, 5 / 16],
          [1, 1, 1 / 16],
        ]) {
          const x1 = x + DX
          const y1 = y + DY
          if (x1 >= 0 && x1 < WIDTH && y1 >= 0 && y1 < HEIGHT) {
            const index1 = 4 * (x1 + y1 * WIDTH);
            for (let i = 0; i < 3; i++) {
              imageData.data[index1 + i] += quantError[i] * fraction
            }
          }
        }
      }
      return imageData
    }
    default: {
      return imageData
    }
  }
}
