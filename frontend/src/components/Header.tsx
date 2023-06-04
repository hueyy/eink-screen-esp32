import type { ComponentChildren, FunctionComponent } from 'preact'

interface Props {
  children: ComponentChildren
  backButton?: boolean
}

const Header: FunctionComponent<Props> = ({
  children,
  backButton = false
}) => {
  return (
    <div className="flex flex-row mt-6 select-none px-2">
      {backButton
        ? (
        <a className="text-2xl flex-initial cursor-pointer" href="/">
          ⬅ <span className="text-base align-middle">Back</span>
        </a>
          )
        : null}
      <div className="text-2xl font-black flex-1 text-center">
        {children}
      </div>
    </div>
  )
}

export default Header
