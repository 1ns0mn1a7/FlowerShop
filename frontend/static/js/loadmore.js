const button = document.getElementById('loadMoreBtn');
const block = document.getElementById('catalogBlock') || document.querySelector('.catalog__block');

if (button && block) {
  let current = Number(button.dataset.current || 1);
  const total = Number(button.dataset.total || 1);
  let loading = false;

  button.addEventListener('click', async () => {
    if (loading) return;
    const next = current + 1;
    if (next > total) { button.remove(); return; }

    loading = true;
    button.disabled = true;

    try {
      const url = new URL(window.location.href);
      url.searchParams.set('page', String(next));

      const res = await fetch(url.toString(), { headers: { 'X-Requested-With': 'fetch' } });
      if (!res.ok) throw new Error('Bad response');

      const html = await res.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');

      const rows = doc.querySelectorAll('.catalog__block > .recommended__elems');
      if (!rows.length) throw new Error('No rows found');

      rows.forEach(row => block.insertBefore(row, button));

      current = next;
      button.dataset.current = String(current);
      if (current >= total) button.remove();
    } catch (_) {
      window.location.assign(`?page=${current + 1}`);
    } finally {
      if (document.body.contains(button)) button.disabled = false;
      loading = false;
    }
  });
}
