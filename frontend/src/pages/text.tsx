import { useCallback, useRef, useState } from 'preact/hooks'

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
      ctx.fillRect(0, 0, 800, 480)

      ctx.fillStyle = `black`
      ctx.font = "48px sans-serif"
      ctx.fillText(text, 10, 50)

      const imageData = ctx.getImageData(0, 0, 800, 480)
      const parts = 100
      const partLength = imageData.data.length / parts
      console.log(partLength);
      (async () => {
        for(let i = 0; i < parts; i++){
          try {
            const response = await fetch(`http://192.168.10.92/api/?block_number=${i}`, { method: 'POST', body: imageData.data.slice(i * partLength, (i + 1) * partLength) })
            console.log(await response.json())
          } catch (error) {
            console.error(error)
            throw error
          }
        }
      })()
      
    }
  }, [text])

  return (
    <>
      <h1>Text</h1>
      <input type="text" placeholder="Enter string..." value={text} onChange={onChangeText}></input>
      <button type="button" onClick={onSubmit}>SUBMIT</button>

      <canvas id="preview" width="800" height="480" ref={canvasRef} style="border: 1px solid black;"></canvas>
    </>
  )
}

export default TextPage