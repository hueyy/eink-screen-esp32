const postImageData = async (imageData: Uint8Array) => {
  try {
    const response = await fetch(`http://192.168.10.92/receive_data/`, { method: 'POST', body: imageData })
    return await response.json()
  } catch (error) {
    console.error(error)
    throw error
  }
}

const Api = {
  postImageData,
}

export default Api