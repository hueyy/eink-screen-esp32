import type { FunctionComponent } from 'preact'

interface Props {
  label: string
}

const SelectInput: FunctionComponent<Props> = ({ label }) => {
  return (
    <div className="">
      <div className="">
        <label>{label}</label>
      </div>
    </div>
  )
}

export default SelectInput
