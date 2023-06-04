import type { ComponentChildren, FunctionComponent } from 'preact'

interface Props {
  className?: string
  onClick?: (() => void) | (() => Promise<void>)
  children: ComponentChildren
}

const PrimaryButton: FunctionComponent<Props> = ({
  className = '',
  onClick = () => {},
  children = null
}) => {
  return (
    <button type="button" onClick={onClick} className={`bg-indigo-700 text-white py-2 px-4 font-bold ${className}`}>
      { children }
    </button>
  )
}

export default PrimaryButton
