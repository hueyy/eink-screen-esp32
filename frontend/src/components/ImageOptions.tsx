import type { FunctionComponent } from 'preact'
import SelectInput from './SelectInput'
import Options from '../utils/Options'
import { useCallback } from 'preact/hooks'
import useStore from '../hooks/useStore'
import type Storage from '../utils/Storage'

interface Props {
  className?: string
  onPreview: (inputStore?: typeof Storage.defaultStore) => void
}

// const imageSizingOptions = [
//   { content: 'Full width', value: Options.imageSizing.fullWidth },
//   { content: 'Full height', value: Options.imageSizing.fullHeight }
// ]

const imageRotationOptions = [
  { content: '0 degrees', value: Options.imageRotation[0] },
  { content: '90 degrees', value: Options.imageRotation[90] },
  { content: '180 degrees', value: Options.imageRotation[180] },
  { content: '270 degrees', value: Options.imageRotation[270] }
]

const ditheringOptions = [
  { content: 'Binary (i.e. colour reduction only)', value: Options.dithering.binary },
  { content: 'Ternary (including red)', value: Options.dithering.ternary },
  { content: 'Floyd-Steinberg', value: Options.dithering.floydSteinberg },
  { content: 'Floyd-Steinberg (with red)', value: Options.dithering.floydSteinbergRed }
]

const ImageOptions: FunctionComponent<Props> = ({
  className = '',
  onPreview
}) => {
  const { store, setStore } = useStore()

  // const onChangeImageSizing = useCallback((value: string) => {
  //   const newStore: typeof store = {
  //     ...store,
  //     imageSizing: value as (typeof store)['imageSizing']
  //   }
  //   setStore(newStore)
  //   onPreview(newStore)
  // }, [store, setStore, onPreview])

  const onChangeImageRotation = useCallback((value: string) => {
    const newStore: typeof store = {
      ...store,
      imageRotation: value as Store['imageRotation']
    }
    setStore(newStore)
    onPreview(newStore)
  }, [store, setStore, onPreview])

  const onChangeDithering = useCallback((value: string) => {
    const newStore = {
      ...store,
      dithering: value as Store['dithering']
    }
    setStore(newStore)
    onPreview(newStore)
  }, [store, setStore, onPreview])

  return (
    <div className={`${className}`}>
      {/* <SelectInput
        label="Image sizing"
        options={imageSizingOptions}
        onChange={onChangeImageSizing}
        value={store.imageSizing}
      /> */}
      <SelectInput
        label="Image rotation"
        options={imageRotationOptions}
        onChange={onChangeImageRotation}
        value={store.imageRotation}
      />
      <SelectInput
        label="Dithering"
        options={ditheringOptions}
        onChange={onChangeDithering}
        value={store.dithering}
      />
    </div>
  )
}

export default ImageOptions
