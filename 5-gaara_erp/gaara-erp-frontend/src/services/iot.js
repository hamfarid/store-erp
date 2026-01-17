import api from "./api"

/**
 * IoT Service
 * Handles all IoT monitoring and device management API calls
 */

// Devices
export const getDevices = async (params = {}) => {
  return api.get("/iot/devices", { params })
}

export const getDeviceById = async (deviceId) => {
  return api.get(`/iot/devices/${deviceId}`)
}

export const createDevice = async (deviceData) => {
  return api.post("/iot/devices", deviceData)
}

export const updateDevice = async (deviceId, deviceData) => {
  return api.put(`/iot/devices/${deviceId}`, deviceData)
}

export const deleteDevice = async (deviceId) => {
  return api.delete(`/iot/devices/${deviceId}`)
}

export const toggleDeviceStatus = async (deviceId, isActive) => {
  return api.patch(`/iot/devices/${deviceId}/status`, { isActive })
}

// Sensors
export const getSensors = async (deviceId = null, params = {}) => {
  const url = deviceId ? `/iot/devices/${deviceId}/sensors` : "/iot/sensors"
  return api.get(url, { params })
}

export const getSensorById = async (sensorId) => {
  return api.get(`/iot/sensors/${sensorId}`)
}

export const getSensorReadings = async (sensorId, params = {}) => {
  const { startDate, endDate, limit = 100 } = params
  const queryParams = new URLSearchParams({
    limit: limit.toString(),
    ...(startDate && { startDate }),
    ...(endDate && { endDate }),
  })

  return api.get(`/iot/sensors/${sensorId}/readings?${queryParams}`)
}

// Alerts
export const getAlerts = async (params = {}) => {
  const { page = 1, limit = 20, status = "", severity = "", device = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(status && { status }),
    ...(severity && { severity }),
    ...(device && { device }),
  })

  return api.get(`/iot/alerts?${queryParams}`)
}

export const getAlertById = async (alertId) => {
  return api.get(`/iot/alerts/${alertId}`)
}

export const acknowledgeAlert = async (alertId) => {
  return api.post(`/iot/alerts/${alertId}/acknowledge`)
}

export const resolveAlert = async (alertId) => {
  return api.post(`/iot/alerts/${alertId}/resolve`)
}

// Real-time Data
export const subscribeToDevice = async (deviceId, callback) => {
  // WebSocket or SSE implementation
  // This is a placeholder for real-time updates
  return api.get(`/iot/devices/${deviceId}/stream`)
}

export const getDeviceStatus = async (deviceId) => {
  return api.get(`/iot/devices/${deviceId}/status`)
}

// Analytics
export const getDeviceAnalytics = async (deviceId, params = {}) => {
  return api.get(`/iot/devices/${deviceId}/analytics`, { params })
}

export const getSensorAnalytics = async (sensorId, params = {}) => {
  return api.get(`/iot/sensors/${sensorId}/analytics`, { params })
}

// Mock data for development
export const mockDevices = [
  {
    id: 1,
    name: "جهاز استشعار الحقل 1",
    type: "sensor",
    location: "حقل الشمال",
    status: "online",
    battery: 85,
    signal: 92,
    lastUpdate: new Date().toISOString(),
    sensors: [
      { id: 1, type: "temperature", value: 25.5, unit: "°C" },
      { id: 2, type: "humidity", value: 60, unit: "%" },
    ],
  },
  {
    id: 2,
    name: "جهاز الري الذكي",
    type: "controller",
    location: "حقل الجنوب",
    status: "online",
    battery: 70,
    signal: 88,
    lastUpdate: new Date().toISOString(),
    sensors: [
      { id: 3, type: "water_level", value: 75, unit: "%" },
    ],
  },
]

export default {
  getDevices,
  getDeviceById,
  createDevice,
  updateDevice,
  deleteDevice,
  toggleDeviceStatus,
  getSensors,
  getSensorById,
  getSensorReadings,
  getAlerts,
  getAlertById,
  acknowledgeAlert,
  resolveAlert,
  subscribeToDevice,
  getDeviceStatus,
  getDeviceAnalytics,
  getSensorAnalytics,
  mockDevices,
}
