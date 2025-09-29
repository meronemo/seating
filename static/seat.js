document.addEventListener('DOMContentLoaded', function() {
    // 이미지 업로드 request 전송
    if (stuImg && teaImg) {
        function updateStatus(label, status, message) {
            const statusDiv = document.getElementById('upload-status')
            const statusIcons = {
                success: '✅',
                skipped: '⏭️',
                error: '❌'
            };
            const statusIcon = statusIcons[status];
            statusDiv.innerHTML += `<div>${statusIcon} ${label}: ${message}</div>`;
        }
        
        // 학생용/교사용 이미지 업로드
        [
            { type: 'student', img: stuImg, label: '학생용 이미지' },
            { type: 'teacher', img: teaImg, label: '교사용 이미지' }
        ].forEach(({ type, img, label }) => {
            fetch('/api/upload_image', {
                method: 'POST',
                body: JSON.stringify({
                    date: date,
                    type: type,
                    image_data: img
                })
            })
            .then(response => response.json())
            .then(data => {
                updateStatus(label, data.status, data.message || '업로드 처리됨');
            });
        });
    }
});

// 인쇄 기능
document.getElementById('print-btn').addEventListener('click', function() {
    const btn = this;
    const originalText = btn.innerHTML;
    
    // 로딩 상태 표시
    btn.innerHTML = '⏳ 준비 중...';
    btn.disabled = true;
    btn.classList.add('loading');
    
    // 새 창에서 이미지 표시
    const img = document.getElementById('teacher-img');
    const imgSrc = img.src;
    const newWindow = window.open('', '_blank');
    newWindow.document.head.innerHTML = `
        <style>
            @page { size: landscape; margin: 0; }
            body { 
                margin: 0; display: flex; justify-content: center; align-items: center; 
                height: 100vh; background: #f8f9fa;
            }
            img { 
                max-width: 100%; max-height: 100vh; 
            }
        </style>
    `;
    newWindow.document.body.innerHTML = `<img src="${imgSrc}" alt="자리 배치 교사용 이미지" />`;
    
    // 버튼 상태 복원
    btn.innerHTML = originalText;
    btn.disabled = false;
    btn.classList.remove('loading');
});
