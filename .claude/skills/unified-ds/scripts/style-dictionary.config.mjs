// Style Dictionary v4 설정 — 해석본 4개 → React 용 CSS 변수 + TS 토큰 객체.
//
//   npm i -D style-dictionary@4
//   node scripts/style-dictionary.config.mjs build/resolved dist/react
//
// 출력
//   dist/react/tokens.css   [data-brand="novera"][data-theme="light"] … 4블록 (+ :root = NOVERA·Light)
//   dist/react/tokens.ts    export const tokens = { bg: { neutralSolid: 'var(--bg-neutral-solid)' } } as const
//
// 이름 변환은 scripts/naming.py 와 동일해야 한다(lint.py 패리티 검사가 잡는다).

import StyleDictionary from 'style-dictionary';
import fs from 'node:fs';
import path from 'node:path';

const NS = 'com.unified-ds';
const [, , inDir = 'build/resolved', outDir = 'dist/react'] = process.argv;
const COMBOS = [
  ['novera', 'light'], ['novera', 'dark'], ['1chon', 'light'], ['1chon', 'dark'],
];

// ── naming.py 미러 ──────────────────────────────────────────
const figmaName = (t) => t.$extensions?.[NS]?.name ?? t.path.join('/');
const cssName = (n) => n.replace(/[/.]/g, '-');
const camel = (ws) => {
  const s = ws[0] + ws.slice(1).map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join('');
  return /^\d/.test(s) ? 'n' + s : s;
};
const codeName = (n) => {
  const [g, ...rest] = n.split('/');
  return [camel(g.split('-')), camel(rest.join('-').replace(/\./g, '-').split('-'))];
};

StyleDictionary.registerTransform({
  name: 'name/unified', type: 'name',
  transform: (t) => cssName(figmaName(t)),
});
StyleDictionary.registerTransform({
  name: 'value/unified', type: 'value',
  filter: (t) => ['dimension', 'duration', 'fontFamily'].includes(t.$type ?? t.type),
  transform: (t) => {
    const v = t.$value ?? t.value;
    const type = t.$type ?? t.type;
    if (type === 'dimension') return `${v}px`;
    if (type === 'duration') return `${v}ms`;
    return `'${v}'`;
  },
});
StyleDictionary.registerTransformGroup({
  name: 'unified/css', transforms: ['name/unified', 'value/unified'],
});

StyleDictionary.registerFormat({
  name: 'typescript/unified',
  format: ({ dictionary }) => {
    const groups = {};
    for (const t of dictionary.allTokens) {
      const n = figmaName(t);
      const [g, k] = codeName(n);
      (groups[g] ??= {})[k] = `var(--${cssName(n)})`;
    }
    const body = Object.entries(groups).map(([g, kv]) =>
      `  ${g}: {\n` + Object.entries(kv).map(([k, v]) => `    ${k}: '${v}',`).join('\n') + '\n  },').join('\n');
    return `// 생성 파일 — 수정 금지. 원본은 Figma Variables.\n` +
      `export const tokens = {\n${body}\n} as const;\n\n` +
      `export type Tokens = typeof tokens;\n` +
      `export type Brand = 'novera' | '1chon';\nexport type Theme = 'light' | 'dark';\n`;
  },
});

fs.mkdirSync(outDir, { recursive: true });
const blocks = [];
for (const [brand, theme] of COMBOS) {
  const src = path.join(inDir, `${brand}-${theme}.json`);
  const isDefault = brand === 'novera' && theme === 'light';
  const selector = `${isDefault ? ':root, ' : ''}[data-brand="${brand}"][data-theme="${theme}"]`;
  const tmp = path.join(outDir, `.${brand}-${theme}.css`);
  const files = [{
    destination: path.basename(tmp), format: 'css/variables',
    options: { selector, outputReferences: false, showFileHeader: false },
  }];
  if (isDefault) files.push({ destination: 'tokens.ts', format: 'typescript/unified' });
  const sd = new StyleDictionary({
    source: [src], usesDtcg: true, log: { verbosity: 'silent' },
    platforms: { react: { transformGroup: 'unified/css', buildPath: outDir + '/', files } },
  });
  await sd.buildAllPlatforms();
  blocks.push(fs.readFileSync(tmp, 'utf8'));
  fs.rmSync(tmp);
}
fs.writeFileSync(path.join(outDir, 'tokens.css'),
  '/* 생성 파일 — 수정 금지. 원본은 Figma Variables. */\n' + blocks.join('\n'));
console.log(`${outDir}/tokens.css · tokens.ts`);
