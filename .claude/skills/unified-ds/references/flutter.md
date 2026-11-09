# Flutter 생성 규칙

## 출력

`tokens.g.dart` 하나:

| 생성물 | 용도 |
|---|---|
| `{Group}Tokens` (BgTokens · FgTokens · StrokeTokens · CommerceTokens · SpacingTokens · RadiusTokens · FontTokens …) | 그룹별 필드 |
| `AppTokens extends ThemeExtension<AppTokens>` | 묶음. `lerp` 로 테마 전환 애니메이션 |
| `AppTokens.noveraLight` · `noveraDark` · `n1chonLight` · `n1chonDark` | 브랜드 · 테마별 인스턴스 |
| `AppTokens.of('1chon', Brightness.dark)` | 문자열 브랜드로 선택 |
| `context.tokens` | `Theme.of(context).extension<AppTokens>()` |
| `context.motionDuration(d)` | Motion Reduced 대응 |
| `AppTextScale.s100 … s135` | Typography 스케일 모드 |

> 브랜드 `1chon` 은 숫자로 시작해 Dart 식별자 규칙상 `n1chon` 이 된다(naming.md 규칙 5와 같은 `n` 접두사).

```dart
MaterialApp(
  theme: ThemeData(extensions: [AppTokens.noveraLight]),
  darkTheme: ThemeData(extensions: [AppTokens.noveraDark]),
);

Container(
  color: context.tokens.bg.neutralSolid,
  padding: EdgeInsets.all(context.tokens.spacing.n16),
  child: Text('구매', style: TextStyle(color: context.tokens.fg.neutralContrast)),
);
```

## 원칙

- **이름은 Figma 와 동일.** `ColorScheme` 에 끼워 맞추지 않는다(`primary` · `onSurface` 로 매핑 금지).
- 색 · 간격 · 라디우스 · 타이포를 ThemeExtension 으로.
- **타이포 역할 6종 → `TextTheme`** 으로 매핑한다. 역할 이름은 Typography 컬렉션이 생기면 확정 `[?]`
  (NDS 의 Title · Body · Caption · Action · Subtitle 등과 1CHON 의 체계를 감사한 뒤).
- **font-size 스케일 모드 → `TextScaler`**: `MediaQuery(data: …copyWith(textScaler: TextScaler.linear(AppTextScale.s120)))`.
  토큰은 100% 값만 생성한다.
- **Motion Reduced → `MediaQuery.disableAnimations`**: 모든 애니메이션 시간은 `context.motionDuration(…)` 을 거친다.

## 파이프라인

```bash
python3 scripts/resolve_tokens.py tokens.json -o build/resolved
python3 scripts/gen_dart.py build/resolved -o dist/flutter/lib/tokens.g.dart
dart format dist/flutter/lib/tokens.g.dart     # Flutter SDK 가 있을 때
```

## 컴포넌트

이름은 `App` 접두사(`AppButton`). 생성자 인자 이름 · 값 = Figma 변형. [recipes.md](recipes.md) 스텁 참고.
