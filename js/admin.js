/**
 * Bufete Caballero - Panel Administrativo y de Gestión de Expedientes
 */

document.addEventListener('DOMContentLoaded', () => {
  const statsWrap = document.getElementById('adminStats');
  const inquiriesTableBody = document.getElementById('inquiriesTableBody');
  const consultationsTableBody = document.getElementById('consultationsTableBody');
  const statusFilter = document.getElementById('statusFilter');
  const searchInput = document.getElementById('searchInput');
  const refreshBtn = document.getElementById('btnRefresh');
  const tabInquiries = document.getElementById('tabInquiries');
  const tabConsultations = document.getElementById('tabConsultations');
  const viewInquiries = document.getElementById('viewInquiries');
  const viewConsultations = document.getElementById('viewConsultations');

  let currentInquiries = [];
  let currentConsultations = [];

  // Tab switching
  if (tabInquiries && tabConsultations) {
    tabInquiries.addEventListener('click', () => {
      tabInquiries.classList.add('active');
      tabConsultations.classList.remove('active');
      viewInquiries.style.display = 'block';
      viewConsultations.style.display = 'none';
    });

    tabConsultations.addEventListener('click', () => {
      tabConsultations.classList.add('active');
      tabInquiries.classList.remove('active');
      viewConsultations.style.display = 'block';
      viewInquiries.style.display = 'none';
    });
  }

  async function loadDashboard() {
    try {
      const stats = await window.apiClient.getAdminDashboard();
      if (statsWrap) {
        statsWrap.innerHTML = `
          <div class="kpi-card">
            <div class="kpi-num">${stats.total_inquiries}</div>
            <div class="kpi-label">Consultas Totales</div>
          </div>
          <div class="kpi-card highlight">
            <div class="kpi-num">${stats.new_inquiries}</div>
            <div class="kpi-label">Expedientes Nuevos</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-num">${stats.total_consultations}</div>
            <div class="kpi-label">Citas Programadas</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-num">${stats.pending_consultations}</div>
            <div class="kpi-label">Citas Confirmadas Activas</div>
          </div>
        `;
      }
    } catch (e) {
      console.error('Error loading dashboard stats:', e);
    }
  }

  function getStatusBadge(status) {
    switch (status) {
      case 'nuevo':
        return '<span class="status-pill status-nuevo">● Nuevo</span>';
      case 'en_estudio':
        return '<span class="status-pill status-estudio">◐ En Estudio</span>';
      case 'contactado':
        return '<span class="status-pill status-contactado">✓ Contactado</span>';
      case 'cerrado':
        return '<span class="status-pill status-cerrado">✕ Cerrado</span>';
      case 'confirmada':
        return '<span class="status-pill status-contactado">✓ Confirmada</span>';
      case 'realizada':
        return '<span class="status-pill status-estudio">● Realizada</span>';
      case 'cancelada':
        return '<span class="status-pill status-cerrado">✕ Cancelada</span>';
      default:
        return `<span class="status-pill">${status}</span>`;
    }
  }

  function renderInquiries(items) {
    if (!inquiriesTableBody) return;
    if (!items || items.length === 0) {
      inquiriesTableBody.innerHTML = '<tr><td colspan="7" class="text-center py-6">No se encontraron expedientes con los criterios seleccionados.</td></tr>';
      return;
    }

    inquiriesTableBody.innerHTML = items.map(item => `
      <tr data-id="${item.id}">
        <td><strong>${item.reference_code}</strong></td>
        <td>
          <div class="client-name">${item.full_name}</div>
          <div class="client-sub">${item.email} ${item.phone ? '· ' + item.phone : ''}</div>
        </td>
        <td><span class="area-tag">${item.legal_area}</span></td>
        <td>
          <div class="subject-text" title="${item.message}">${item.subject}</div>
        </td>
        <td>
          <span class="urgency-dot ${item.urgency}"></span> ${item.urgency.toUpperCase()}
        </td>
        <td>
          <select class="status-selector" data-id="${item.id}">
            <option value="nuevo" ${item.status === 'nuevo' ? 'selected' : ''}>Nuevo</option>
            <option value="en_estudio" ${item.status === 'en_estudio' ? 'selected' : ''}>En Estudio</option>
            <option value="contactado" ${item.status === 'contactado' ? 'selected' : ''}>Contactado</option>
            <option value="cerrado" ${item.status === 'cerrado' ? 'selected' : ''}>Cerrado</option>
          </select>
        </td>
        <td>
          <button class="btn btn-sm btn-ghost btn-view-detail" data-id="${item.id}">Ver / Notas</button>
        </td>
      </tr>
    `).join('');

    // Bind inline status change
    inquiriesTableBody.querySelectorAll('.status-selector').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        try {
          await window.apiClient.updateInquiryStatus(id, newStatus);
          loadDashboard();
        } catch (err) {
          alert('Error al actualizar estado: ' + err.message);
        }
      });
    });

    // Bind details modal
    inquiriesTableBody.querySelectorAll('.btn-view-detail').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.getAttribute('data-id'), 10);
        const item = currentInquiries.find(i => i.id === id);
        if (item) openDetailDrawer(item);
      });
    });
  }

  function renderConsultations(items) {
    if (!consultationsTableBody) return;
    if (!items || items.length === 0) {
      consultationsTableBody.innerHTML = '<tr><td colspan="7" class="text-center py-6">No hay citas registradas en el sistema.</td></tr>';
      return;
    }

    consultationsTableBody.innerHTML = items.map(c => `
      <tr>
        <td><strong>${c.reference_code}</strong></td>
        <td>
          <div class="client-name">${c.client_name}</div>
          <div class="client-sub">${c.email} · ${c.phone}</div>
        </td>
        <td>${c.practice_area}</td>
        <td><strong>${c.booking_date}</strong><br><span class="time-sub">${c.time_slot}</span></td>
        <td>${c.preferred_lawyer_name || 'Cualquiera disponible'}</td>
        <td>${c.consultation_type.toUpperCase()}</td>
        <td>
          <select class="status-selector-consultation" data-id="${c.id}">
            <option value="confirmada" ${c.status === 'confirmada' ? 'selected' : ''}>Confirmada</option>
            <option value="realizada" ${c.status === 'realizada' ? 'selected' : ''}>Realizada</option>
            <option value="cancelada" ${c.status === 'cancelada' ? 'selected' : ''}>Cancelada</option>
          </select>
        </td>
      </tr>
    `).join('');

    consultationsTableBody.querySelectorAll('.status-selector-consultation').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        try {
          await window.apiClient.updateConsultationStatus(id, newStatus);
          loadDashboard();
        } catch (err) {
          alert('Error al actualizar cita: ' + err.message);
        }
      });
    });
  }

  function openDetailDrawer(item) {
    let drawer = document.getElementById('inquiryDetailDrawer');
    if (!drawer) {
      const drawerHTML = `
        <div class="drawer-overlay" id="inquiryDetailDrawer">
          <div class="drawer-panel">
            <button class="drawer-close" id="closeDrawer">&times;</button>
            <div id="drawerContent"></div>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', drawerHTML);
      drawer = document.getElementById('inquiryDetailDrawer');
      document.getElementById('closeDrawer').addEventListener('click', () => {
        drawer.classList.remove('open');
      });
      drawer.addEventListener('click', (e) => {
        if (e.target === drawer) drawer.classList.remove('open');
      });
    }

    const content = document.getElementById('drawerContent');
    content.innerHTML = `
      <div class="drawer-header">
        <span class="ref-badge">${item.reference_code}</span>
        <h3>${item.subject}</h3>
        <span class="date-sub">Recibido: ${new Date(item.created_at).toLocaleString('es-ES')}</span>
      </div>

      <div class="drawer-info-grid">
        <div><strong>Cliente:</strong> ${item.full_name}</div>
        <div><strong>Email:</strong> <a href="mailto:${item.email}">${item.email}</a></div>
        <div><strong>Teléfono:</strong> <a href="tel:${item.phone || ''}">${item.phone || 'No indicado'}</a></div>
        <div><strong>Área:</strong> ${item.legal_area}</div>
        <div><strong>Urgencia:</strong> ${item.urgency.toUpperCase()}</div>
        <div><strong>Preferencia:</strong> ${item.preferred_contact.toUpperCase()}</div>
      </div>

      <div class="drawer-section">
        <h4>Mensaje del Cliente:</h4>
        <div class="message-box">${item.message}</div>
      </div>

      <div class="drawer-section">
        <h4>Anotaciones Internas del Letrado:</h4>
        <textarea id="drawerNotes" class="eval-textarea" rows="3" placeholder="Añadir observaciones internas sobre la llamada, documentación solicitada o asignación...">${item.admin_notes || ''}</textarea>
        <button type="button" class="btn btn-sm btn-primary" id="btnSaveNotes" style="margin-top:8px;">Guardar Notas</button>
      </div>

      <div class="drawer-actions">
        <a href="mailto:${item.email}?subject=Bufete Caballero - Ref ${item.reference_code}" class="btn btn-primary">Responder por Email</a>
        <button type="button" class="btn btn-ghost" id="btnDeleteInquiry" style="color:var(--burgundy);">Eliminar Expediente</button>
      </div>
    `;

    document.getElementById('btnSaveNotes').addEventListener('click', async () => {
      const notes = document.getElementById('drawerNotes').value;
      try {
        await window.apiClient.updateInquiryStatus(item.id, item.status, notes);
        item.admin_notes = notes;
        alert('Notas guardadas correctamente.');
      } catch (err) {
        alert('Error: ' + err.message);
      }
    });

    document.getElementById('btnDeleteInquiry').addEventListener('click', async () => {
      if (confirm(`¿Está seguro de eliminar el expediente ${item.reference_code}?`)) {
        try {
          await window.apiClient.deleteInquiry(item.id);
          drawer.classList.remove('open');
          loadData();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      }
    });

    drawer.classList.add('open');
  }

  async function loadData() {
    await loadDashboard();
    try {
      const filterVal = statusFilter ? statusFilter.value : '';
      const searchVal = searchInput ? searchInput.value.trim() : '';
      
      const filters = {};
      if (filterVal) filters.status = filterVal;
      if (searchVal) filters.search = searchVal;

      currentInquiries = await window.apiClient.getAdminInquiries(filters);
      renderInquiries(currentInquiries);

      currentConsultations = await window.apiClient.getAdminConsultations();
      renderConsultations(currentConsultations);
    } catch (e) {
      console.error('Error loading admin data:', e);
    }
  }

  if (statusFilter) statusFilter.addEventListener('change', loadData);
  if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(loadData, 300);
    });
  }

  if (refreshBtn) refreshBtn.addEventListener('click', loadData);

  // Initial load
  loadData();
});
