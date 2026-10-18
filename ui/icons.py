"""One custom line icon per page (inline SVG, no emoji, no network).
`icon(name, size)` returns an SVG string. `MATERIAL` maps each page to a Material Symbols name for
Streamlit's own menu (st.Page(icon=":material/...:")), which is also emoji-free."""

_P = {
    "home": '<path d="M32 6 L54 15 V32 C54 45 45 54 32 58 C19 54 10 45 10 32 V15 Z"/><path d="M22 32 L29 39 L43 24"/>',
    "federation": '<circle cx="32" cy="32" r="7"/><circle cx="12" cy="14" r="6"/><circle cx="52" cy="14" r="6"/><circle cx="32" cy="55" r="6"/>'
                  '<path d="M17 18 L27 27 M47 18 L37 27 M32 39 V49"/>',
    "privacy": '<rect x="13" y="28" width="38" height="28" rx="6"/><path d="M21 28 V20 a11 11 0 0 1 22 0 V28"/><circle cx="32" cy="42" r="3.5"/><path d="M32 45 V50"/>',
    "secure": '<rect x="8" y="8" width="20" height="20" rx="4"/><rect x="36" y="8" width="20" height="20" rx="4"/><rect x="8" y="36" width="20" height="20" rx="4"/>'
              '<path d="M36 46 H56 M46 36 V56"/>',
    "alerts": '<path d="M14 46 V30 a18 18 0 0 1 36 0 V46"/><path d="M8 46 H56 V54 H8 Z"/><path d="M32 6 V10 M12 12 L15 15 M52 12 L49 15"/><path d="M25 40 V32 a7 7 0 0 1 7 -7"/>',
    "laundering": '<circle cx="32" cy="10" r="5"/><circle cx="10" cy="40" r="5"/><circle cx="54" cy="40" r="5"/><circle cx="32" cy="56" r="4"/>'
                  '<path d="M29 14 L13 36 M35 14 L51 36 M15 41 L27 54 M49 41 L37 54 M15 40 H49"/>',
    "data": '<ellipse cx="32" cy="14" rx="20" ry="8"/><path d="M12 14 V32 C12 36 21 40 32 40 C43 40 52 36 52 32 V14"/><path d="M12 32 V50 C12 54 21 58 32 58 C43 58 52 54 52 50 V32"/>',
    "linuxone": '<rect x="14" y="6" width="36" height="52" rx="4"/><path d="M14 22 H50 M14 38 H50"/><circle cx="22" cy="14" r="1.8"/><circle cx="22" cy="30" r="1.8"/><circle cx="22" cy="46" r="1.8"/><path d="M30 14 H42 M30 30 H42 M30 46 H42"/>',
}

# Material Symbols names used by st.Page / st.page_link / set_page_config
MATERIAL = {
    "home": ":material/shield:", "federation": ":material/hub:", "privacy": ":material/lock:",
    "secure": ":material/encrypted:", "alerts": ":material/notification_important:",
    "laundering": ":material/account_tree:", "data": ":material/database:", "linuxone": ":material/dns:",
}


def icon(name, size=40, color="currentColor", stroke=3):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')
