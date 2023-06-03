const imageSizing = {
  crop: 'crop',
  centre: 'centre'
} as const

const imageRotation = {
  0: '0',
  90: '90',
  180: '180',
  270: '270'
} as const

const Options = {
  imageSizing,
  imageRotation
}

export default Options
