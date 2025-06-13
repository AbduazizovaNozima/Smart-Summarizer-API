document.addEventListener('DOMContentLoaded', function() {
    // DOM elementlarini olish
    const elements = {
        summarizeBtn: document.getElementById('summarize'),
        textArea: document.getElementById('text'),
        summaryContainer: document.getElementById('summary-container'),
        summary: document.getElementById('summary'),
        loading: document.querySelector('.loading'),
        error: document.querySelector('.error')
    };

    // Xulosa qilish funksiyasi
    async function summarizeText() {
        const text = elements.textArea.value.trim();

        // Matn bo'sh ekanligini tekshirish
        if (!text) {
            elements.error.textContent = 'Please enter some text to summarize.';
            return;
        }

        // UI ni yangilash
        elements.error.textContent = '';
        elements.loading.style.display = 'flex';
        elements.summaryContainer.style.display = 'none';
        elements.summarizeBtn.disabled = true;

        try {
            // API ga so'rov yuborish
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            // Xato tekshirish
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate summary');
            }

            // Natijani ko'rsatish
            elements.summary.textContent = data.summary;
            elements.summaryContainer.style.display = 'block';
        } catch (err) {
            elements.error.textContent = err.message;
        } finally {
            elements.loading.style.display = 'none';
            elements.summarizeBtn.disabled = false;
        }
    }

    // Event listener qo'shish
    elements.summarizeBtn.addEventListener('click', summarizeText);
});