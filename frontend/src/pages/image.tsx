import { useCallback, useRef } from 'preact/hooks'
import { convertImageDataToMonoHLSB } from '../utils/Utils'
import Api from '../utils/Api'
import type { FunctionComponent } from 'preact'
import PrimaryButton from '../components/PrimaryButton'
import ImageOptions from '../components/ImageOptions'

const WIDTH = 800
const HEIGHT = 480

const ImagePage: FunctionComponent = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  // const [currentImage, setImage] = useState<HTMLImageElement>()
  const onChangeFile = useCallback((event: Event) => {
    if (((event.target as HTMLInputElement).files != null) &&
      ((event.target as HTMLInputElement).files as FileList).length === 1) {
      const file = ((event.target as HTMLInputElement).files as FileList)[0]
      const blobURL = URL.createObjectURL(file)
      const image = new Image()
      image.src = blobURL
      // setImage(image)

      image.onload = () => {
        URL.revokeObjectURL(image.src)
        if (canvasRef.current != null) {
          const ctx = canvasRef.current.getContext('2d') as CanvasRenderingContext2D
          ctx.fillStyle = 'white'
          ctx.fillRect(0, 0, WIDTH, HEIGHT)
          ctx.drawImage(image, 0, 0)
        }
      }
    }
  }, [])

  const onSubmit = useCallback(() => {
    if (canvasRef.current != null) {
      const ctx = canvasRef.current.getContext('2d') as CanvasRenderingContext2D
      const rawImageData = ctx.getImageData(0, 0, WIDTH, HEIGHT).data
      const imageData = convertImageDataToMonoHLSB(rawImageData, WIDTH, HEIGHT)
      void Api.postImageData(imageData)
    }
  }, [])

  return (
    <>
      <div className="py-4 px-2">
        <h1 className="text-3xl">Image</h1>
      </div>

      <div className="py-6 px-2 flex flex-col items-start">
        <input
          className="mb-4"
          type="file"
          onChange={onChangeFile}
          accept="image/*"
        ></input>

        <ImageOptions />

        <PrimaryButton onClick={onSubmit}>SUBMIT</PrimaryButton>
      </div>

      <canvas
        id="preview"
        className="border border-black mx-2"
        width={WIDTH} height={HEIGHT}
        ref={canvasRef}>
      </canvas>
    </>
  )
}

export default ImagePage
