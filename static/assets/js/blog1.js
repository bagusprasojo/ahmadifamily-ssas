// Ambil postingan via Blogger JSON Feed
fetch('https://www.tokoumi.com/feeds/posts/default?alt=json&max-results=5')
  .then(response => response.json())
  .then(data => {
    const posts = data.feed.entry || [];
    const container = document.getElementById('recent-posts');

    posts.forEach(post => {
      const title = post.title.$t;
      const link = post.link.find(l => l.rel === 'alternate').href;
      const content = post.content?.$t || '';

      // Ambil gambar pertama dari isi konten
      let imgSrc = '';
      const imgMatch = content.match(/<img[^>]+src="([^">]+)"/);
      if (imgMatch && imgMatch[1]) {
        imgSrc = imgMatch[1];
      } else {
        imgSrc = 'https://via.placeholder.com/300x200?text=No+Image'; // Fallback jika tidak ada gambar
      }

      // Ambil snippet
      const snippet = content.replace(/<[^>]+>/g, '').substring(0, 100);

      const col = document.createElement('div');
      col.className = 'col-md-6 col-lg-4';

      col.innerHTML = `
        <div class='card h-100 shadow-sm'>
          <img src='${imgSrc}' class='card-img-top' alt='${title}' />
          <div class='card-body'>
            <h5 class='card-title'><a href='${link}'>${title}</a></h5>
            <p class='card-text'>${snippet}...</p>
            <a class='btn btn-sm btn-primary' href='${link}'>Baca Selengkapnya</a>
          </div>
        </div>
      `;

      container.appendChild(col);
    });
  })
  .catch(error => console.error('Gagal memuat postingan:', error));
