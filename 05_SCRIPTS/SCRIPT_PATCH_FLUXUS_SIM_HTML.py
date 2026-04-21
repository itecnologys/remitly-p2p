# -*- coding: utf-8 -*-
"""Injeta FLUXUS (i18n, dados fixos, mounts) nas páginas HTML da simulação."""
from __future__ import annotations

import re
from pathlib import Path

CRITSO = Path(__file__).resolve().parents[1] / "09_ Simulacao web" / "fluxus"

HEADER_BLOCK = """                                <div class="button-show-hide">
                                    <i class="icon-menu"></i>
                                </div>
                                <h6>Dashboard</h6>
                                <form class="form-search flex-grow">"""

HEADER_BLOCK_NEW = """                                <div class="button-show-hide">
                                    <i class="icon-menu"></i>
                                </div>
                                <h6 data-i18n="header_dashboard">Dashboard</h6>
                                <div id="fluxus-lang-mount" class="ms-2 d-flex align-items-center flex-shrink-0"></div>
                                <form class="form-search flex-grow">"""

SCRIPTS = """    <script src="js/fluxus-i18n-data.js"></script>
    <script src="js/fluxus-sim-data.js"></script>
    <script src="js/fluxus-app.js"></script>
    <script src="js/main.js"></script>"""

DISCLAIMER_AFTER = """                    <!-- /header-dashboard -->
                    <div class="tf-container py-2"><div id="fluxus-disclaimer-mount"></div></div>
                    <!-- main-content -->"""

DISCLAIMER_BEFORE = """                    <!-- /header-dashboard -->
                    <!-- main-content -->"""


def patch_one(text: str) -> str:
    if "fluxus-app.js" in text:
        return text

    text = text.replace(
        "<title>Shared By NULLPHPSCRIPT.COM - Critso - Crypto Dashboard Template</title>",
        "<title>FLUXUS — Simulation</title>",
        1,
    )

    text = text.replace(HEADER_BLOCK, HEADER_BLOCK_NEW, 1)

    text = text.replace(
        '<div class="center-heading f14-regular text-Gray menu-heading mb-12">Navigation</div>',
        '<div class="center-heading f14-regular text-Gray menu-heading mb-12" data-i18n="nav_section">Navigation</div>',
        1,
    )

    text = re.sub(
        r'(<a href="index\.html" class="menu-item-button[^"]*">\s*<div class="icon">[\s\S]*?</div>\s*)<div class="text">Dashboard</div>',
        r'\1<div class="text" data-i18n="nav_dashboard">Dashboard</div>',
        text,
        count=1,
    )

    text = re.sub(
        r'(<a href="javascript:void\(0\);" class="menu-item-button">\s*<div class="icon">\s*<i class="icon-wallet1"></i>\s*</div>\s*)<div class="text">My Wallet</div>',
        r'\1<div class="text" data-i18n="nav_wallet">My Wallet</div>',
        text,
        count=1,
    )

    text = text.replace(
        '<a href="my-wallet.html" class="">\n                                                    <div class="text">My Wallet</div>',
        '<a href="my-wallet.html" class="">\n                                                    <div class="text" data-i18n="nav_wallet">My Wallet</div>',
        1,
    )
    text = text.replace(
        '<a href="account.html" class="">\n                                                    <div class="text">Account</div>',
        '<a href="account.html" class="">\n                                                    <div class="text" data-i18n="nav_account">Account</div>',
        1,
    )

    text = re.sub(
        r'(<a href="transaction\.html" class="menu-item-button[^"]*">\s*[\s\S]*?</div>\s*)<div class="text">Transaction</div>',
        r'\1<div class="text" data-i18n="nav_transactions">Transaction</div>',
        text,
        count=1,
    )

    text = re.sub(
        r'(<a href="crypto\.html" class="menu-item-button[^"]*">\s*<div class="icon">[\s\S]*?</div>\s*)<div class="text">Crypto</div>',
        r'\1<div class="text" data-i18n="nav_routes">Crypto</div>',
        text,
        count=1,
    )

    text = re.sub(
        r'(<a href="exchange\.html" class="menu-item-button[^"]*">\s*<div class="icon">[\s\S]*?</div>\s*)<div class="text">Exchange</div>',
        r'\1<div class="text" data-i18n="nav_fx">Exchange</div>',
        text,
        count=1,
    )

    text = re.sub(
        r'(<a href="settings\.html" class="menu-item-button[^"]*">\s*<div class="icon">[\s\S]*?</div>\s*)<div class="text">Settings</div>',
        r'\1<div class="text" data-i18n="nav_settings">Settings</div>',
        text,
        count=1,
    )

    text = re.sub(
        r'(<a href="component\.html" class="menu-item-button[^"]*">\s*<div class="icon">[\s\S]*?</div>\s*)<div class="text">Component</div>',
        r'\1<div class="text" data-i18n="nav_components">Component</div>',
        text,
        count=1,
    )

    text = text.replace(
        '<p class="f12-regular text-White">For more features</p>\n                                <p class="f12-bold text-White">Upgrade to Pro</p>',
        '<p class="f12-regular text-White" data-i18n="upgrade_title">For more features</p>\n                                <p class="f12-bold text-White" data-i18n="upgrade_line">Upgrade to Pro</p>',
        1,
    )

    text = text.replace(DISCLAIMER_BEFORE, DISCLAIMER_AFTER, 1)

    text = text.replace(
        '<script src="js/main.js"></script>',
        SCRIPTS,
        1,
    )

    return text


def main() -> None:
    n = 0
    for f in sorted(CRITSO.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        if "section-menu-left" not in raw:
            continue
        new = patch_one(raw)
        if new != raw:
            f.write_text(new, encoding="utf-8")
            n += 1
            print("patched", f.name)
    print("done", n, "files")


if __name__ == "__main__":
    main()
