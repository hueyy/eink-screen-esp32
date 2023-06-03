import type { FunctionComponent } from 'preact'

const HomePage: FunctionComponent = () => {
  return (
    <>
      <h1>eInk Screen</h1>
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
    </>
  )
}

export default HomePage
