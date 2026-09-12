// Global Interactive Functionality for Simpsons Breakdown Recovery

document.addEventListener('DOMContentLoaded', () => {
  // 1. ENTRY POP-UP BANNER
  const modal = document.getElementById('emergencyModal');
  const closeBtn = document.getElementById('modalCloseBtn');
  
  if (modal && !sessionStorage.getItem('simpsons_modal_seen')) {
    setTimeout(() => {
      modal.classList.add('active');
    }, 600);
  }

  window.closeModal = function() {
    if (modal) {
      modal.classList.remove('active');
      sessionStorage.setItem('simpsons_modal_seen', 'true');
    }
  };

  if (closeBtn) {
    closeBtn.addEventListener('click', window.closeModal);
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) window.closeModal();
    });
  }

  // 2. FAQ ACCORDIONS
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const btn = item.querySelector('.faq-question');
    if (btn) {
      btn.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        faqItems.forEach(f => f.classList.remove('active'));
        if (!isActive) item.classList.add('active');
      });
    }
  });

  // 3. REVIEWS CAROUSEL SCROLLING
  const track = document.getElementById('reviewsTrack');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');

  if (track && prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -380, behavior: 'smooth' });
    });
    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: 380, behavior: 'smooth' });
    });
  }

  // 4. MOBILE MENU TOGGLE
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenuNav');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('active');
    });
  }
});

// 5. DIRECT WHATSAPP DISPATCH FORM HANDLER
function handleDispatchForm(event) {
  event.preventDefault();
  const name = document.getElementById('custName')?.value || 'Motorist';
  const phone = document.getElementById('custPhone')?.value || '';
  const loc = document.getElementById('breakdownLoc')?.value || '';
  const vehicle = document.getElementById('vehicleType')?.value || '';
  const service = document.getElementById('serviceNeeded')?.value || 'Emergency Breakdown Recovery';
  const dropoff = document.getElementById('dropoffLoc')?.value || 'Not specified';

  const text = `Hello Dean & Simpsons Recovery,\n\nI need immediate recovery assistance in the Birmingham/West Midlands area:\n\n• Name: ${name}\n• Phone: ${phone}\n• Breakdown Location: ${loc}\n• Vehicle Model: ${vehicle}\n• Service Required: ${service}\n• Drop-off Destination: ${dropoff}\n\nPlease confirm your closest truck and fixed price quote.`;

  const url = `https://wa.me/447706057962?text=${encodeURIComponent(text)}`;
  window.open(url, '_blank');
}

// 6. LEGAL / TERMS MODAL HANDLER
function openLegal(title) {
  const modal = document.getElementById('legalModal');
  const header = document.getElementById('legalTitle');
  if (modal && header) {
    header.innerText = title;
    modal.classList.add('active');
  }
}

function closeLegal() {
  const modal = document.getElementById('legalModal');
  if (modal) modal.classList.remove('active');
}
