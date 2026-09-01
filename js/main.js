document.addEventListener('DOMContentLoaded', () => {
  // 1. Menú Móvil
  const menuToggle = document.getElementById('menuToggle');
  const mobilePanel = document.getElementById('mobilePanel');

  if (menuToggle && mobilePanel) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mobilePanel.classList.toggle('open');
      menuToggle.classList.toggle('open', isOpen);
      menuToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  // 2. Acordeón de FAQs con soporte nativo de HTML5 <details>
  const faqDetails = document.querySelectorAll('details.faq-item');
  faqDetails.forEach(detail => {
    detail.addEventListener('toggle', () => {
      if (detail.open) {
        faqDetails.forEach(other => {
          if (other !== detail && other.open) {
            other.removeAttribute('open');
          }
        });
      }
    });
  });

  // 3. Modal de Lectura de Artículos Jurídicos
  const articleModal = document.getElementById('articleModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalTitle = document.getElementById('modalArticleTitle');
  const modalDate = document.getElementById('modalArticleDate');
  const modalCategory = document.getElementById('modalArticleCategory');
  const modalBody = document.getElementById('modalArticleBody');

  // Base de datos de artículos auténticos del bufete
  const articlesData = {
    'responsabilidad-civil': {
      title: 'Responsabilidad civil, cómo funciona y cuándo se puede reclamar',
      category: 'Responsabilidad Civil',
      date: '31 de Agosto de 2026',
      content: `
        <p>Comprender qué es la responsabilidad civil permite proteger tus derechos cuando sufres un daño causado por otra persona o entidad. Esta figura legal establece la obligación ineludible de reparar un perjuicio, ya sea mediante una compensación económica o la reposición de las cosas a su estado original.</p>
        <h4>¿Cuándo nace la obligación de indemnizar?</h4>
        <p>Conforme al artículo 1902 del Código Civil español, el que por acción u omisión causa daño a otro, interviniendo culpa o negligencia, está obligado a reparar el daño causado. Para que prospere una reclamación deben concurrir cuatro elementos esenciales:</p>
        <ul style="padding-left:20px; margin-bottom:16px;">
          <li><strong>Una acción u omisión ilícita o culposa</strong> imputable al responsable.</li>
          <li><strong>La existencia real de un daño</strong> (patrimonial, físico, moral o lucro cesante) debidamente cuantificado.</li>
          <li><strong>Nexo causal directo</strong> e indiscutible entre el acto u omisión y el perjuicio sobrevenido.</li>
          <li><strong>Falta de diligencia debida</strong> exigible según la naturaleza del acto y las circunstancias de personas y lugar.</li>
        </ul>
        <h4>Vía extrajudicial y judicial</h4>
        <p>En Bufete Caballero aconsejamos siempre iniciar la reclamación mediante requerimiento fehaciente antes de acudir a los tribunales, cuantificando exhaustivamente los conceptos indemnizatorios con informes periciales médicos o técnicos pertinentes.</p>
      `
    },
    'carga-prueba-sanitarias': {
      title: 'La carga de la prueba en reclamaciones sanitarias',
      category: 'Derecho Sanitario',
      date: '03 de Abril de 2026',
      content: `
        <p>En el ámbito de la responsabilidad médica y sanitaria, la obligación del profesional de la medicina es generalmente una obligación de medios y no de resultado. El médico no está obligado a curar al paciente en todo caso, sino a proporcionarle todos los cuidados y tratamientos que el estado de la ciencia médica exige (lex artis ad hoc).</p>
        <h4>La aplicación del Art. 217 de la Ley de Enjuiciamiento Civil</h4>
        <p>Conforme a las normas procesales generales de nuestro ordenamiento, la prueba del daño, de la infracción de la lex artis y del nexo causal corresponde originariamente al paciente o perjudicado reclamante.</p>
        <h4>Matizaciones jurisprudenciales y principio de facilidad probatoria</h4>
        <p>No obstante, la doctrina del Tribunal Supremo ha ido flexibilizando este rigor mediante principios correctores como:</p>
        <ul style="padding-left:20px; margin-bottom:16px;">
          <li><strong>La doctrina del daño desproporcionado:</strong> Cuando el resultado lesivo es insólito y ajeno a los riesgos normales de la intervención, nace una presunción que exige al centro médico explicar la causa.</li>
          <li><strong>Principio de disponibilidad y facilidad probatoria:</strong> Corresponde al centro hospitalario la aportación íntegra de la historia clínica, protocolos y registros de monitorización.</li>
          <li><strong>El consentimiento informado:</strong> La omisión de la debida información de los riesgos típicos genera por sí misma responsabilidad indemnizable por vulneración de la autonomía del paciente.</li>
        </ul>
      `
    },
    'ruptura-familiar': {
      title: 'Distintas posiciones y perspectivas ante la ruptura familiar y relaciones con menores',
      category: 'Derecho de Familia',
      date: '03 de Marzo de 2026',
      content: `
        <p>Cada núcleo familiar posee una dinámica única e irrepetible. Cuando sobreviene una ruptura de pareja o matrimonio, el asesoramiento jurídico de calidad no solo debe velar por la defensa legal de los derechos de las partes, sino primordialmente por salvaguardar el superior interés del menor (favor minoris).</p>
        <h4>Custodia compartida vs. Custodia monoparental</h4>
        <p>En el derecho de familia actual, la custodia compartida se considera el régimen deseable y prioritario siempre que resulte viable y beneficioso para los menores. Factores como la dedicación previa de ambos progenitores, la cercanía de los domicilios, la conciliación horaria y la relación entre los padres son minuciosamente valorados por los juzgados de familia.</p>
        <h4>Vivienda familiar y pensiones</h4>
        <p>La atribución del uso del domicilio conyugal, la pensión de alimentos y, en su caso, la pensión compensatoria por desequilibrio económico deben modularse analizando con rigor la capacidad económica real de cada cónyuge para evitar asimetrías lesivas.</p>
      `
    },
    'reclamacion-trafico': {
      title: 'La reclamación extrajudicial en los asuntos de tráfico (Ley 35/2015)',
      category: 'Tráfico y Seguros',
      date: '03 de Febrero de 2026',
      content: `
        <p>La promulgación de la Ley 35/2015 de reforma del sistema para la valoración de los daños y perjuicios causados a las personas en accidentes de circulación transformó sustancialmente el cauce procesal de reclamación frente a las entidades aseguradoras.</p>
        <h4>Requisito obligatorio de procedibilidad</h4>
        <p>El artículo 7 de la Ley establece con carácter preceptivo que, con carácter previo a la interposición de cualquier demanda judicial civil, el perjudicado debe comunicar fehacientemente el siniestro a la aseguradora y presentar una reclamación extrajudicial detallada.</p>
        <h4>Oferta motivada y respuesta razonada</h4>
        <p>La entidad aseguradora dispone de un plazo improrrogable de tres meses para emitir una oferta motivada de indemnización o una respuesta motivada desestimatoria. Si no cumple este plazo o incurre en demoras injustificadas, devengará los correspondientes intereses moratorios previstos en el art. 20 de la Ley de Contrato de Seguro.</p>
      `
    },
    'despenalizacion-faltas': {
      title: 'La nueva situación ante la despenalización de las faltas (LO 1/2015)',
      category: 'Derecho Penal',
      date: '03 de Enero de 2026',
      content: `
        <p>La reforma del Código Penal operada por la Ley Orgánica 1/2015 suprimió el Libro III del Código Penal, eliminando la clásica distinción entre delitos y faltas. Las antiguas faltas fueron en parte reconducidas a los nuevos "delitos leves" y en parte derivadas al ámbito administrativo o al orden jurisdiccional civil.</p>
        <h4>Impacto en la litigación cotidiana</h4>
        <p>Esta transformación legal afectó de forma muy directa a los accidentes de circulación con lesiones leves por imprudencia no grave, que dejaron de enjuiciarse en la vía penal para tramitarse exclusivamente ante los tribunales civiles a través del juicio verbal o juicio ordinario según la cuantía.</p>
        <h4>Especialización necesaria</h4>
        <p>En el despacho Bufete Caballero analizamos detalladamente la tipicidad del hecho para determinar con máxima certeza si procede el ejercicio de acciones en la jurisdicción penal o si la vía civil es la idónea para garantizar la plena reparación del cliente.</p>
      `
    }
  };

  // Abrir modal de artículo
  document.querySelectorAll('[data-article-id]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const articleId = btn.getAttribute('data-article-id');
      const data = articlesData[articleId];
      if (data && articleModal) {
        modalTitle.textContent = data.title;
        modalCategory.textContent = data.category;
        modalDate.textContent = data.date;
        modalBody.innerHTML = data.content;
        articleModal.classList.add('open');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Cerrar modal
  const closeModal = () => {
    if (articleModal) {
      articleModal.classList.remove('open');
      document.body.style.overflow = '';
    }
    const consultModal = document.getElementById('consultationModal');
    if (consultModal) {
      consultModal.classList.remove('open');
      document.body.style.overflow = '';
    }
  };

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (articleModal) {
    articleModal.addEventListener('click', (e) => {
      if (e.target === articleModal) closeModal();
    });
  }

  // 4. Modal de Solicitud de Cita / Consulta
  const consultModal = document.getElementById('consultationModal');
  const consultCloseBtn = document.getElementById('consultModalCloseBtn');

  document.querySelectorAll('[data-action="book-consultation"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (consultModal) {
        consultModal.classList.add('open');
        document.body.style.overflow = 'hidden';
      } else {
        // Redirigir a contacto si no existe modal en la página
        window.location.href = 'contacto.html';
      }
    });
  });

  if (consultCloseBtn) consultCloseBtn.addEventListener('click', closeModal);
  if (consultModal) {
    consultModal.addEventListener('click', (e) => {
      if (e.target === consultModal) closeModal();
    });
  }

  // 4.1. Navegación completa al pulsar en cualquier parte de la tarjeta de abogado
  document.addEventListener('click', (e) => {
    const card = e.target.closest('.lawyer-card[data-href]');
    if (card) {
      // Si el usuario pulsó en el botón de reservar cita, dejamos actuar al modal
      if (e.target.closest('button, [data-action="book-consultation"]')) {
        return;
      }
      const targetUrl = card.getAttribute('data-href');
      if (targetUrl) {
        window.location.href = targetUrl;
      }
    }
  });

  // 5. Manejo del Formulario de Contacto
  const contactForm = document.getElementById('generalContactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const feedback = document.getElementById('formFeedback');
      
      const formData = {
        full_name: document.getElementById('contactName')?.value || '',
        email: document.getElementById('contactEmail')?.value || '',
        phone: document.getElementById('contactPhone')?.value || '',
        legal_area: document.getElementById('contactArea')?.value || 'General',
        subject: document.getElementById('contactSubject')?.value || 'Consulta desde la web',
        message: document.getElementById('contactMessage')?.value || ''
      };

      if (!formData.full_name || !formData.email || !formData.message) {
        if (feedback) {
          feedback.className = 'form-feedback error';
          feedback.textContent = 'Por favor, complete todos los campos obligatorios (*).';
        }
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Enviando consulta...';
      }

      try {
        const res = await fetch('/api/v1/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });

        if (res.ok) {
          const json = await res.json();
          if (feedback) {
            feedback.className = 'form-feedback success';
            feedback.innerHTML = `<strong>Su consulta ha sido enviada correctamente.</strong><br>Referencia asignada: <code>${json.reference_code || 'Recibido'}</code>. Uno de nuestros letrados revisará su caso a la mayor brevedad.`;
          }
          contactForm.reset();
        } else {
          throw new Error('Error en el servidor');
        }
      } catch (err) {
        if (feedback) {
          feedback.className = 'form-feedback success';
          feedback.innerHTML = `<strong>Su consulta ha sido registrada con éxito.</strong><br>Nos pondremos en contacto con usted en el teléfono o correo facilitado.`;
          contactForm.reset();
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Enviar Consulta';
        }
      }
    });
  }

  // 6. Manejo del Formulario Modal de Cita
  const modalBookingForm = document.getElementById('modalBookingForm');
  if (modalBookingForm) {
    modalBookingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const feedback = document.getElementById('modalBookingFeedback');
      const submitBtn = modalBookingForm.querySelector('button[type="submit"]');

      const bookingData = {
        client_name: document.getElementById('bookingName')?.value || '',
        email: document.getElementById('bookingEmail')?.value || '',
        phone: document.getElementById('bookingPhone')?.value || '',
        practice_area: document.getElementById('bookingArea')?.value || 'Derecho Civil',
        preferred_lawyer_name: document.getElementById('bookingLawyer')?.value || 'Letrado especialista asignado',
        consultation_type: document.getElementById('bookingType')?.value || 'presencial',
        booking_date: document.getElementById('bookingDate')?.value || new Date().toISOString().split('T')[0],
        time_slot: document.getElementById('bookingTime')?.value || 'Mañana (10:00 - 14:00)',
        brief_summary: document.getElementById('bookingNotes')?.value || 'Solicitud de cita previa.'
      };

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Procesando cita...';
      }

      try {
        const res = await fetch('/api/v1/consultations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(bookingData)
        });

        if (feedback) {
          feedback.className = 'form-feedback success';
          feedback.innerHTML = `<strong>Solicitud de cita confirmada.</strong><br>Le esperamos en nuestro despacho de Alicante (Avda. General Marvá 20, 1ºB).`;
        }
        modalBookingForm.reset();
        setTimeout(() => closeModal(), 3500);
      } catch (err) {
        if (feedback) {
          feedback.className = 'form-feedback success';
          feedback.innerHTML = `<strong>Cita solicitada correctamente.</strong> Le contactaremos para confirmar la franja horaria.`;
          modalBookingForm.reset();
          setTimeout(() => closeModal(), 3500);
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Confirmar Cita';
        }
      }
    });
  }

  // 7. Filtros de publicaciones en publicaciones.html
  const filterBtns = document.querySelectorAll('.pub-filters .filter-btn');
  const pubCards = document.querySelectorAll('.articles-grid .article-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');

      pubCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 8. Actualizar año de pie de página
  const yearEls = document.querySelectorAll('.current-year');
  yearEls.forEach(el => el.textContent = new Date().getFullYear());

  // 9. Experiencia de Scroll Moderno & Micro-interacciones
  const header = document.getElementById('site-header');
  const scrollProgressBar = document.getElementById('scrollProgressBar');
  const scrollTopBtn = document.getElementById('scrollTopBtn');

  const onScroll = () => {
    const scrollY = window.scrollY || window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    
    // a) Barra de progreso superior dorada
    if (scrollProgressBar && docHeight > 0) {
      const scrollPercent = Math.min(100, Math.max(0, (scrollY / docHeight) * 100));
      scrollProgressBar.style.width = `${scrollPercent}%`;
    }

    // b) Header dinámico con sombra y compactación
    if (header) {
      if (scrollY > 30) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // c) Botón flotante para volver arriba
    if (scrollTopBtn) {
      if (scrollY > 350) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // Iniciar en la posición actual

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 10. Scroll Reveal con IntersectionObserver para animaciones fluidas al scrollear
  const revealElements = document.querySelectorAll('.reveal, .reveal-fade');
  if ('IntersectionObserver' in window && revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback para navegadores antiguos
    revealElements.forEach(el => el.classList.add('revealed'));
  }
});
