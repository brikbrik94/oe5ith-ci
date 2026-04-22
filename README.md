# OE5ITH CI Repository

Design System für das OE5ITH Cloud Portal.

## Struktur

```
ci-repo/
├── assets/
│   └── logo.svg              # System-Logo (SVG, monochrom blau)
├── components/
│   └── topbar.html           # Generische Referenzseite: Topbar
└── docs/
    └── topbar.md             # Topbar-Spezifikation
```

## Prinzip

Jedes UI-Element besteht aus zwei Dateien:

| Datei | Inhalt |
|---|---|
| `components/<element>.html` | Generische, funktionale Referenzseite mit allen Platzhaltern. Zeigt alle Breakpoints live. |
| `docs/<element>.md` | Vollständige Spezifikation: Tokens, Verhalten, CSS, Accessibility, Seitentypen-Matrix. |

## Workflow

1. Element in `docs/<element>.md` spezifizieren
2. In `components/<element>.html` visuell umsetzen und testen
3. Aus der Referenz in die jeweiligen Site-Templates übertragen

## Status

| Element | Spec | Referenz-HTML |
|---|---|---|
| Topbar | ✅ | ✅ |
| Sidebar | ✅ | ✅ |
| Cards | ✅ | ✅ |
| Buttons | ✅ | ✅ |
| Badges | ✅ | ✅ |
| Typografie | ✅ | ✅ |
| Farben/Tokens | ✅ | ✅ |
