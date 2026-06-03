#!/usr/bin/env python3
"""Single source of truth for the security & pentesting collection.

Edit CATALOG below, then run `python scripts/build_security.py` to regenerate
both security/security.html (browser-importable) and security/README.md
(human-readable mirror). The website (scripts/build_site.py) reads the HTML,
so the live site updates from the same source.

Adding a tool is a one-line edit to CATALOG — no need to keep two files in
sync by hand. Run scripts/check_links.py afterwards to validate the URLs.
"""

from __future__ import annotations

import html
from pathlib import Path

WRAPPER = "Security & Pentesting"

# Public URL where the searchable site is published (e.g. GitHub Pages). Leave
# empty to omit the "browse the live site" link and point readers to the local
# docs/index.html instead. Set this once the site has a stable home.
SITE_URL = ""

# Ordered catalog: category -> [(name, url), ...]. Curated, reputable tools and
# references across the offensive/defensive workflow. Keep names recognizable
# and prefer official sites or canonical source repos.
CATALOG: dict[str, list[tuple[str, str]]] = {
    "Reconnaissance & OSINT": [
        ("Nmap", "https://nmap.org/"),
        ("Masscan", "https://github.com/robertdavidgraham/masscan"),
        ("Naabu", "https://github.com/projectdiscovery/naabu"),
        ("Shodan", "https://www.shodan.io/"),
        ("Censys Search", "https://search.censys.io/"),
        ("OWASP Amass", "https://github.com/owasp-amass/amass"),
        ("Subfinder", "https://github.com/projectdiscovery/subfinder"),
        ("Sublist3r", "https://github.com/aboul3la/Sublist3r"),
        ("assetfinder", "https://github.com/tomnomnom/assetfinder"),
        ("httpx", "https://github.com/projectdiscovery/httpx"),
        ("dnsx", "https://github.com/projectdiscovery/dnsx"),
        ("Katana", "https://github.com/projectdiscovery/katana"),
        ("gau", "https://github.com/lc/gau"),
        ("waybackurls", "https://github.com/tomnomnom/waybackurls"),
        ("theHarvester", "https://github.com/laramies/theHarvester"),
        ("Recon-ng", "https://github.com/lanmaster53/recon-ng"),
        ("SpiderFoot", "https://www.spiderfoot.net/"),
        ("Maltego", "https://www.maltego.com/"),
        ("OSINT Framework", "https://osintframework.com/"),
        ("gowitness", "https://github.com/sensepost/gowitness"),
        ("Aquatone", "https://github.com/michenriksen/aquatone"),
    ],
    "Web Application Testing": [
        ("Burp Suite (PortSwigger)", "https://portswigger.net/burp"),
        ("Caido", "https://caido.io/"),
        ("OWASP ZAP", "https://www.zaproxy.org/"),
        ("sqlmap", "https://sqlmap.org/"),
        ("Nikto", "https://github.com/sullo/nikto"),
        ("ffuf", "https://github.com/ffuf/ffuf"),
        ("feroxbuster", "https://github.com/epi052/feroxbuster"),
        ("Gobuster", "https://github.com/OJ/gobuster"),
        ("dirsearch", "https://github.com/maurosoria/dirsearch"),
        ("Nuclei", "https://github.com/projectdiscovery/nuclei"),
        ("WPScan", "https://wpscan.com/"),
        ("Dalfox", "https://github.com/hahwul/dalfox"),
        ("XSStrike", "https://github.com/s0md3v/XSStrike"),
        ("Commix", "https://github.com/commixproject/commix"),
        ("Wfuzz", "https://github.com/xmendez/wfuzz"),
        ("Arjun", "https://github.com/s0md3v/Arjun"),
        ("ParamSpider", "https://github.com/devanshbatham/ParamSpider"),
        ("jwt_tool", "https://github.com/ticarpi/jwt_tool"),
        ("testssl.sh", "https://github.com/drwetter/testssl.sh"),
    ],
    "API Security": [
        ("OWASP API Security Top 10", "https://owasp.org/www-project-api-security/"),
        ("Kiterunner", "https://github.com/assetnote/kiterunner"),
        ("Akto", "https://github.com/akto-api-security/akto"),
        ("mitmproxy", "https://mitmproxy.org/"),
    ],
    "Cloud Security": [
        ("Prowler", "https://github.com/prowler-cloud/prowler"),
        ("ScoutSuite", "https://github.com/nccgroup/ScoutSuite"),
        ("Pacu", "https://github.com/RhinoSecurityLabs/pacu"),
        ("CloudFox", "https://github.com/BishopFox/cloudfox"),
        ("Cartography", "https://github.com/lyft/cartography"),
        ("ROADtools", "https://github.com/dirkjanm/ROADtools"),
        ("MicroBurst", "https://github.com/NetSPI/MicroBurst"),
        ("stratus-red-team", "https://github.com/DataDog/stratus-red-team"),
        ("Steampipe", "https://github.com/turbot/steampipe"),
        ("PMapper", "https://github.com/nccgroup/PMapper"),
    ],
    "Container & Kubernetes": [
        ("Trivy", "https://github.com/aquasecurity/trivy"),
        ("Grype", "https://github.com/anchore/grype"),
        ("Syft", "https://github.com/anchore/syft"),
        ("kube-hunter", "https://github.com/aquasecurity/kube-hunter"),
        ("kube-bench", "https://github.com/aquasecurity/kube-bench"),
        ("Kubescape", "https://github.com/kubescape/kubescape"),
        ("kubeaudit", "https://github.com/Shopify/kubeaudit"),
        ("Falco", "https://github.com/falcosecurity/falco"),
        ("Peirates", "https://github.com/inguardians/peirates"),
        ("Docker Bench Security", "https://github.com/docker/docker-bench-security"),
    ],
    "Mobile Security": [
        ("MobSF", "https://github.com/MobSF/Mobile-Security-Framework-MobSF"),
        ("Frida", "https://frida.re/"),
        ("Objection", "https://github.com/sensepost/objection"),
        ("Apktool", "https://apktool.org/"),
        ("jadx", "https://github.com/skylot/jadx"),
        ("Androguard", "https://github.com/androguard/androguard"),
        ("Drozer", "https://github.com/WithSecureLabs/drozer"),
        ("OWASP MASTG", "https://mas.owasp.org/"),
    ],
    "Exploitation & C2": [
        ("Metasploit", "https://www.metasploit.com/"),
        ("Exploit Database", "https://www.exploit-db.com/"),
        ("Packet Storm", "https://packetstormsecurity.com/"),
        ("Impacket", "https://github.com/fortra/impacket"),
        ("Sliver C2", "https://github.com/BishopFox/sliver"),
        ("Havoc", "https://github.com/HavocFramework/Havoc"),
        ("Mythic", "https://github.com/its-a-feature/Mythic"),
        ("PoshC2", "https://github.com/nettitude/PoshC2"),
        ("Empire", "https://github.com/BC-SECURITY/Empire"),
        ("Villain", "https://github.com/t3l3machus/Villain"),
    ],
    "Privilege Escalation": [
        ("PEASS-ng (winPEAS/linPEAS)", "https://github.com/peass-ng/PEASS-ng"),
        ("LinEnum", "https://github.com/rebootuser/LinEnum"),
        ("linux-smart-enumeration", "https://github.com/diego-treitos/linux-smart-enumeration"),
        ("pspy", "https://github.com/DominicBreuker/pspy"),
        ("Seatbelt", "https://github.com/GhostPack/Seatbelt"),
        ("PrivescCheck", "https://github.com/itm4n/PrivescCheck"),
        ("BeRoot", "https://github.com/AlessandroZ/BeRoot"),
    ],
    "Passwords & Credentials": [
        ("Hashcat", "https://hashcat.net/hashcat/"),
        ("John the Ripper", "https://www.openwall.com/john/"),
        ("THC Hydra", "https://github.com/vanhauser-thc/thc-hydra"),
        ("Medusa", "https://github.com/jmk-foofus/medusa"),
        ("Have I Been Pwned", "https://haveibeenpwned.com/"),
        ("CrackStation", "https://crackstation.net/"),
        ("Name-That-Hash", "https://github.com/HashPals/Name-That-Hash"),
        ("hashID", "https://github.com/psypanda/hashID"),
        ("CeWL", "https://github.com/digininja/CeWL"),
        ("Mentalist", "https://github.com/sc0tfree/mentalist"),
    ],
    "Active Directory & Post-Exploitation": [
        ("BloodHound", "https://github.com/SpecterOps/BloodHound"),
        ("NetExec", "https://github.com/Pennyw0rth/NetExec"),
        ("Mimikatz", "https://github.com/gentilkiwi/mimikatz"),
        ("Rubeus", "https://github.com/GhostPack/Rubeus"),
        ("Certipy", "https://github.com/ly4k/Certipy"),
        ("Responder", "https://github.com/lgandx/Responder"),
        ("Kerbrute", "https://github.com/ropnop/kerbrute"),
        ("PowerSploit", "https://github.com/PowerShellMafia/PowerSploit"),
        ("ADRecon", "https://github.com/adrecon/ADRecon"),
        ("PingCastle", "https://www.pingcastle.com/"),
        ("Coercer", "https://github.com/p0dalirius/Coercer"),
        ("ldapdomaindump", "https://github.com/dirkjanm/ldapdomaindump"),
        ("Snaffler", "https://github.com/SnaffCon/Snaffler"),
        ("BloodHound.py", "https://github.com/dirkjanm/BloodHound.py"),
    ],
    "Network & Wireless": [
        ("Wireshark", "https://www.wireshark.org/"),
        ("tcpdump", "https://www.tcpdump.org/"),
        ("Bettercap", "https://www.bettercap.org/"),
        ("Aircrack-ng", "https://www.aircrack-ng.org/"),
        ("Kismet", "https://www.kismetwireless.net/"),
        ("Wifite2", "https://github.com/derv82/wifite2"),
        ("Reaver", "https://github.com/t6x/reaver-wps-fork-t6x"),
        ("EAPHammer", "https://github.com/s0lst1c3/eaphammer"),
    ],
    "Code, Secrets & Supply Chain": [
        ("Semgrep", "https://github.com/semgrep/semgrep"),
        ("CodeQL", "https://codeql.github.com/"),
        ("Bandit", "https://github.com/PyCQA/bandit"),
        ("Gitleaks", "https://github.com/gitleaks/gitleaks"),
        ("TruffleHog", "https://github.com/trufflesecurity/trufflehog"),
        ("detect-secrets", "https://github.com/Yelp/detect-secrets"),
        ("git-secrets", "https://github.com/awslabs/git-secrets"),
        ("OSV-Scanner", "https://github.com/google/osv-scanner"),
        ("OWASP Dependency-Check", "https://github.com/jeremylong/DependencyCheck"),
        ("Checkov", "https://github.com/bridgecrewio/checkov"),
        ("tfsec", "https://github.com/aquasecurity/tfsec"),
        ("Dependency-Track", "https://github.com/DependencyTrack/dependency-track"),
    ],
    "Fuzzing": [
        ("AFL++", "https://github.com/AFLplusplus/AFLplusplus"),
        ("libFuzzer", "https://llvm.org/docs/LibFuzzer.html"),
        ("honggfuzz", "https://github.com/google/honggfuzz"),
        ("boofuzz", "https://github.com/jtpereyda/boofuzz"),
        ("radamsa", "https://gitlab.com/akihe/radamsa"),
        ("Atheris", "https://github.com/google/atheris"),
        ("RESTler", "https://github.com/microsoft/restler-fuzzer"),
    ],
    "Forensics & Reverse Engineering": [
        ("Ghidra", "https://ghidra-sre.org/"),
        ("IDA Free", "https://hex-rays.com/ida-free/"),
        ("Cutter", "https://cutter.re/"),
        ("radare2", "https://rada.re/n/"),
        ("x64dbg", "https://x64dbg.com/"),
        ("pwndbg", "https://github.com/pwndbg/pwndbg"),
        ("GEF", "https://github.com/hugsy/gef"),
        ("angr", "https://angr.io/"),
        ("dnSpy", "https://github.com/dnSpy/dnSpy"),
        ("capa", "https://github.com/mandiant/capa"),
        ("YARA", "https://github.com/VirusTotal/yara"),
        ("FLARE FLOSS", "https://github.com/mandiant/flare-floss"),
        ("Detect It Easy", "https://github.com/horsicq/Detect-It-Easy"),
        ("Volatility 3", "https://github.com/volatilityfoundation/volatility3"),
        ("Autopsy", "https://www.autopsy.com/"),
        ("Velociraptor", "https://github.com/Velocidex/velociraptor"),
        ("CyberChef", "https://gchq.github.io/CyberChef/"),
    ],
    "Threat Intelligence": [
        ("VirusTotal", "https://www.virustotal.com/"),
        ("urlscan.io", "https://urlscan.io/"),
        ("AbuseIPDB", "https://www.abuseipdb.com/"),
        ("AlienVault OTX", "https://otx.alienvault.com/"),
        ("GreyNoise", "https://www.greynoise.io/"),
        ("MISP", "https://www.misp-project.org/"),
        ("OpenCTI", "https://www.opencti.io/"),
        ("TheHive", "https://github.com/TheHive-Project/TheHive"),
        ("MalwareBazaar", "https://bazaar.abuse.ch/"),
        ("URLhaus", "https://urlhaus.abuse.ch/"),
        ("ThreatFox", "https://threatfox.abuse.ch/"),
        ("Any.Run", "https://any.run/"),
        ("Hybrid Analysis", "https://www.hybrid-analysis.com/"),
        ("Pulsedive", "https://pulsedive.com/"),
        ("IntelOwl", "https://github.com/intelowlproject/IntelOwl"),
    ],
    "Vulnerability Intelligence": [
        ("CVE Program", "https://www.cve.org/"),
        ("NVD (NIST)", "https://nvd.nist.gov/"),
        ("CISA Known Exploited Vulnerabilities", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"),
        ("MITRE ATT&CK", "https://attack.mitre.org/"),
        ("OWASP Top Ten", "https://owasp.org/www-project-top-ten/"),
        ("GitHub Advisory Database", "https://github.com/advisories"),
        ("OSV", "https://osv.dev/"),
        ("CVE Details", "https://www.cvedetails.com/"),
        ("Vulners", "https://vulners.com/"),
        ("Rapid7 Vuln & Exploit DB", "https://www.rapid7.com/db/"),
    ],
    "Learning & Practice": [
        ("Hack The Box", "https://www.hackthebox.com/"),
        ("HTB Academy", "https://academy.hackthebox.com/"),
        ("TryHackMe", "https://tryhackme.com/"),
        ("PortSwigger Web Security Academy", "https://portswigger.net/web-security"),
        ("PentesterLab", "https://pentesterlab.com/"),
        ("picoCTF", "https://picoctf.org/"),
        ("OverTheWire", "https://overthewire.org/wargames/"),
        ("CyberDefenders", "https://cyberdefenders.org/"),
        ("VulnHub", "https://www.vulnhub.com/"),
        ("Root-Me", "https://www.root-me.org/"),
        ("OWASP Juice Shop", "https://owasp.org/www-project-juice-shop/"),
        ("DVWA", "https://github.com/digininja/DVWA"),
        ("CTFtime", "https://ctftime.org/"),
        ("Cryptopals", "https://cryptopals.com/"),
        ("Exploit Education", "https://exploit.education/"),
        ("GOAD (Game of Active Directory)", "https://github.com/Orange-Cyberdefense/GOAD"),
    ],
    "Reference & Cheat Sheets": [
        ("OWASP", "https://owasp.org/"),
        ("OWASP Cheat Sheet Series", "https://cheatsheetseries.owasp.org/"),
        ("OWASP Web Security Testing Guide", "https://owasp.org/www-project-web-security-testing-guide/"),
        ("OWASP ASVS", "https://owasp.org/www-project-application-security-verification-standard/"),
        ("HackTricks", "https://github.com/HackTricks-wiki/hacktricks"),
        ("PayloadsAllTheThings", "https://github.com/swisskyrepo/PayloadsAllTheThings"),
        ("GTFOBins", "https://gtfobins.github.io/"),
        ("LOLBAS", "https://lolbas-project.github.io/"),
        ("LOLDrivers", "https://www.loldrivers.io/"),
        ("WADComs", "https://wadcoms.github.io/"),
        ("SecLists", "https://github.com/danielmiessler/SecLists"),
        ("Red Team Notes (ired.team)", "https://www.ired.team/"),
        ("Internal All The Things", "https://swisskyrepo.github.io/InternalAllTheThings/"),
        ("revshells.com", "https://www.revshells.com/"),
        ("filesec.io", "https://filesec.io/"),
        ("malapi.io", "https://malapi.io/"),
    ],
    "Reporting & Collaboration": [
        ("Faraday", "https://github.com/infobyte/faraday"),
        ("Dradis", "https://dradisframework.com/"),
        ("Ghostwriter", "https://github.com/GhostManager/Ghostwriter"),
        ("SysReptor", "https://github.com/Syslifters/sysreptor"),
        ("VECTR", "https://github.com/SecurityRiskAdvisors/VECTR"),
    ],
    "Distributions": [
        ("Kali Linux", "https://www.kali.org/"),
        ("Parrot Security OS", "https://www.parrotsec.org/"),
        ("BlackArch", "https://blackarch.org/"),
        ("FLARE VM", "https://github.com/mandiant/flare-vm"),
        ("Commando VM", "https://github.com/mandiant/commando-vm"),
        ("REMnux", "https://remnux.org/"),
        ("SANS SIFT Workstation", "https://www.sans.org/tools/sift-workstation/"),
        ("Tails", "https://tails.net/"),
        ("Whonix", "https://www.whonix.org/"),
    ],
    "Awesome Lists": [
        ("awesome-pentest", "https://github.com/enaqx/awesome-pentest"),
        ("Awesome Hacking", "https://github.com/Hack-with-Github/Awesome-Hacking"),
        ("awesome-osint", "https://github.com/jivoi/awesome-osint"),
        ("awesome-web-security", "https://github.com/qazbnm456/awesome-web-security"),
        ("awesome-malware-analysis", "https://github.com/rshipp/awesome-malware-analysis"),
        ("awesome-incident-response", "https://github.com/meirwah/awesome-incident-response"),
        ("awesome-threat-intelligence", "https://github.com/hslatman/awesome-threat-intelligence"),
        ("awesome-red-teaming", "https://github.com/yeyintminthuhtut/Awesome-Red-Teaming"),
        ("awesome-api-security", "https://github.com/arainho/awesome-api-security"),
    ],
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def total() -> int:
    return sum(len(v) for v in CATALOG.values())


def render_html() -> str:
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<!-- Generated by scripts/build_security.py from its CATALOG.",
        "     DO NOT EDIT manually; edit the catalog and re-run the script. -->",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
        f"    <DT><H3>{esc(WRAPPER)}</H3>",
        "    <DL><p>",
    ]
    for category, tools in CATALOG.items():
        lines.append(f"        <DT><H3>{esc(category)}</H3>")
        lines.append("        <DL><p>")
        for name, url in tools:
            lines.append(f'            <DT><A HREF="{esc(url)}">{esc(name)}</A>')
        lines.append("        </DL><p>")
    lines += ["    </DL><p>", "</DL><p>", ""]
    return "\n".join(lines)


def render_readme() -> str:
    lines = [
        "# Security & Pentesting Tools",
        "",
        f"A curated, browser-importable directory of {total()} security, "
        "penetration-testing, and defensive resources — from reconnaissance and "
        "exploitation to cloud, mobile, forensics, threat intel, and hands-on "
        "practice.",
        "",
        (f"**[🔎 Browse everything on the live, searchable site →]({SITE_URL})**"
         if SITE_URL else
         "**Prefer a searchable view?** Open [`docs/index.html`](../docs/index.html) "
         "in your browser, or import `security.html` below."),
        "",
        "Import `security.html` into your browser the same way as the "
        "[OSINT collection](../osint/README.md#method-to-import-bookmark).",
        "",
        "> For lawful, authorized security testing and education only.",
        "",
        "_This file and `security.html` are generated from the catalog in "
        "[`scripts/build_security.py`](../scripts/build_security.py) — edit there "
        "and re-run to add tools._",
        "",
        "### Table of Contents",
        "",
        "<DL><p>",
    ]
    for category, tools in CATALOG.items():
        lines.append(f"    <DT><H3>{esc(category)}</H3>")
        lines.append("    <DL><p>")
        for name, url in tools:
            lines.append(f'        <DT><A HREF="{esc(url)}">{esc(name)}</A>')
        lines.append("    </DL><p>")
    lines += ["</DL><p>", ""]
    return "\n".join(lines)


def main() -> int:
    Path("security/security.html").write_text(render_html(), encoding="utf-8")
    Path("security/README.md").write_text(render_readme(), encoding="utf-8")
    print(f"Generated security/security.html and security/README.md — "
          f"{total()} tools across {len(CATALOG)} categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
