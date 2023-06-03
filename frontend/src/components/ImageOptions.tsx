import type { FunctionComponent } from 'preact'
import SelectInput from './SelectInput'
import Options from '../utils/Options'
import { useCallback } from 'preact/hooks'
import useStore from '../hooks/useStore'

interface Props {
  className?: string
  onPreview: (imageRotation: string) => void
}

const imageSizingOptions = [
  { content: 'Crop', value: Options.imageSizing.crop },
  { content: 'Centre', value: Options.imageSizing.centre }
]

const imageRotationOptions = [
  { content: '0 degrees', value: Options.imageRotation[0] },
  { content: '90 degrees', value: Options.imageRotation[90] },
  { content: '180 degrees', value: Options.imageRotation[180] },
  { content: '270 degrees', value: Options.imageRotation[270] }
]

const ImageOptions: FunctionComponent<Props> = ({
  className = '',
  onPreview
}) => {
  const { store, setStore } = useStore()

  const onChangeImageRotation = useCallback((value: string) => {
    const newStore = {
      ...store,
      imageRotation: value as (typeof store)['imageRotation']
    }
    setStore(newStore)
    onPreview(value)
  }, [store, setStore, onPreview])

  return (
    <div className={`${className}`}>
      <SelectInput
        label="Image sizing"
        options={imageSizingOptions}
      />
      <SelectInput
        label="Image rotation"
        options={imageRotationOptions}
        onChange={onChangeImageRotation}
        value={store.imageRotation}
      />
    </div>
  )
}

export default ImageOptions
