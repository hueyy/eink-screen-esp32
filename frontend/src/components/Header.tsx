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
          <a className="text-2xl flex-initial cursor-pointer flex flex-row items-center" href="/">
            <div>⬅</div>
            <div className="text-base align-middle ml-2">Back</div>
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
