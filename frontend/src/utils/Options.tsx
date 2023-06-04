const imageSizing = {
  fullWidth: 'fullWidth',
  fullHeight: 'fullHeight'
} as const

const imageRotation = {
  0: '0',
  90: '90',
  180: '180',
  270: '270'
} as const

const dithering = {
  binary: 'binary',
  ternary: 'ternary',
  floydSteinberg: 'floydSteinberg',
  floydSteinbergRed: 'floydSteinbergRed'
} as const

const Options = {
  imageSizing,
  imageRotation,
  dithering
}

export default Options
