# Hybrid PLS animation (vendored)

`index.html`, `animation_data.js` and `hybridpls-demo.gif` are copies of the `animation/` folder in
<https://github.com/Jong-Min-Moon/FShybridPLS>, so that `_software/hybrid-pls.md` can embed the interactive
version from this site instead of depending on the package repository's Pages deployment.

Re-copy the three files after changing the animation upstream. The only local modification is an `?embed=1`
URL parameter (a `body.embed` CSS rule plus two lines in `boot()`), which hides the standalone page's
title and tagline so the figure fits inside the landing page; `_software/hybrid-pls.md` loads the iframe with
that parameter.
