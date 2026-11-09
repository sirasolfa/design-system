// use_figma 쓰기 스크립트 — Updates · Changelog 에 "업데이트 항목" 1건 추가.
// 쓰기 작업 1회 = 항목 1건. 최신이 위, 월 섹션(YYYY.MM). 추가만 한다(정정은 새 "변경" 항목).
// 사용: ENTRY 를 채워 use_figma(fileKey=<통합 DS>, skillNames="figma-use") 로 실행.
// Progress Board 갱신은 write-progress.js 를 **별도 호출**로(페이지 전환은 호출당 1회).

const ENTRY = {
  유형: '추가',                      // 추가 · 변경 · 이름변경 · 폐기 · 삭제 · 문서 · 릴리스 · 결정
  날짜: '2026.11.09',                // YYYY.MM.DD — 작업 완료일 또는 배포일
  타이틀: '추가 · 한 줄 요약',        // "유형 · 한 줄 요약"
  상세: '무엇이 어떻게 바뀌었는지. 영향 토큰 · 컴포넌트 목록. 값 변경은 이전 → 새 값, 폐기는 대체 토큰',
  범위: 'Semantic',                  // Primitive / Brand / Semantic / Module / 컴포넌트명 / 문서 페이지명 / 코드(React · Flutter)
  비고: '없음',                      // 버전, 결정 안건 번호, 링크, 후속 조치. 없으면 "없음"
  수정자: 'unified-ds 스킬 (요청자: 이름)',
};

// ── 사전 검증 ────────────────────────────────────────────────
const TYPES = ['추가', '변경', '이름변경', '폐기', '삭제', '문서', '릴리스', '결정'];
const errs = [];
if (!TYPES.includes(ENTRY.유형)) errs.push('유형 어휘 아님: ' + ENTRY.유형);
if (!/^\d{4}\.\d{2}\.\d{2}$/.test(ENTRY.날짜)) errs.push('날짜 형식 YYYY.MM.DD 아님');
if (!ENTRY.타이틀.startsWith(ENTRY.유형 + ' · ')) errs.push('타이틀은 "유형 · 한 줄 요약"');
for (const k of ['상세', '범위', '비고', '수정자']) if (!String(ENTRY[k] || '').trim()) errs.push(k + ' 빈칸');
if (errs.length) throw new Error('ENTRY 검증 실패: ' + errs.join(' / '));

// ── 찾기 (이름으로) ─────────────────────────────────────────
const page = figma.root.children.find((p) => p.name.includes('Updates'));
await figma.setCurrentPageAsync(page);
const comp = page.findOne((n) => n.type === 'COMPONENT' && n.name === '업데이트 항목');
const root = page.children.find((n) => n.type === 'FRAME' && n.name.startsWith('Updates'));
if (!comp || !root) throw new Error('템플릿 컴포넌트 또는 Updates 프레임을 찾지 못함');

const defs = comp.componentPropertyDefinitions;
const key = (label) => Object.keys(defs).find((k) => k.split('#')[0] === label);

const loadFonts = async (node) => {
  for (const t of node.findAllWithCriteria({ types: ['TEXT'] })) {
    for (const s of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(s.fontName);
  }
};

// ── 월 섹션 ────────────────────────────────────────────────
const month = ENTRY.날짜.slice(0, 7);
const created = [];
let sec = root.children.find((n) => n.type === 'FRAME' && n.name === month);
if (!sec) {
  const proto = root.children.find((n) => n.type === 'FRAME' && /^\d{4}\.\d{2}$/.test(n.name));
  if (!proto) throw new Error('복제할 월 섹션이 없음 — 수동으로 하나 만든 뒤 재시도');
  await loadFonts(proto);
  sec = proto.clone();
  for (const c of [...sec.children]) if (c.type === 'INSTANCE') c.remove();
  sec.name = month;
  const title = sec.children.find((c) => c.type === 'TEXT');
  if (title) title.characters = month;
  // 최신 월이 위 — Header 바로 다음
  const months = root.children.filter((n) => n.type === 'FRAME' && /^\d{4}\.\d{2}$/.test(n.name) && n !== sec);
  const after = months.find((m) => m.name < month);
  root.insertChild(after ? root.children.indexOf(after) : root.children.length, sec);
  created.push(sec.id);
}

// ── 항목 ───────────────────────────────────────────────────
const sibling = sec.children.find((c) => c.type === 'INSTANCE');
const inst = comp.createInstance();
const titleIdx = sec.children.findIndex((c) => c.type === 'TEXT');
sec.insertChild(titleIdx + 1, inst);           // 같은 달 안에서도 최신이 위
if (sibling) inst.layoutSizingHorizontal = sibling.layoutSizingHorizontal;
await loadFonts(inst);
const props = {};
for (const f of ['날짜', '타이틀', '상세', '범위', '비고', '수정자']) {
  const k = key(f);
  if (!k) throw new Error('프로퍼티를 찾지 못함: ' + f);
  props[k] = ENTRY[f];
}
inst.setProperties(props);
const badge = inst.findOne((n) => n.type === 'INSTANCE' && n.name === '유형');
if (badge) badge.setProperties({ 유형: ENTRY.유형 });
created.push(inst.id);

return { createdNodeIds: created, month, entryId: inst.id, 타이틀: ENTRY.타이틀, badgeSet: !!badge };
