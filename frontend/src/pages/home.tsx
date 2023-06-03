import type { FunctionComponent } from 'preact'
import PrimaryButton from '../components/PrimaryButton'
import { useCallback } from 'preact/hooks'
import Api from '../utils/Api'

const HomePage: FunctionComponent = () => {
  const onClear = useCallback(() => {
    void Api.clearImage()
  }, [])
  return (
    <>
      <h1 className="text-2xl font-black">eInk Screen</h1>
      <ul>
        <li>
          <a href="/text">Text</a>
        </li>
        <li>
          <a href="/toots">Toots</a>
        </li>
        <li>
          <a href="/image">Images</a>
        </li>
      </ul>
      <PrimaryButton onClick={onClear}>CLEAR</PrimaryButton>
    </>
  )
}

export default HomePage
