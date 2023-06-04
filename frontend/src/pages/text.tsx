import { useCallback, useRef, useState } from 'preact/hooks'
import { convertImageDataToMonoHLSB } from '../utils/Utils'
import Api from '../utils/Api'
import type { FunctionComponent } from 'preact'
import Container from '../components/Container'
import Header from '../components/Header'
import PrimaryButton from '../components/PrimaryButton'

const WIDTH = 800
const HEIGHT = 480

const TextPage: FunctionComponent = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [text, setText] = useState('')

  const onChangeText = useCallback((event: Event) => {
    setText((event.target as HTMLInputElement).value)
  }, [])

  const onPreview = useCallback(() => {
    if (canvasRef.current != null) {
      const ctx = canvasRef.current.getContext('2d') as CanvasRenderingContext2D
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, WIDTH, HEIGHT)

      ctx.fillStyle = 'black'
      ctx.font = '72px sans-serif'
      ctx.fillText(text, 10, 80)

      return ctx
    }
  }, [text])

  const onSubmit = useCallback(() => {
    const ctx = onPreview()
    if (ctx != null) {
      const rawImageData = ctx.getImageData(0, 0, WIDTH, HEIGHT).data
      const imageData = convertImageDataToMonoHLSB(rawImageData, WIDTH, HEIGHT)
      void Api.postImageData(imageData)
    }
  }, [onPreview])

  return (
    <Container>
      <Header backButton>Text</Header>
      <div className="flex flex-col items-start py-6 px-2">
        <input
          className="my-4 px-4 py-2 border border-neutral-500"
          type="text"
          placeholder="Enter string..."
          value={text}
          onChange={onChangeText}
        ></input>
        <PrimaryButton onClick={onSubmit}>SUBMIT</PrimaryButton>
      </div>

      <canvas
        className="border border-black w-full max-w-full mx-auto"
        id="preview"
        width={WIDTH}
        height={HEIGHT}
        ref={canvasRef}
      ></canvas>
    </Container>
  )
}

export default TextPage
