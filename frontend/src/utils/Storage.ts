import Options from './Options'

const STORE_KEY = 'store'

const defaultStore: Store = {
  imageSizing: Options.imageSizing.fullWidth,
  imageRotation: Options.imageRotation[0],
  dithering: Options.dithering.ternary,
  wifi: [],
  host: 'http://192.168.10.92'
}

const set = (newStore: Store): void => {
  localStorage.setItem(STORE_KEY, JSON.stringify(newStore))
}

const get = (): Store => {
  const store = localStorage.getItem(STORE_KEY)
  if (store === null) {
    return defaultStore
  }
  try {
    return JSON.parse(store)
  } catch (error) {
    console.error(error)
    return defaultStore
  }
}

const Storage = {
  defaultStore,
  set,
  get
}

export default Storage
