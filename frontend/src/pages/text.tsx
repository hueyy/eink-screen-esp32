import { useCallback, useRef, useState } from 'preact/hooks'

const WIDTH = 800
const HEIGHT = 480

// const convertToMONOVLSB = (buffer: Uint8ClampedArray): Uint8Array => {
//   const newBuffer = new Uint8Array(WIDTH * HEIGHT / 8)
//   for(let i = 0; i < buffer.length; i += 4){
//     const red = buffer[i]
//     const green = buffer[i+1]
//     const blue = buffer[i+2]
//     const alpha = buffer[i+3]

//     const pixelIndex = i / 4
//     const bitIndex = pixelIndex % 8
//     const byteIndex = Math.floor(pixelIndex / 8)

//     if(alpha < 127){
//       // assume white
//       newBuffer[byteIndex] |= (0x80 >>> bitIndex)
//     } else if(red === 255 && green === 255 && blue === 255){
//       newBuffer[byteIndex] |= (0x80 >>> bitIndex)
//     } else if(red === 0 && green === 0 && blue === 0){
//       newBuffer[byteIndex] &= ~(0x80 >>> bitIndex)
//     }
//   }
//   return newBuffer
// }

// const convertToMONOVLSB = (buffer: Uint8ClampedArray): Uint8Array => {
//   const data = new Uint8Array(Math.ceil(WIDTH * HEIGHT / 8));

//   for (let y = 0; y < HEIGHT; y += 8) {
//     for (let x = 0; x < WIDTH; x++) {
//       let currentByte = 0
//       for (let yOffset = 0; yOffset < 8; yOffset++) {
//         const pixelIndex = ((y + yOffset) * WIDTH + x) * 4
//         const rgbaValue = buffer[pixelIndex]
//         const redValue = rgbaValue & 0xff
//         currentByte |= (redValue >> 7 - yOffset) << yOffset
//       }
//       data[y / 8 * WIDTH + x] = currentByte
//     }
//   }

//   return data
// }



const TextPage = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [text, setText] = useState(``)

  const onChangeText = useCallback((event: Event) => {
    setText((event.target as HTMLInputElement).value)
  }, [])

  const onSubmit = useCallback(() => {
    if(canvasRef.current){
      const ctx = canvasRef.current.getContext("2d") as CanvasRenderingContext2D
      ctx.fillStyle = `black`
      ctx.fillRect(0, 0, WIDTH, HEIGHT)

      ctx.fillStyle = `white`
      ctx.font = "48px sans-serif"
      ctx.fillText(text, 10, 50)

      const imageData = convertToMONOVLSB(ctx.getImageData(0, 0, WIDTH, HEIGHT).data);
      console.log(imageData);
      (async () => {
        try {
          const response = await fetch(`http://192.168.10.92/receive_data/`, { method: 'POST', body: imageData })
          console.log(await response.json())
        } catch (error) {
          console.error(error)
          throw error
        }
      })()
    }
  }, [text])

  return (
    <>
      <h1>Text</h1>
      <input type="text" placeholder="Enter string..." value={text} onChange={onChangeText}></input>
      <button type="button" onClick={onSubmit}>SUBMIT</button>

      <canvas id="preview" width={WIDTH} height={HEIGHT} ref={canvasRef} style="border: 1px solid black;"></canvas>
    </>
  )
}

export default TextPage