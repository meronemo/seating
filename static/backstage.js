// 템플릿 복제해서 image 아이템 생성
function createImageItem(imageData) {
    const gallery = document.getElementById('gallery');
	const template = document.getElementById('image-template');
	const clone = template.cloneNode(true);
	clone.removeAttribute('id');
	clone.style.display = 'block';
	clone.querySelector('.image-name').textContent = imageData.pathname;
	clone.querySelector('.image-placeholder').innerHTML = `<img src="${imageData.url}" class="actual-image" alt="${imageData.pathname}">`;
	
	// 공유 버튼에 클릭 이벤트 추가
	const shareBtn = clone.querySelector('.btn-share');
	shareBtn.onclick = () => shareImage(imageData.url, imageData.pathname);
	
    gallery.appendChild(clone);
}

function shareImage(url, name) {
    const displayName = name.substring(2, 4) + '/' + name.substring(4, 6) + ' 자리 배치 결과';
    Kakao.Share.sendCustom({
        templateId: 124702,
        templateArgs: {
            url: url,
            title: displayName,
            path: name
        }
    });
}

Kakao.init(KAKAO_API_KEY);

fetch('/api/get_images')
    .then(res => res.json())
    .then(data => {
        data.forEach(imageData => {
            createImageItem(imageData);
        });
    });

