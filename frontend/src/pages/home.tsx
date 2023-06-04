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
  const onClear = useCallback(async () => {
    try {
      const response = await Api.clearImage(store.host)
      window.alert(JSON.stringify(response))
    } catch (error) {
      console.error(error)
    }
  }, [store])

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
      <div className="bg-neutral-200 px-4 py-2 my-6 select-none cursor-pointer mx-2" onClick={onClickHost}>
        <label className="font-semibold">
          Host:&nbsp;
        </label>
        <span>
          {store.host}
        </span>
      </div>
      <div className="flex flex-col gap-4 my-6 mx-2">
        <Link href="/text" text={'Text'} />
        <Link href="/image" text={'Images'} />
        {/* <Link href="/toots" text={'Toots'} /> */}
      </div>
      <PrimaryButton onClick={onClear} className="mx-2">CLEAR</PrimaryButton>
      <div className="mx-auto text-center my-6">
        <a href="https://github.com/hueyy/eink-screen" className="text-neutral-500">
          source code
        </a>
      </div>
    </Container>
  )
}

export default HomePage
