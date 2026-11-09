// use_figma 읽기 전용 — 기록 페이지를 JSON 으로. 페이지 전환은 호출당 1회이므로
// PAGE 를 바꿔 3번(병렬) 호출한다.
//   PAGE = 'Updates'         (통합 DS) → updates.json   : audit_log.py · changelog.py 입력
//   PAGE = 'Progress Board'  (통합 DS) → progress.json  : audit_log.py 입력
//   PAGE = 'Roadmap'         (로드맵)  → roadmap.json   : 현황 갱신(SKILL.md 4.6) 입력

const PAGE = 'Updates';

const page = figma.root.children.find((p) => p.name.includes(PAGE));
await figma.setCurrentPageAsync(page);
const label = (k) => k.split('#')[0];
const textProps = (i) => Object.fromEntries(
  Object.entries(i.componentProperties).filter(([, v]) => v.type === 'TEXT').map(([k, v]) => [label(k), v.value]));
const badge = (i, layer) => {
  const b = i.findOne((n) => n.type === 'INSTANCE' && n.name === layer);
  return b ? Object.values(b.variantProperties || {})[0] : null;
};

if (PAGE === 'Updates') {
  const root = page.children.find((n) => n.type === 'FRAME' && n.name.startsWith('Updates'));
  const entries = [];
  for (const sec of root.children.filter((n) => n.type === 'FRAME' && /^\d{4}\.\d{2}$/.test(n.name))) {
    sec.children.filter((c) => c.type === 'INSTANCE').forEach((i, order) =>
      entries.push({ id: i.id, month: sec.name, order, 유형: badge(i, '유형'), ...textProps(i) }));
  }
  return { page: page.name, entries };
}

if (PAGE === 'Progress Board') {
  const board = page.children.find((n) => n.type === 'FRAME' && n.name === 'Progress Board');
  const rows = [];
  for (const g of board.children.filter((n) => n.type === 'FRAME' && n.children.some((c) => c.type === 'INSTANCE'))) {
    for (const i of g.children.filter((c) => c.type === 'INSTANCE' && c.name === '진행 행'))
      rows.push({ id: i.id, group: g.name, ...textProps(i), 상태: badge(i, '상태'),
        Figma: badge(i, 'Figma'), React: badge(i, 'React'), Flutter: badge(i, 'Flutter') });
  }
  return { page: page.name, rows };
}

// Roadmap — 업무 카드
const cards = page.findAllWithCriteria({ types: ['INSTANCE'] }).filter((i) => i.name === '업무 카드');
return { page: page.name, cards: cards.map((i) => ({ id: i.id, ...textProps(i), 상태: badge(i, '상태') })) };
