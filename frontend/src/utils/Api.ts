const postImageData = async (host: string, imageData: Uint8Array): Promise<Record<string, string>> => {
  try {
    const response = await fetch(`${host}/receive_data/`, { method: 'POST', body: imageData })
    return await response.json()
  } catch (error) {
    console.error(error)
    throw error
  }
}

const clearImage = async (host: string): Promise<Record<string, string>> => {
  try {
    const response = await fetch(`${host}/clear/`, { method: 'POST' })
    return await response.json()
  } catch (error) {
    console.error(error)
    throw error
  }
}

const Api = {
  postImageData,
  clearImage
}

export default Api
