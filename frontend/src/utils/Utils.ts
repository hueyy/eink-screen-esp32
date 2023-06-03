const DITHER_THRESHOLD = 128

const determineBit = (
  red: number,
  green: number,
  blue: number,
  alpha: number
): boolean => {
  if (alpha < 127) {
    return true
  } else if ((red + blue + green) / 3 > DITHER_THRESHOLD) {
    return true
  } else {
    return false
  }
}

// NOT TESTED
export const convertImageDataToMonoVLSB = (
  buffer: Uint8ClampedArray,
  width: number,
  height: number
): Uint8Array => {
  // Buffer should contain a 1-dimensional array of integers from 0-255
  // in the RGBA format, representing pixels proceeding from left to
  // right and then downwards

  // Output should be in the MONO_VLSB format whereby bits in a byte are
  // vertically mapped with bit 0 being nearest the top of the screen.
  // Consequently each byte occupies 8 vertical pixels. Subsequent bytes
  // appear at successive horizontal locations until the rightmost edge
  // is reached. Further bytes are rendered at locations starting at the
  // leftmost edge, 8 pixels lower.

  const newByteBuffer = new Uint8Array(width * height / 8)
  const newBitBuffer = new Uint8Array(width * height)

  for (let i = 0; i < buffer.length; i += 4) {
    const red = buffer[i]
    const green = buffer[i + 1]
    const blue = buffer[i + 2]
    const alpha = buffer[i + 3]
    const outputBit = determineBit(red, green, blue, alpha)
    newBitBuffer[i / 4] = outputBit ? 1 : 0
  }

  for (let i = 0; i < newByteBuffer.length; i++) {
    let bitString = ''
    for (let j = 0; j < 8; j++) {
      bitString = bitString.concat(`${newBitBuffer[i % width + (width * j) + width * 8 * Math.floor(i / width)]}`)
    }
    const byte = Number.parseInt(bitString, 2)
    newByteBuffer[i] = byte
  }

  return newByteBuffer
}

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
