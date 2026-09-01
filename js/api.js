/**
 * Bufete Caballero - API Client
 * Centralized Fetch wrapper for FastAPI Backend
 */

const API_BASE = '/api/v1';

const apiClient = {
  /**
   * Health check
   */
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Error al conectar con el servidor');
    return res.json();
  },

  /**
   * Enviar formulario de contacto
   */
  async submitContact(data) {
    const res = await fetch(`${API_BASE}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Error al enviar la consulta' }));
      throw new Error(err.detail || 'Error en la solicitud');
    }
    return res.json();
  },

  /**
   * Obtener franjas horarias disponibles para una fecha
   */
  async getAvailableSlots(date, lawyerName = '') {
    let url = `${API_BASE}/consultations/available-slots?date=${encodeURIComponent(date)}`;
    if (lawyerName && lawyerName !== 'Cualquiera disponible') {
      url += `&lawyer_name=${encodeURIComponent(lawyerName)}`;
    }
    const res = await fetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Error al cargar horarios' }));
      throw new Error(err.detail || 'Error al obtener horarios');
    }
    return res.json();
  },

  /**
   * Reservar cita o consulta legal
   */
  async bookConsultation(data) {
    const res = await fetch(`${API_BASE}/consultations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Error al programar la cita' }));
      throw new Error(err.detail || 'Error al reservar cita');
    }
    return res.json();
  },

  /**
   * Evaluador legal / triage de casos
   */
  async evaluateCase(data) {
    const res = await fetch(`${API_BASE}/case-evaluator`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Error en la evaluación' }));
      throw new Error(err.detail || 'Error al evaluar el caso');
    }
    return res.json();
  },

  /**
   * Obtener abogados
   */
  async getLawyers() {
    const res = await fetch(`${API_BASE}/lawyers`);
    if (!res.ok) throw new Error('Error al cargar equipo de abogados');
    return res.json();
  },

  /**
   * Obtener áreas de práctica
   */
  async getPracticeAreas() {
    const res = await fetch(`${API_BASE}/practice-areas`);
    if (!res.ok) throw new Error('Error al cargar áreas de práctica');
    return res.json();
  },

  /**
   * ADMIN: Obtener métricas del dashboard
   */
  async getAdminDashboard() {
    const res = await fetch(`${API_BASE}/admin/dashboard`);
    if (!res.ok) throw new Error('Error al cargar estadísticas');
    return res.json();
  },

  /**
   * ADMIN: Obtener consultas con filtros
   */
  async getAdminInquiries(filters = {}) {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.urgency) params.append('urgency', filters.urgency);
    if (filters.area) params.append('area', filters.area);
    if (filters.search) params.append('search', filters.search);

    const res = await fetch(`${API_BASE}/admin/inquiries?${params.toString()}`);
    if (!res.ok) throw new Error('Error al cargar expedientes');
    return res.json();
  },

  /**
   * ADMIN: Obtener citas agendadas
   */
  async getAdminConsultations() {
    const res = await fetch(`${API_BASE}/consultations`);
    if (!res.ok) throw new Error('Error al cargar citas');
    return res.json();
  },

  /**
   * ADMIN: Actualizar estado y notas de expediente
   */
  async updateInquiryStatus(id, status, notes = null) {
    const res = await fetch(`${API_BASE}/admin/inquiries/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, admin_notes: notes })
    });
    if (!res.ok) throw new Error('Error al actualizar expediente');
    return res.json();
  },

  /**
   * ADMIN: Actualizar estado de cita
   */
  async updateConsultationStatus(id, status) {
    const res = await fetch(`${API_BASE}/admin/consultations/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    if (!res.ok) throw new Error('Error al actualizar cita');
    return res.json();
  },

  /**
   * ADMIN: Eliminar expediente
   */
  async deleteInquiry(id) {
    const res = await fetch(`${API_BASE}/admin/inquiries/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Error al eliminar expediente');
    return true;
  }
};

window.apiClient = apiClient;
