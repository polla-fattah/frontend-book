# Modern Front-End Engineering

*From Browser Fundamentals to Production Architecture*

This repository is the complete Hugo website for the front-end architecture and engineering book.

It is intentionally one site:

```text
new-lectures/
├── content/book/        chapter and appendix manuscript
├── content/slides/      lecture decks for each chapter
├── content/playground/  practical exercises and labs
├── layouts/             site presentation and Hugo templates
├── assets/              styles, scripts, and slide assets
├── static/              local fonts and static files
└── hugo.yaml            the site configuration
```

The presentation layer is part of this website. There is no separate theme dependency or `themes/` directory.

## Run locally

From the repository root:

```powershell
hugo server --source .
```

Build the complete site:

```powershell
hugo --source . --cleanDestinationDir
```

The Playground contains exercise briefs only. Implementation code for those exercises will live in a separate repository in a later phase.

## Main sections

- `/book` - the complete manuscript;
- `/slides` - chapter lecture decks;
- `/playground` - practical chapter exercises.
