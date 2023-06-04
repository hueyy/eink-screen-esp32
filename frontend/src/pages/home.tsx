import type { FunctionComponent } from 'preact'
import PrimaryButton from '../components/PrimaryButton'
import { useCallback } from 'preact/hooks'
import Api from '../utils/Api'
import Container from '../components/Container'
import useStore from '../hooks/useStore'
import Header from '../components/Header'

interface LinkProps {
  text: string
  href: string
}

const Link: FunctionComponent<LinkProps> = ({ text, href }) => {
  return (
    <a className="bg-slate-200 px-4 py-2" href={href}>
      {text}
    </a>
  )
}

const HomePage: FunctionComponent = () => {
  const { store, setStore } = useStore()
  const onClear = useCallback(() => {
    void Api.clearImage()
  }, [])

  const onClickHost = useCallback(() => {
    const newHost = window.prompt('New host?', store.host)
    if (newHost !== null) {
      setStore({
        ...store,
        host: newHost
      })
    }
  }, [store, setStore])

  return (
    <Container>
      <Header>eInk Screen</Header>
      <div className="bg-neutral-200 px-4 py-2 my-6 select-none cursor-pointer" onClick={onClickHost}>
        <label className="font-semibold">
          Host:&nbsp;
        </label>
        <span>
          {store.host}
        </span>
      </div>
      <div className="flex flex-col gap-4 my-6">
        <Link href="/text" text={'Text'} />
        <Link href="/image" text={'Images'} />
        {/* <Link href="/toots" text={'Toots'} /> */}
      </div>
      <PrimaryButton onClick={onClear}>CLEAR</PrimaryButton>
    </Container>
  )
}

export default HomePage
