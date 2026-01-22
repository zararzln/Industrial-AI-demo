import axios from 'axios';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Equipment {
  id: string;
  name: string;
  type: string;
  location: string;
  status: 'operational' | 'warning' | 'critical' | 'maintenance' | 'offline';
  health_score: number;
  last_maintenance: string;
  next_maintenance: string;
  metrics: {
    temperature: number;
    pressure: number;
    vibration: number;
    [key: string]: number;
  };
}

export interface Alert {
  id: string;
  equipment_id: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  type: string;
  message: string;
  resolved: boolean;
}

export interface DashboardMetrics {
  total_equipment: number;
  operational_count: number;
  warning_count: number;
  critical_count: number;
  average_health_score: number;
  total_alerts: number;
  unresolved_alerts: number;
  maintenance_cost_mtd: number;
  energy_efficiency: number;
  predicted_failures: Array<{
    equipment_id: string;
    equipment_name: string;
    failure_probability: number;
    estimated_days: number;
    reason: string;
  }>;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
  recommendations: string[];
  confidence: number;
  agent_reasoning?: string;
}

// Equipment API
export const equipmentAPI = {
  getAll: () => api.get<Equipment[]>('/equipment'),
  getById: (id: string) => api.get<Equipment>(`/equipment/${id}`),
  getByStatus: (status: string) => api.get<Equipment[]>(`/equipment/status/${status}`),
  getAlerts: (equipmentId: string) => api.get<Alert[]>(`/equipment/${equipmentId}/alerts`),
};

// Dashboard API
export const dashboardAPI = {
  getExecutive: () => api.get<DashboardMetrics>('/dashboard/executive'),
  getOperator: () => api.get('/dashboard/operator'),
  getAllAlerts: (resolved?: boolean) => {
    const params = resolved !== undefined ? { resolved } : {};
    return api.get<Alert[]>('/dashboard/alerts', { params });
  },
  resolveAlert: (alertId: string) => api.patch(`/dashboard/alerts/${alertId}/resolve`),
};

// AI API
export const aiAPI = {
  query: (query: string, equipmentId?: string) =>
    api.post<QueryResponse>('/ai/query', { query, equipment_id: equipmentId }),
  healthCheck: () => api.get('/ai/health'),
};

export default api;
