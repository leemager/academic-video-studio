# Share the starter, keep personal work separate

This is a **private GitHub template repository**. A private link alone does not grant access. The owner invites each recipient's GitHub account, or provides an authorised archive by another route. Invitations are deliberate actions; Codex should not send them merely because it is preparing a template.

Once someone has access, GitHub's **Use this template** button creates an independent repository. Recommend a new **private** repository for each academic, rather than having everyone push voice and course work to the shared starter. Cloning/ZIP extraction into a separate local folder is also fine. [GitHub's template documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) explains the access model.

[GET-STARTED-FROM-GITHUB.txt](../GET-STARTED-FROM-GITHUB.txt) is the message to paste into Codex before cloning. [STARTER-PROMPT.txt](../STARTER-PROMPT.txt) is the fuller setup request once the folder is open. Codex should handle technical setup; the academic supplies source material and voice, reviews the content, and chooses the output.

## What Git includes

Reusable code, skills, guides, a neutral visual example, licensed fonts and one original transition effect. There is no speaker identity, voice recording, generated speech, real lecture or institution-specific asset.

## What Git excludes by default

- `voices/` personal profiles and recordings.
- `notes/` sources and working material.
- `voiceover/` generated takes and audition selections.
- `projects/` personal project folders, except the neutral example.
- `public/` generated audio/media/auditions, except shared fonts and the effect.
- `.runtime/`, `.venv/`, `.work/`, `renders/` and secrets.

Generated `src/data/*.json` files are ignored except the example. The small registry is tracked and may acquire imports of ignored local projects. **Before pushing reusable code, restore a shareable registry containing only the example in the copy being shared**, preserving the personal working copy; otherwise a fresh clone will reference missing projects. `npm run check-share` detects this. Do not force-add personal material to make the check pass.

Ignored files are not a backup. For transfer of a personal studio, deliberately make a private archive of the necessary sources, original reference, transcript, profile, selected WAVs, manifests and editable project. Exclude installed dependencies/model caches unless needed. Explain who will receive the voice reference before uploading it. A final MP4 usually does not require distributing the clone inputs.

Run `npm run check-share` against the Git index before each template/code push, then review `git diff --cached --stat` and the actual staged files. It catches sensitive locations and known template mistakes, but cannot determine whether arbitrary new text contains confidential information.
