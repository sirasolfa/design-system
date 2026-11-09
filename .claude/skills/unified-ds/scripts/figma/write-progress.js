// use_figma 쓰기 스크립트 — Progress Board 의 "진행 행" 갱신(없으면 생성).
// Updates 항목을 쓴 직후 같은 날짜 · 같은 타이틀로 실행한다.
// 행 식별: `항목` 텍스트 프로퍼티 완전 일치.  null 필드 = 변경 안 함.

const ROWS = [
  {
    항목: 'Semantic 컬러',
    종류: '토큰',                    // 토큰 / 컴포넌트 / 문서 / 코드
    담당자: '이름',
    '최종 갱신일': '2026.11.09',     // = Updates 항목 날짜
    링크: '추가 · 한 줄 요약',        // = 최근 Updates 항목 타이틀
    상태: '진행중',                  // 예정 · 진행중 · 완료 · 보류
    Figma: '반영',                   // 미착수 · 진행 · 반영 · 검증 완료
    React: null,
    Flutter: null,
  },
];

const STATUS = ['예정', '진행중', '완료', '보류'];
const PLATFORM = ['미착수', '진행', '반영', '검증 완료'];
const KINDS = { 토큰: 'Foundation — 토큰', 컴포넌트: '컴포넌트', 문서: '문서 · 코드', 코드: '문서 · 코드' };
for (const r of ROWS) {
  if (r.상태 != null && !STATUS.includes(r.상태)) throw new Error('상태 어휘 아님: ' + r.상태);
  for (const p of ['Figma', 'React', 'Flutter'])
    if (r[p] != null && !PLATFORM.includes(r[p])) throw new Error(p + ' 상태 어휘 아님: ' + r[p]);
  if (!/^\d{4}\.\d{2}\.\d{2}$/.test(r['최종 갱신일'])) throw new Error('최종 갱신일 형식');
  if (!r.링크) throw new Error('링크(최근 Updates 타이틀) 빈칸');
}

const page = figma.root.children.find((p) => p.name.includes('Progress Board'));
await figma.setCurrentPageAsync(page);
const comp = page.findOne((n) => n.type === 'COMPONENT' && n.name === '진행 행');
const board = page.children.find((n) => n.type === 'FRAME' && n.name === 'Progress Board');
if (!comp || !board) throw new Error('진행 행 컴포넌트 또는 Progress Board 프레임 없음');
const defs = comp.componentPropertyDefinitions;
const key = (label) => Object.keys(defs).find((k) => k.split('#')[0] === label);
const loadFonts = async (node) => {
  for (const t of node.findAllWithCriteria({ types: ['TEXT'] }))
    for (const s of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(s.fontName);
};

const rows = board.findAllWithCriteria({ types: ['INSTANCE'] }).filter((i) => i.name === '진행 행');
const itemKey = key('항목');
const result = { createdNodeIds: [], mutatedNodeIds: [] };

for (const r of ROWS) {
  let inst = rows.find((i) => i.componentProperties[itemKey]?.value === r.항목);
  if (!inst) {
    const group = board.children.find((n) => n.type === 'FRAME' && n.name === KINDS[r.종류]);
    if (!group) throw new Error('종류 그룹 프레임 없음: ' + r.종류);
    const sibling = group.children.find((c) => c.type === 'INSTANCE');
    inst = comp.createInstance();
    group.appendChild(inst);
    if (sibling) inst.layoutSizingHorizontal = sibling.layoutSizingHorizontal;
    result.createdNodeIds.push(inst.id);
  } else {
    result.mutatedNodeIds.push(inst.id);
  }
  await loadFonts(inst);
  const props = {};
  for (const f of ['항목', '종류', '담당자', '최종 갱신일', '링크']) if (r[f] != null) props[key(f)] = r[f];
  inst.setProperties(props);
  const set = (layer, prop, v) => {
    if (v == null) return;
    const b = inst.findOne((n) => n.type === 'INSTANCE' && n.name === layer);
    if (!b) throw new Error('뱃지 레이어 없음: ' + layer);
    b.setProperties({ [prop]: v });
  };
  set('상태', '상태', r.상태);
  for (const p of ['Figma', 'React', 'Flutter']) set(p, '플랫폼 상태', r[p]);
}
return result;
