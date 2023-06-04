const DITHER_THRESHOLD = 128

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

// NOT TESTED
// export const convertImageDataToMonoVLSB = (
//   buffer: Uint8ClampedArray,
//   width: number,
//   height: number
// ): Uint8Array => {
//   // Buffer should contain a 1-dimensional array of integers from 0-255
//   // in the RGBA format, representing pixels proceeding from left to
//   // right and then downwards

//   // Output should be in the MONO_VLSB format whereby bits in a byte are
//   // vertically mapped with bit 0 being nearest the top of the screen.
//   // Consequently each byte occupies 8 vertical pixels. Subsequent bytes
//   // appear at successive horizontal locations until the rightmost edge
//   // is reached. Further bytes are rendered at locations starting at the
//   // leftmost edge, 8 pixels lower.

//   const newByteBuffer = new Uint8Array(width * height / 8)
//   const newBitBuffer = new Uint8Array(width * height)

//   for (let i = 0; i < buffer.length; i += 4) {
//     const red = buffer[i]
//     const green = buffer[i + 1]
//     const blue = buffer[i + 2]
//     const alpha = buffer[i + 3]
//     const outputBit = determineBit(red, green, blue, alpha)
//     newBitBuffer[i / 4] = outputBit ? 1 : 0
//   }

//   for (let i = 0; i < newByteBuffer.length; i++) {
//     let bitString = ''
//     for (let j = 0; j < 8; j++) {
//       bitString = bitString.concat(`${newBitBuffer[i % width + (width * j) + width * 8 * Math.floor(i / width)]}`)
//     }
//     const byte = Number.parseInt(bitString, 2)
//     newByteBuffer[i] = byte
//   }

//   return newByteBuffer
// }

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

    const isRed = red > 230 && green < 30 && blue < 30

    if (isRed) {
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

export const ditherImageData = (imageData: ImageData, ditherMode: Store['dithering']): ImageData => {
  const { data, width } = imageData
  switch (ditherMode) {
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
        if (data[currentPixel] > 250 && data[currentPixel + 1] < 10 && data[currentPixel + 2] < 10) {
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
      for (let currentPixel = 0; currentPixel <= data.length; currentPixel += 4) {
        const averageLuminosity = (data[currentPixel] + data[currentPixel + 1] + data[currentPixel + 2]) / 3
        if (averageLuminosity < 240 && averageLuminosity > 20) {
          const newPixel = imageData.data[currentPixel] < DITHER_THRESHOLD ? 0 : 255
          const err = Math.floor((imageData.data[currentPixel] - newPixel) / 16)
          imageData.data[currentPixel] = newPixel
          imageData.data[currentPixel + 4] += err * 7
          imageData.data[currentPixel + 4 * width - 4] += err * 3
          imageData.data[currentPixel + 4 * width] += err * 5
          imageData.data[currentPixel + 4 * width + 4] += err * 1
          data[currentPixel + 1] = data[currentPixel]
          data[currentPixel + 2] = data[currentPixel]
        }
      }
      return imageData
    }
    case 'floydStenbergRed': {
      return imageData
    }
    default: {
      return imageData
    }
  }
}
