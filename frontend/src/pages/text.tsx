import { useCallback, useRef, useState } from 'preact/hooks'

const WIDTH = 800
const HEIGHT = 480

const convertToMONOVLSB = (buffer: Uint8ClampedArray): Uint8Array => {
  const newBuffer = new Uint8Array(WIDTH * HEIGHT / 8)
  // TODO
  return newBuffer
}

const TextPage = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [text, setText] = useState(``)

  const onChangeText = useCallback((event: Event) => {
    setText((event.target as HTMLInputElement).value)
  }, [])

  const onSubmit = useCallback(() => {
    if(canvasRef.current){
      const ctx = canvasRef.current.getContext("2d") as CanvasRenderingContext2D
      ctx.fillStyle = `white`
      ctx.fillRect(0, 0, WIDTH, HEIGHT)

      ctx.fillStyle = `black`
      ctx.font = "48px sans-serif"
      ctx.fillText(text, 10, 50)

      const imageData = ctx.getImageData(0, 0, WIDTH, HEIGHT);
      (async () => {
        try {
          const response = await fetch(`http://192.168.10.92/receive_data/}`, { method: 'POST', body: imageData.data })
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