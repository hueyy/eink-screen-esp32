import { useCallback, useEffect, useState } from 'preact/hooks'
import Storage from '../utils/Storage'

const useStore = () => {
  const [store, setStoreInState] = useState(Storage.defaultStore)

  useEffect(() => {
    const retrieveStore = Storage.get()
    setStoreInState(retrieveStore)
  }, [])

  const setStore = useCallback((newStore: typeof Storage.defaultStore) => {
    setStoreInState(newStore)
    Storage.set(newStore)
  }, [])

  return { store, setStore } as const
}

export default useStore
