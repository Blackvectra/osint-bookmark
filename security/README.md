# Security & Pentesting Tools

A curated, browser-importable directory of 237 security, penetration-testing, and defensive resources — from reconnaissance and exploitation to cloud, mobile, forensics, threat intel, and hands-on practice.

**Prefer a searchable view?** Open [`docs/index.html`](../docs/index.html) in your browser, or import `security.html` below.

Import `security.html` into your browser the same way as the [OSINT collection](../osint/README.md#method-to-import-bookmark).

> For lawful, authorized security testing and education only.

_This file and `security.html` are generated from the catalog in [`scripts/build_security.py`](../scripts/build_security.py) — edit there and re-run to add tools._

### Table of Contents

<DL><p>
    <DT><H3>Reconnaissance &amp; OSINT</H3>
    <DL><p>
        <DT><A HREF="https://nmap.org/">Nmap</A>
        <DT><A HREF="https://github.com/robertdavidgraham/masscan">Masscan</A>
        <DT><A HREF="https://github.com/projectdiscovery/naabu">Naabu</A>
        <DT><A HREF="https://www.shodan.io/">Shodan</A>
        <DT><A HREF="https://search.censys.io/">Censys Search</A>
        <DT><A HREF="https://github.com/owasp-amass/amass">OWASP Amass</A>
        <DT><A HREF="https://github.com/projectdiscovery/subfinder">Subfinder</A>
        <DT><A HREF="https://github.com/aboul3la/Sublist3r">Sublist3r</A>
        <DT><A HREF="https://github.com/tomnomnom/assetfinder">assetfinder</A>
        <DT><A HREF="https://github.com/projectdiscovery/httpx">httpx</A>
        <DT><A HREF="https://github.com/projectdiscovery/dnsx">dnsx</A>
        <DT><A HREF="https://github.com/projectdiscovery/katana">Katana</A>
        <DT><A HREF="https://github.com/lc/gau">gau</A>
        <DT><A HREF="https://github.com/tomnomnom/waybackurls">waybackurls</A>
        <DT><A HREF="https://github.com/laramies/theHarvester">theHarvester</A>
        <DT><A HREF="https://github.com/lanmaster53/recon-ng">Recon-ng</A>
        <DT><A HREF="https://www.spiderfoot.net/">SpiderFoot</A>
        <DT><A HREF="https://www.maltego.com/">Maltego</A>
        <DT><A HREF="https://osintframework.com/">OSINT Framework</A>
        <DT><A HREF="https://github.com/sensepost/gowitness">gowitness</A>
        <DT><A HREF="https://github.com/michenriksen/aquatone">Aquatone</A>
    </DL><p>
    <DT><H3>Web Application Testing</H3>
    <DL><p>
        <DT><A HREF="https://portswigger.net/burp">Burp Suite (PortSwigger)</A>
        <DT><A HREF="https://caido.io/">Caido</A>
        <DT><A HREF="https://www.zaproxy.org/">OWASP ZAP</A>
        <DT><A HREF="https://sqlmap.org/">sqlmap</A>
        <DT><A HREF="https://github.com/sullo/nikto">Nikto</A>
        <DT><A HREF="https://github.com/ffuf/ffuf">ffuf</A>
        <DT><A HREF="https://github.com/epi052/feroxbuster">feroxbuster</A>
        <DT><A HREF="https://github.com/OJ/gobuster">Gobuster</A>
        <DT><A HREF="https://github.com/maurosoria/dirsearch">dirsearch</A>
        <DT><A HREF="https://github.com/projectdiscovery/nuclei">Nuclei</A>
        <DT><A HREF="https://wpscan.com/">WPScan</A>
        <DT><A HREF="https://github.com/hahwul/dalfox">Dalfox</A>
        <DT><A HREF="https://github.com/s0md3v/XSStrike">XSStrike</A>
        <DT><A HREF="https://github.com/commixproject/commix">Commix</A>
        <DT><A HREF="https://github.com/xmendez/wfuzz">Wfuzz</A>
        <DT><A HREF="https://github.com/s0md3v/Arjun">Arjun</A>
        <DT><A HREF="https://github.com/devanshbatham/ParamSpider">ParamSpider</A>
        <DT><A HREF="https://github.com/ticarpi/jwt_tool">jwt_tool</A>
        <DT><A HREF="https://github.com/drwetter/testssl.sh">testssl.sh</A>
    </DL><p>
    <DT><H3>API Security</H3>
    <DL><p>
        <DT><A HREF="https://owasp.org/www-project-api-security/">OWASP API Security Top 10</A>
        <DT><A HREF="https://github.com/assetnote/kiterunner">Kiterunner</A>
        <DT><A HREF="https://github.com/akto-api-security/akto">Akto</A>
        <DT><A HREF="https://mitmproxy.org/">mitmproxy</A>
    </DL><p>
    <DT><H3>Cloud Security</H3>
    <DL><p>
        <DT><A HREF="https://github.com/prowler-cloud/prowler">Prowler</A>
        <DT><A HREF="https://github.com/nccgroup/ScoutSuite">ScoutSuite</A>
        <DT><A HREF="https://github.com/RhinoSecurityLabs/pacu">Pacu</A>
        <DT><A HREF="https://github.com/BishopFox/cloudfox">CloudFox</A>
        <DT><A HREF="https://github.com/lyft/cartography">Cartography</A>
        <DT><A HREF="https://github.com/dirkjanm/ROADtools">ROADtools</A>
        <DT><A HREF="https://github.com/NetSPI/MicroBurst">MicroBurst</A>
        <DT><A HREF="https://github.com/DataDog/stratus-red-team">stratus-red-team</A>
        <DT><A HREF="https://github.com/turbot/steampipe">Steampipe</A>
        <DT><A HREF="https://github.com/nccgroup/PMapper">PMapper</A>
    </DL><p>
    <DT><H3>Container &amp; Kubernetes</H3>
    <DL><p>
        <DT><A HREF="https://github.com/aquasecurity/trivy">Trivy</A>
        <DT><A HREF="https://github.com/anchore/grype">Grype</A>
        <DT><A HREF="https://github.com/anchore/syft">Syft</A>
        <DT><A HREF="https://github.com/aquasecurity/kube-hunter">kube-hunter</A>
        <DT><A HREF="https://github.com/aquasecurity/kube-bench">kube-bench</A>
        <DT><A HREF="https://github.com/kubescape/kubescape">Kubescape</A>
        <DT><A HREF="https://github.com/Shopify/kubeaudit">kubeaudit</A>
        <DT><A HREF="https://github.com/falcosecurity/falco">Falco</A>
        <DT><A HREF="https://github.com/inguardians/peirates">Peirates</A>
        <DT><A HREF="https://github.com/docker/docker-bench-security">Docker Bench Security</A>
    </DL><p>
    <DT><H3>Mobile Security</H3>
    <DL><p>
        <DT><A HREF="https://github.com/MobSF/Mobile-Security-Framework-MobSF">MobSF</A>
        <DT><A HREF="https://frida.re/">Frida</A>
        <DT><A HREF="https://github.com/sensepost/objection">Objection</A>
        <DT><A HREF="https://apktool.org/">Apktool</A>
        <DT><A HREF="https://github.com/skylot/jadx">jadx</A>
        <DT><A HREF="https://github.com/androguard/androguard">Androguard</A>
        <DT><A HREF="https://github.com/WithSecureLabs/drozer">Drozer</A>
        <DT><A HREF="https://mas.owasp.org/">OWASP MASTG</A>
    </DL><p>
    <DT><H3>Exploitation &amp; C2</H3>
    <DL><p>
        <DT><A HREF="https://www.metasploit.com/">Metasploit</A>
        <DT><A HREF="https://www.exploit-db.com/">Exploit Database</A>
        <DT><A HREF="https://packetstormsecurity.com/">Packet Storm</A>
        <DT><A HREF="https://github.com/fortra/impacket">Impacket</A>
        <DT><A HREF="https://github.com/BishopFox/sliver">Sliver C2</A>
        <DT><A HREF="https://github.com/HavocFramework/Havoc">Havoc</A>
        <DT><A HREF="https://github.com/its-a-feature/Mythic">Mythic</A>
        <DT><A HREF="https://github.com/nettitude/PoshC2">PoshC2</A>
        <DT><A HREF="https://github.com/BC-SECURITY/Empire">Empire</A>
        <DT><A HREF="https://github.com/t3l3machus/Villain">Villain</A>
    </DL><p>
    <DT><H3>Privilege Escalation</H3>
    <DL><p>
        <DT><A HREF="https://github.com/peass-ng/PEASS-ng">PEASS-ng (winPEAS/linPEAS)</A>
        <DT><A HREF="https://github.com/rebootuser/LinEnum">LinEnum</A>
        <DT><A HREF="https://github.com/diego-treitos/linux-smart-enumeration">linux-smart-enumeration</A>
        <DT><A HREF="https://github.com/DominicBreuker/pspy">pspy</A>
        <DT><A HREF="https://github.com/GhostPack/Seatbelt">Seatbelt</A>
        <DT><A HREF="https://github.com/itm4n/PrivescCheck">PrivescCheck</A>
        <DT><A HREF="https://github.com/AlessandroZ/BeRoot">BeRoot</A>
    </DL><p>
    <DT><H3>Passwords &amp; Credentials</H3>
    <DL><p>
        <DT><A HREF="https://hashcat.net/hashcat/">Hashcat</A>
        <DT><A HREF="https://www.openwall.com/john/">John the Ripper</A>
        <DT><A HREF="https://github.com/vanhauser-thc/thc-hydra">THC Hydra</A>
        <DT><A HREF="https://github.com/jmk-foofus/medusa">Medusa</A>
        <DT><A HREF="https://haveibeenpwned.com/">Have I Been Pwned</A>
        <DT><A HREF="https://crackstation.net/">CrackStation</A>
        <DT><A HREF="https://github.com/HashPals/Name-That-Hash">Name-That-Hash</A>
        <DT><A HREF="https://github.com/psypanda/hashID">hashID</A>
        <DT><A HREF="https://github.com/digininja/CeWL">CeWL</A>
        <DT><A HREF="https://github.com/sc0tfree/mentalist">Mentalist</A>
    </DL><p>
    <DT><H3>Active Directory &amp; Post-Exploitation</H3>
    <DL><p>
        <DT><A HREF="https://github.com/SpecterOps/BloodHound">BloodHound</A>
        <DT><A HREF="https://github.com/Pennyw0rth/NetExec">NetExec</A>
        <DT><A HREF="https://github.com/gentilkiwi/mimikatz">Mimikatz</A>
        <DT><A HREF="https://github.com/GhostPack/Rubeus">Rubeus</A>
        <DT><A HREF="https://github.com/ly4k/Certipy">Certipy</A>
        <DT><A HREF="https://github.com/lgandx/Responder">Responder</A>
        <DT><A HREF="https://github.com/ropnop/kerbrute">Kerbrute</A>
        <DT><A HREF="https://github.com/PowerShellMafia/PowerSploit">PowerSploit</A>
        <DT><A HREF="https://github.com/adrecon/ADRecon">ADRecon</A>
        <DT><A HREF="https://www.pingcastle.com/">PingCastle</A>
        <DT><A HREF="https://github.com/p0dalirius/Coercer">Coercer</A>
        <DT><A HREF="https://github.com/dirkjanm/ldapdomaindump">ldapdomaindump</A>
        <DT><A HREF="https://github.com/SnaffCon/Snaffler">Snaffler</A>
        <DT><A HREF="https://github.com/dirkjanm/BloodHound.py">BloodHound.py</A>
    </DL><p>
    <DT><H3>Network &amp; Wireless</H3>
    <DL><p>
        <DT><A HREF="https://www.wireshark.org/">Wireshark</A>
        <DT><A HREF="https://www.tcpdump.org/">tcpdump</A>
        <DT><A HREF="https://www.bettercap.org/">Bettercap</A>
        <DT><A HREF="https://www.aircrack-ng.org/">Aircrack-ng</A>
        <DT><A HREF="https://www.kismetwireless.net/">Kismet</A>
        <DT><A HREF="https://github.com/derv82/wifite2">Wifite2</A>
        <DT><A HREF="https://github.com/t6x/reaver-wps-fork-t6x">Reaver</A>
        <DT><A HREF="https://github.com/s0lst1c3/eaphammer">EAPHammer</A>
    </DL><p>
    <DT><H3>Code, Secrets &amp; Supply Chain</H3>
    <DL><p>
        <DT><A HREF="https://github.com/semgrep/semgrep">Semgrep</A>
        <DT><A HREF="https://codeql.github.com/">CodeQL</A>
        <DT><A HREF="https://github.com/PyCQA/bandit">Bandit</A>
        <DT><A HREF="https://github.com/gitleaks/gitleaks">Gitleaks</A>
        <DT><A HREF="https://github.com/trufflesecurity/trufflehog">TruffleHog</A>
        <DT><A HREF="https://github.com/Yelp/detect-secrets">detect-secrets</A>
        <DT><A HREF="https://github.com/awslabs/git-secrets">git-secrets</A>
        <DT><A HREF="https://github.com/google/osv-scanner">OSV-Scanner</A>
        <DT><A HREF="https://github.com/jeremylong/DependencyCheck">OWASP Dependency-Check</A>
        <DT><A HREF="https://github.com/bridgecrewio/checkov">Checkov</A>
        <DT><A HREF="https://github.com/aquasecurity/tfsec">tfsec</A>
        <DT><A HREF="https://github.com/DependencyTrack/dependency-track">Dependency-Track</A>
    </DL><p>
    <DT><H3>Fuzzing</H3>
    <DL><p>
        <DT><A HREF="https://github.com/AFLplusplus/AFLplusplus">AFL++</A>
        <DT><A HREF="https://llvm.org/docs/LibFuzzer.html">libFuzzer</A>
        <DT><A HREF="https://github.com/google/honggfuzz">honggfuzz</A>
        <DT><A HREF="https://github.com/jtpereyda/boofuzz">boofuzz</A>
        <DT><A HREF="https://gitlab.com/akihe/radamsa">radamsa</A>
        <DT><A HREF="https://github.com/google/atheris">Atheris</A>
        <DT><A HREF="https://github.com/microsoft/restler-fuzzer">RESTler</A>
    </DL><p>
    <DT><H3>Forensics &amp; Reverse Engineering</H3>
    <DL><p>
        <DT><A HREF="https://ghidra-sre.org/">Ghidra</A>
        <DT><A HREF="https://hex-rays.com/ida-free/">IDA Free</A>
        <DT><A HREF="https://cutter.re/">Cutter</A>
        <DT><A HREF="https://rada.re/n/">radare2</A>
        <DT><A HREF="https://x64dbg.com/">x64dbg</A>
        <DT><A HREF="https://github.com/pwndbg/pwndbg">pwndbg</A>
        <DT><A HREF="https://github.com/hugsy/gef">GEF</A>
        <DT><A HREF="https://angr.io/">angr</A>
        <DT><A HREF="https://github.com/dnSpy/dnSpy">dnSpy</A>
        <DT><A HREF="https://github.com/mandiant/capa">capa</A>
        <DT><A HREF="https://github.com/VirusTotal/yara">YARA</A>
        <DT><A HREF="https://github.com/mandiant/flare-floss">FLARE FLOSS</A>
        <DT><A HREF="https://github.com/horsicq/Detect-It-Easy">Detect It Easy</A>
        <DT><A HREF="https://github.com/volatilityfoundation/volatility3">Volatility 3</A>
        <DT><A HREF="https://www.autopsy.com/">Autopsy</A>
        <DT><A HREF="https://github.com/Velocidex/velociraptor">Velociraptor</A>
        <DT><A HREF="https://gchq.github.io/CyberChef/">CyberChef</A>
    </DL><p>
    <DT><H3>Threat Intelligence</H3>
    <DL><p>
        <DT><A HREF="https://www.virustotal.com/">VirusTotal</A>
        <DT><A HREF="https://urlscan.io/">urlscan.io</A>
        <DT><A HREF="https://www.abuseipdb.com/">AbuseIPDB</A>
        <DT><A HREF="https://otx.alienvault.com/">AlienVault OTX</A>
        <DT><A HREF="https://www.greynoise.io/">GreyNoise</A>
        <DT><A HREF="https://www.misp-project.org/">MISP</A>
        <DT><A HREF="https://www.opencti.io/">OpenCTI</A>
        <DT><A HREF="https://github.com/TheHive-Project/TheHive">TheHive</A>
        <DT><A HREF="https://bazaar.abuse.ch/">MalwareBazaar</A>
        <DT><A HREF="https://urlhaus.abuse.ch/">URLhaus</A>
        <DT><A HREF="https://threatfox.abuse.ch/">ThreatFox</A>
        <DT><A HREF="https://any.run/">Any.Run</A>
        <DT><A HREF="https://www.hybrid-analysis.com/">Hybrid Analysis</A>
        <DT><A HREF="https://pulsedive.com/">Pulsedive</A>
        <DT><A HREF="https://github.com/intelowlproject/IntelOwl">IntelOwl</A>
    </DL><p>
    <DT><H3>Vulnerability Intelligence</H3>
    <DL><p>
        <DT><A HREF="https://www.cve.org/">CVE Program</A>
        <DT><A HREF="https://nvd.nist.gov/">NVD (NIST)</A>
        <DT><A HREF="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA Known Exploited Vulnerabilities</A>
        <DT><A HREF="https://attack.mitre.org/">MITRE ATT&amp;CK</A>
        <DT><A HREF="https://owasp.org/www-project-top-ten/">OWASP Top Ten</A>
        <DT><A HREF="https://github.com/advisories">GitHub Advisory Database</A>
        <DT><A HREF="https://osv.dev/">OSV</A>
        <DT><A HREF="https://www.cvedetails.com/">CVE Details</A>
        <DT><A HREF="https://vulners.com/">Vulners</A>
        <DT><A HREF="https://www.rapid7.com/db/">Rapid7 Vuln &amp; Exploit DB</A>
    </DL><p>
    <DT><H3>Learning &amp; Practice</H3>
    <DL><p>
        <DT><A HREF="https://www.hackthebox.com/">Hack The Box</A>
        <DT><A HREF="https://academy.hackthebox.com/">HTB Academy</A>
        <DT><A HREF="https://tryhackme.com/">TryHackMe</A>
        <DT><A HREF="https://portswigger.net/web-security">PortSwigger Web Security Academy</A>
        <DT><A HREF="https://pentesterlab.com/">PentesterLab</A>
        <DT><A HREF="https://picoctf.org/">picoCTF</A>
        <DT><A HREF="https://overthewire.org/wargames/">OverTheWire</A>
        <DT><A HREF="https://cyberdefenders.org/">CyberDefenders</A>
        <DT><A HREF="https://www.vulnhub.com/">VulnHub</A>
        <DT><A HREF="https://www.root-me.org/">Root-Me</A>
        <DT><A HREF="https://owasp.org/www-project-juice-shop/">OWASP Juice Shop</A>
        <DT><A HREF="https://github.com/digininja/DVWA">DVWA</A>
        <DT><A HREF="https://ctftime.org/">CTFtime</A>
        <DT><A HREF="https://cryptopals.com/">Cryptopals</A>
        <DT><A HREF="https://exploit.education/">Exploit Education</A>
        <DT><A HREF="https://github.com/Orange-Cyberdefense/GOAD">GOAD (Game of Active Directory)</A>
    </DL><p>
    <DT><H3>Reference &amp; Cheat Sheets</H3>
    <DL><p>
        <DT><A HREF="https://owasp.org/">OWASP</A>
        <DT><A HREF="https://cheatsheetseries.owasp.org/">OWASP Cheat Sheet Series</A>
        <DT><A HREF="https://owasp.org/www-project-web-security-testing-guide/">OWASP Web Security Testing Guide</A>
        <DT><A HREF="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</A>
        <DT><A HREF="https://github.com/HackTricks-wiki/hacktricks">HackTricks</A>
        <DT><A HREF="https://github.com/swisskyrepo/PayloadsAllTheThings">PayloadsAllTheThings</A>
        <DT><A HREF="https://gtfobins.github.io/">GTFOBins</A>
        <DT><A HREF="https://lolbas-project.github.io/">LOLBAS</A>
        <DT><A HREF="https://www.loldrivers.io/">LOLDrivers</A>
        <DT><A HREF="https://wadcoms.github.io/">WADComs</A>
        <DT><A HREF="https://github.com/danielmiessler/SecLists">SecLists</A>
        <DT><A HREF="https://www.ired.team/">Red Team Notes (ired.team)</A>
        <DT><A HREF="https://swisskyrepo.github.io/InternalAllTheThings/">Internal All The Things</A>
        <DT><A HREF="https://www.revshells.com/">revshells.com</A>
        <DT><A HREF="https://filesec.io/">filesec.io</A>
        <DT><A HREF="https://malapi.io/">malapi.io</A>
    </DL><p>
    <DT><H3>Reporting &amp; Collaboration</H3>
    <DL><p>
        <DT><A HREF="https://github.com/infobyte/faraday">Faraday</A>
        <DT><A HREF="https://dradisframework.com/">Dradis</A>
        <DT><A HREF="https://github.com/GhostManager/Ghostwriter">Ghostwriter</A>
        <DT><A HREF="https://github.com/Syslifters/sysreptor">SysReptor</A>
        <DT><A HREF="https://github.com/SecurityRiskAdvisors/VECTR">VECTR</A>
    </DL><p>
    <DT><H3>Distributions</H3>
    <DL><p>
        <DT><A HREF="https://www.kali.org/">Kali Linux</A>
        <DT><A HREF="https://www.parrotsec.org/">Parrot Security OS</A>
        <DT><A HREF="https://blackarch.org/">BlackArch</A>
        <DT><A HREF="https://github.com/mandiant/flare-vm">FLARE VM</A>
        <DT><A HREF="https://github.com/mandiant/commando-vm">Commando VM</A>
        <DT><A HREF="https://remnux.org/">REMnux</A>
        <DT><A HREF="https://www.sans.org/tools/sift-workstation/">SANS SIFT Workstation</A>
        <DT><A HREF="https://tails.net/">Tails</A>
        <DT><A HREF="https://www.whonix.org/">Whonix</A>
    </DL><p>
    <DT><H3>Awesome Lists</H3>
    <DL><p>
        <DT><A HREF="https://github.com/enaqx/awesome-pentest">awesome-pentest</A>
        <DT><A HREF="https://github.com/Hack-with-Github/Awesome-Hacking">Awesome Hacking</A>
        <DT><A HREF="https://github.com/jivoi/awesome-osint">awesome-osint</A>
        <DT><A HREF="https://github.com/qazbnm456/awesome-web-security">awesome-web-security</A>
        <DT><A HREF="https://github.com/rshipp/awesome-malware-analysis">awesome-malware-analysis</A>
        <DT><A HREF="https://github.com/meirwah/awesome-incident-response">awesome-incident-response</A>
        <DT><A HREF="https://github.com/hslatman/awesome-threat-intelligence">awesome-threat-intelligence</A>
        <DT><A HREF="https://github.com/yeyintminthuhtut/Awesome-Red-Teaming">awesome-red-teaming</A>
        <DT><A HREF="https://github.com/arainho/awesome-api-security">awesome-api-security</A>
    </DL><p>
</DL><p>
