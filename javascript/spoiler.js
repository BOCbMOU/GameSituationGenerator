{
  const t = document.querySelector('a.toggle-spoiler:hover').parentElement
    .lastChild;
  if (t.style.opacity === '1') {
    const s = t.style;
    s.transition =
      'height 300ms cubic-bezier(.25,.46,.45,.94) 0s, opacity 50ms ease-out 250ms';
    s.opacity = 0;
    s.height = '0px';
  } else {
    const s = t.style;
    s.transition =
      'height 300ms cubic-bezier(.25,.46,.45,.94) 0s, opacity 50ms';
    s.opacity = 1;
    s.height = `${t.scrollHeight - 5}px`;
  }
}
void 0;
