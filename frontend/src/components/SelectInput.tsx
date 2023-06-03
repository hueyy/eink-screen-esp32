import { useCallback } from 'preact/hooks'
import type { FunctionComponent } from 'preact'

interface Props {
  className?: string
  label: string
  options: Array<{
    value: string
    content: string
  }>
  value?: string
  onChange?: (value: string) => void
  defaultValue?: string
}

const SelectInput: FunctionComponent<Props> = ({
  className = '',
  label,
  options,
  value = '',
  defaultValue = options[0].value,
  onChange = () => {}
}) => {
  const onSelect = useCallback(({ target }: Event) => {
    if (target instanceof HTMLSelectElement) {
      onChange(target.value)
    }
  }, [onChange])
  const valueWithDefault = (((value.length === 0) || !options.map(({ value }) => value).includes(value)) && defaultValue.length > 0)
    ? defaultValue
    : value

  return (
    <div className={`flex flex-row justify-between items-center gap-4 ${className}`}>
      <div className="font-bold">
        <label>{label}</label>
      </div>
      <select
        className={'h-full border border-solid border-gray-400 rounded px-2 py-1 outline-none bg-gray-100'}
        value={valueWithDefault}
        onChange={onSelect}
      >
        {options.map(({ value, content }) => (
          <option
            value={value}
            key={value}
          >
            {content}
          </option>
        ))}
      </select>
    </div>
  )
}

export default SelectInput
