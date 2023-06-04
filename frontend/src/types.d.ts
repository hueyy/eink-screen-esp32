interface WifiCredential {
  ssid: string
  password: string
}

interface Store {
  imageSizing: 'fullWidth' | 'fullHeight'
  imageRotation: '0' | '90' | '180' | '270'
  wifi: WifiCredential[]
  host: string
}
