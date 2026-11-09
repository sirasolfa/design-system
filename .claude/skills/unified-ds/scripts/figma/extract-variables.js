// use_figma 읽기 전용 스크립트 — 로컬 변수 전체를 원시 JSON 으로 반환한다.
// 사용: use_figma(fileKey=<통합 DS>, code=<이 파일>, skillNames="figma-use")
// 반환값을 build/raw-variables.json 으로 저장한 뒤 `python3 scripts/to_dtcg.py` 에 넣는다.
//
// 값 표현
//   COLOR  → "#RRGGBBAA" (대문자)
//   FLOAT  → number
//   STRING → string
//   BOOLEAN→ boolean
//   alias  → { "alias": "<대상 변수 이름>", "aliasCollection": "<대상 컬렉션 이름>" }

const hex = (c) => {
  const h = (v) => Math.round(v * 255).toString(16).padStart(2, '0').toUpperCase();
  return '#' + h(c.r) + h(c.g) + h(c.b) + h(c.a === undefined ? 1 : c.a);
};

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const colById = Object.fromEntries(collections.map((c) => [c.id, c]));
const cache = {};
const lookup = async (id) => {
  if (!(id in cache)) cache[id] = await figma.variables.getVariableByIdAsync(id);
  return cache[id];
};

const variables = [];
for (const col of collections) {
  const modeName = Object.fromEntries(col.modes.map((m) => [m.modeId, m.name]));
  for (const vid of col.variableIds) {
    const v = await lookup(vid);
    if (!v) continue;
    const values = {};
    for (const [modeId, val] of Object.entries(v.valuesByMode)) {
      let out = val;
      if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') {
        const t = await lookup(val.id);
        out = t
          ? { alias: t.name, aliasCollection: (colById[t.variableCollectionId] || {}).name || '(remote)' }
          : { alias: null, aliasId: val.id };
      } else if (v.resolvedType === 'COLOR') {
        out = hex(val);
      }
      values[modeName[modeId] || modeId] = out;
    }
    variables.push({
      id: v.id,
      name: v.name,
      collection: col.name,
      type: v.resolvedType,
      scopes: v.scopes,
      description: v.description || '',
      hidden: v.hiddenFromPublishing,
      values,
    });
  }
}

return {
  extractedAt: new Date().toISOString(),
  fileKey: figma.fileKey,
  collections: collections.map((c) => ({
    id: c.id, name: c.name, modes: c.modes.map((m) => m.name),
    hidden: c.hiddenFromPublishing, count: c.variableIds.length,
  })),
  variables,
};
