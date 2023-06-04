import { type ComponentChildren, type FunctionComponent } from 'preact'

interface Props {
  className?: string
  children: ComponentChildren
}

const Container: FunctionComponent<Props> = ({ className = '', children }) => {
  return (
    <div className="max-w-screen-md mx-auto">
      {children}
    </div>
  )
}

export default Container
