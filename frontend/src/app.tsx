import { useCallback, useEffect } from 'preact/hooks'


const IMAGE_BUFFER_SERVICE_ID = "5eabe403-2988-48b4-90e9-a714538f0080"
const IMAGE_BUFFER_CHARACTERISTIC_ID = "6c9494c0-d4f8-418c-af2c-084c32baf2d3"
const CHARACTERISTIC_MAX_SIZE = 512

const RecursiveSend = (characteristic: any, data: any) => {
  return characteristic.writeValue(data)
  .catch(() => {
    return RecursiveSend(characteristic, data);
  })
}

const sendBufferedData = (service: any, file: any) => {
  const totalSize = file.byteLength;
  let remaining = totalSize;
  let amountToWrite = 0;
  let currentPosition = 0;
  if (remaining > 0) {
    if (remaining >= CHARACTERISTIC_MAX_SIZE) {
      amountToWrite = CHARACTERISTIC_MAX_SIZE
    }
    else {
      amountToWrite = remaining;
    }
    let dataToSend = file.slice(currentPosition, currentPosition + amountToWrite);
    currentPosition += amountToWrite;
    remaining -= amountToWrite;
    console.log("remaining: " + remaining);
    service.getCharacteristic(IMAGE_BUFFER_CHARACTERISTIC_ID)
      .then((characteristic: any) => RecursiveSend(characteristic, dataToSend))
      .then((_: any) => {
        return console.log((100 * (currentPosition/totalSize)).toPrecision(3) + '%');
      })
      .catch((error: Error) => { 
        console.log(error); 
      });
  }
}

const sendFileOverBluetooth = (service: any, file: any) => {
  service.getCharacteristic(IMAGE_BUFFER_CHARACTERISTIC_ID)
  .then((characteristic: any) => {
    let readyFlagCharacteristic = characteristic;
    return characteristic.startNotifications()
    .then((_: any) => {
      readyFlagCharacteristic.addEventListener('characteristicvaluechanged', sendBufferedData)
    });
  })
  .catch((error: Error) => { 
    console.log(error); 
  });
  sendBufferedData(service, file);
}

const getGATT = async (): Promise<BluetoothRemoteGATTServer> => {
  const device = await navigator.bluetooth.requestDevice({
    filters: [{
      services: [IMAGE_BUFFER_SERVICE_ID],
    }]
  })
  console.log(device)
  if(!device.gatt){
    console.error("No GATT!")
    return await getGATT()
  }
  return device.gatt
}

const getService = async (gatt: BluetoothRemoteGATTServer): Promise<BluetoothRemoteGATTService> => {
  const server = await gatt.connect()
  console.log(server)
  try {
    const service = await server.getPrimaryService(IMAGE_BUFFER_SERVICE_ID)
    console.log(service)
    return service
  } catch (error){
    console.error(error)
    return await getService(gatt)
  }
}

export function App() {

  const onStart = useCallback(async () => {
    try {
      const gatt = await getGATT()
      const service = await getService(gatt)   
      const data = new ArrayBuffer(100)
      sendFileOverBluetooth(service, data)
    } catch (error){
      console.error(error)
    }
    
  }, [])

  return (
    <>
      <h1>Hello world</h1>
      <button onClick={onStart}>START</button>
    </>
  )
}
