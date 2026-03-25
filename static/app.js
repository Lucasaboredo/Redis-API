const apiUrl = '/api/episodes';
let currentPaymentEpisode = null;

document.addEventListener('DOMContentLoaded', () => {
    loadEpisodes();
    
    // Config modal
    document.getElementById('cancel-payment-btn').addEventListener('click', closePaymentModal);
    document.getElementById('confirm-payment-btn').addEventListener('click', confirmPayment);
    
    // Auto-refresh every 10 seconds to show real-time changes
    setInterval(loadEpisodes, 10000);
});

async function loadEpisodes() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        
        if (response.ok) {
            renderEpisodes(data);
        } else {
            showToast(data.error || 'Error cargando episodios', 'error');
        }
    } catch (error) {
        showToast('Error de conexión', 'error');
        console.error(error);
    }
}

function renderEpisodes(episodes) {
    const container = document.getElementById('episodes-container');
    container.innerHTML = '';
    
    episodes.forEach(ep => {
        const card = document.createElement('div');
        card.className = 'episode-card';
        
        let statusClass = '';
        let buttonHtml = '';
        
        if (ep.status === 'Disponible') {
            statusClass = 'status-disponible';
            buttonHtml = `<button class="btn primary-btn" onclick="rentEpisode('${ep.id}')">Alquilar</button>`;
        } else if (ep.status === 'Reservado') {
            statusClass = 'status-reservado';
            buttonHtml = `<button class="btn pay-btn" onclick="openPaymentModal('${ep.id}')">Confirmar Pago</button>`;
        } else if (ep.status === 'Alquilado') {
            statusClass = 'status-alquilado';
            buttonHtml = `<button class="btn outline-btn" disabled>No Disponible</button>`;
        }
        
        card.innerHTML = `
            <div>
                <div class="episode-header">
                    <h3 class="episode-title">${ep.title}</h3>
                    <span class="episode-season">S${ep.season.toString().padStart(2, '0')}</span>
                </div>
                <div class="status-badge ${statusClass}">${ep.status}</div>
                <p style="color:#aaa; font-size:0.9rem;">${ep.id}</p>
            </div>
            <div class="card-actions">
                ${buttonHtml}
            </div>
        `;
        
        container.appendChild(card);
    });
}

async function rentEpisode(epId) {
    try {
        const res = await fetch(`${apiUrl}/${epId}/rent`, { method: 'POST' });
        const data = await res.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            loadEpisodes();
            openPaymentModal(epId);
        } else {
            showToast(data.message, 'error');
            loadEpisodes();
        }
    } catch (e) {
        showToast('Error de red', 'error');
    }
}

function openPaymentModal(epId) {
    currentPaymentEpisode = epId;
    document.getElementById('payment-desc').innerHTML = `Abona el alquiler del <strong>Capítulo ${epId}</strong>. Tienes 4 minutos desde la reserva para confirmar.`;
    document.getElementById('payment-modal').classList.remove('hidden');
}

function closePaymentModal() {
    currentPaymentEpisode = null;
    document.getElementById('payment-modal').classList.add('hidden');
}

async function confirmPayment() {
    if (!currentPaymentEpisode) return;
    
    const price = document.getElementById('price-input').value;
    
    try {
        const res = await fetch(`${apiUrl}/${currentPaymentEpisode}/pay`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ price: price })
        });
        const data = await res.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            closePaymentModal();
            loadEpisodes();
        } else {
            showToast(data.message, 'error');
            closePaymentModal();
            loadEpisodes();
        }
    } catch (e) {
        showToast('Error procesando pago', 'error');
    }
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    if (type === 'error') {
        toast.style.borderLeftColor = 'var(--accent-red)';
    }
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
