document.addEventListener('DOMContentLoaded', () => {
    const askBtn = document.getElementById('askBtn');
    const userQuestionInput = document.getElementById('userQuestion');
    const downloadBtn = document.getElementById('downloadBtn');

    // 1. Soru Gönderme Olayları (Sayfanın yenilenmesi engellendi)
    if (askBtn) {
        askBtn.addEventListener('click', (e) => {
            e.preventDefault();
            sendQueryToServer();
        });
    }

    if (userQuestionInput) {
        userQuestionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendQueryToServer();
            }
        });
    }

    // 2. Tüm FAQ Dosyasını PDF Olarak İndirme Olayı
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async function() {
            try {
                const res = await fetch('/api/all-faq');
                const data = await res.json();

                // faq.md içeriğini satır satır işleyerek soru satırlarını kalın yapalım
                let rawContent = data.content || "";
                let formattedContent = rawContent.split('\n').map(line => {
                    if (line.startsWith('## Soru:') || line.startsWith('Soru:')) {
                        return `<div style="font-weight: bold; color: #7a0be3; margin-top: 10px;">${line}</div>`;
                    } else if (line.startsWith('Cevap:')) {
                        return `<div style="margin-bottom: 8px; color: #333;">${line}</div>`;
                    }
                    return `<div>${line}</div>`;
                }).join('');

                const element = document.createElement('div');
                element.innerHTML = `
                <div style="padding: 25px; font-family: Arial, sans-serif; color: #333;">
                    <h1 style="color: #c30a32; border-bottom: 2px solid #c30a32; padding-bottom: 10px; font-size: 22px;">Ofis ve Staj SSS Tam Rehberi</h1>
                    <p style="color: #2d0303; font-size: 12px;">Tarih: ${new Date().toLocaleDateString('tr-TR')}</p>
                    <hr style="border: none; border-top: 2px solid #ddd; margin: 15px 0;">
                    <div style="line-height: 1.5; font-size: 14px;">
                        ${formattedContent}
                    </div>
                </div>
            `;

                const opt = {
                    margin: 10,
                    filename: 'ofis-staj-tum-faq-rehberi.pdf',
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2, useCORS: true },
                    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                };

                html2pdf().from(element).set(opt).save();
            } catch (err) {
                console.error("PDF indirme hatası:", err);
                alert("Tüm FAQ dosyası indirilirken bir hata oluştu.");
            }
        });
    }
});

// 3. Sunucuya İstek Atan Fonksiyon
async function sendQueryToServer() {
    const queryInput = document.getElementById('userQuestion');
    const responseArea = document.getElementById('chatResponseArea');
    const responseText = document.getElementById('responseText');

    if (!queryInput) return;
    const query = queryInput.value.trim();

    if (!query) {
        alert('Lütfen bir soru yazın.');
        return;
    }

    responseArea.classList.remove('d-none');
    responseText.innerHTML = "<i>Qdrant veritabanında anlamsal arama yapılıyor...</i>";

    try {
        const res = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        if (!res.ok) {
            throw new Error(`Sunucu hatası kodu: ${res.status}`);
        }

        const data = await res.json();

        responseText.innerHTML = `<strong class="text-primary">Eşleşen Soru:</strong> ${data.question || 'Bulunamadı'}<br><br>` +
            `<strong class="text-success">Yanıt:</strong><br>${data.answer}`;
    } catch (err) {
        console.error("Fetch Hatası:", err);
        responseText.innerText = "Sunucu ile bağlantı kurulamadı veya 500 hatası alındı.";
    }
}