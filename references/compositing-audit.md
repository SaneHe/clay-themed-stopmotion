# Compositing audit

Generated character images often contain useful props already. A later CSS layer can accidentally draw the same prop again, producing a block that looks glued to the character or changes position between scenes.

## Before writing CSS

1. Open every transparent PNG at full size.
2. Write down the visible objects and their owner:

   | Object | Owner | Allowed extra layer |
   | --- | --- | --- |
   | character-held prop | `character.png` | only a named replacement or close-up |
   | character accessory | `character.png` | none unless the source pose changes |
   | landmark/hero object | dedicated PNG | only a deliberate alternate shot |
   | door, machine, set piece | scene HTML/CSS | yes, it belongs to the environment |
   | rain, steam, light, texture | scene HTML/CSS | yes, it belongs to the environment |

3. Give any intentionally separate prop a unique ID and a reason in `ASSET_MANIFEST.md`.
4. Do not add generic `.coffee`, `.bag`, `.card`, or `.shadow` helpers just because a scene needs an object until the source PNG has been checked.

## During layout

- Render a static frame before adding motion. Verify that each prop appears once and is attached to the correct hand, shoulder, or floor position.
- Keep a prop in the same coordinate system as its owner. A fixed `right`/`bottom` overlay will drift when the character moves unless it is intentionally a scene prop.
- If a character PNG already has a hand prop or accessory, animate the character image or edit the source asset; do not animate a second simplified rectangle on top.
- Keep set pieces separate and label them as environment props so they are not mistaken for character artifacts.

## Before delivery

Inspect at least one frame from each scene after the first motion starts and one transition frame. Look specifically for:

- white/brown cup-shaped blocks beside a hand;
- dark blue bags or rectangles under a character;
- repeated landmarks, shadows, wheels, or signs;
- objects that jump because they use a different parent coordinate system;
- development labels such as “Codex preview” on the end card.

If an object cannot be explained by the asset manifest, remove it or name it before exporting. Update the contact sheet after the final render so old artifacts are not mistaken for current output.
