$(document).ready(function() {
    // Override styles of the footnotes.
    document.querySelectorAll("d-footnote").forEach(function(footnote) {
        if (footnote.shadowRoot) {
            const span = footnote.shadowRoot.querySelector("sup > span");
            if (span) span.setAttribute("style", "color: var(--global-theme-color);");

            const hoverBox = footnote.shadowRoot.querySelector("d-hover-box");
            if (hoverBox && hoverBox.shadowRoot) {
                const style = hoverBox.shadowRoot.querySelector("style");
                if (style && style.sheet) {
                    style.sheet.insertRule(".panel {background-color: var(--global-bg-color) !important;}");
                    style.sheet.insertRule(".panel {border-color: var(--global-divider-color) !important;}");
                }
            }
        }
    });
    // Override styles of the citations.
    document.querySelectorAll("d-cite").forEach(function(cite) {
        if (cite.shadowRoot) {
            const span = cite.shadowRoot.querySelector("div > span");
            if (span) span.setAttribute("style", "color: var(--global-theme-color);");

            const style = cite.shadowRoot.querySelector("style");
            if (style && style.sheet) {
                style.sheet.insertRule("ul li a {color: var(--global-text-color) !important; text-decoration: none;}");
                style.sheet.insertRule("ul li a:hover {color: var(--global-theme-color) !important;}");
            }

            const hoverBox = cite.shadowRoot.querySelector("d-hover-box");
            if (hoverBox && hoverBox.shadowRoot) {
                const hoverStyle = hoverBox.shadowRoot.querySelector("style");
                if (hoverStyle && hoverStyle.sheet) {
                    hoverStyle.sheet.insertRule(".panel {background-color: var(--global-bg-color) !important;}");
                    hoverStyle.sheet.insertRule(".panel {border-color: var(--global-divider-color) !important;}");
                }
            }
        }
    });
})