import { useCallback, useEffect, useRef, useState } from 'preact/hooks'
import { convertImageDataToMonoRedHLSB, ditherImageData } from '../utils/Utils'
import Api from '../utils/Api'
import type { FunctionComponent } from 'preact'
import PrimaryButton from '../components/PrimaryButton'
import ImageOptions from '../components/ImageOptions'
import type Storage from '../utils/Storage'
import useStore from '../hooks/useStore'
import Container from '../components/Container'
import Header from '../components/Header'

const WIDTH = 800
const HEIGHT = 480

const ImagePage: FunctionComponent = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [currentImage, setImage] = useState<string>()

  const { store, getStore } = useStore()

  const onPreview = useCallback((inputStore?: typeof Storage.defaultStore) => {
    const currentStore = (typeof inputStore === 'undefined') ? getStore() : inputStore
    if (currentImage != null) {
      const image = new Image()
      image.src = currentImage

      image.onload = async () => {
        if (canvasRef.current != null) {
          const ctx = canvasRef.current.getContext('2d') as CanvasRenderingContext2D
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
          ctx.fillStyle = 'white'
          ctx.fillRect(0, 0, WIDTH, HEIGHT)
          ctx.save()

          ctx.translate(ctx.canvas.width / 2, ctx.canvas.height / 2)
          const rotation = Number.parseInt(currentStore.imageRotation, 10)
          ctx.rotate(rotation * Math.PI / 180)

          let ratio = Math.min(ctx.canvas.width / image.width, ctx.canvas.height / image.height)
          switch (currentStore.imageSizing) {
            case `fullHeight`: {
              ratio = ctx.canvas.height / image.height
              break
            }

            case 'fullWidth': {
              ratio = ctx.canvas.width / image.width
              break
            }

            default: {
              break
            }
          }
          const offsetX = Math.round((ctx.canvas.width - image.width * ratio) / 2) - ctx.canvas.width / 2
          const offsetY = Math.round((ctx.canvas.height - image.height * ratio) / 2) - ctx.canvas.height / 2

          ctx.drawImage(
            image,
            0,
            0,
            image.width,
            image.height,
            offsetX,
            offsetY,
            image.width * ratio,
            image.height * ratio
          )
          ctx.restore()

          const rawImageData = ctx.getImageData(0, 0, WIDTH, HEIGHT)
          const ditheredImageData = await ditherImageData(rawImageData, currentStore.dithering)
          ctx.putImageData(ditheredImageData, 0, 0)
        }
      }
    }
  }, [currentImage, getStore])

  const onChangeFile = useCallback((event: Event) => {
    if (((event.target as HTMLInputElement).files != null) &&
      ((event.target as HTMLInputElement).files as FileList).length === 1) {
      const file = ((event.target as HTMLInputElement).files as FileList)[0]
      const blobURL = URL.createObjectURL(file)
      setImage(blobURL)
    }
  }, [])

  useEffect(() => { onPreview() }, [onPreview, currentImage])

  const onSubmit = useCallback(() => {
    if (canvasRef.current != null) {
      const ctx = canvasRef.current.getContext('2d') as CanvasRenderingContext2D
      const rawImageData = ctx.getImageData(0, 0, WIDTH, HEIGHT)
      const imageData = convertImageDataToMonoRedHLSB(rawImageData.data, WIDTH, HEIGHT)
      void Api.postImageData(store.host, imageData)
    }
  }, [store])

  return (
    <Container>
      <Header backButton>
        Image
      </Header>

      <div className="py-6 px-2 flex flex-col items-start">
        <input
          className="mb-4"
          type="file"
          onChange={onChangeFile}
          accept="image/*"
        ></input>

        <ImageOptions className="pb-6" onPreview={onPreview} />

        <PrimaryButton onClick={onSubmit}>SUBMIT</PrimaryButton>
      </div>

      <canvas
        id="preview"
        className="border border-black w-full max-w-full mx-auto"
        width={WIDTH} height={HEIGHT}
        ref={canvasRef}>
      </canvas>
    </Container>
  )
}

export default ImagePage
