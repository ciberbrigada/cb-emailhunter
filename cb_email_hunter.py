#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#   CB-EMAILHUNTER v1.0 — Ciberbrigada OSINT Suite
#   Herramienta de reconocimiento de emails en fuentes abiertas
#   Uso exclusivo para fines legales y educativos
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import time
import hashlib
import urllib.parse
import smtplib
import socket
import json
import re
import os

try:
    import requests
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install requests colorama --break-system-packages -q")
    import requests
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# ── Colores ──────────────────────────────────────────────────────────────────
C  = Fore.CYAN
Y  = Fore.YELLOW
G  = Fore.GREEN
R  = Fore.RED
W  = Fore.WHITE
D  = Fore.WHITE + Style.DIM
M  = Fore.MAGENTA
B  = Style.BRIGHT
RS = Style.RESET_ALL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html,*/*",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
}

def banner():
    os.system("cls" if os.name == "nt" else "clear")

    CYAN  = '\033[96m'
    ORAN  = '\033[38;5;208m'
    DIM   = '\033[2m\033[37m'
    BOLD  = '\033[1m'
    YEL   = '\033[33m'
    RST   = '\033[0m'

    # Logo CB — compacto, denso, elegante
    # Lado izquierdo (águila + C) = CYAN | Lado derecho (B + circuitos) = NARANJA
    logo = [
        "              ...::::...               ",
        "              ..:::+: ....             ",
        "        .:...:::::::.  ..:....... ..   ",
        "       :+  .:::::::    ::::::::::.     ",
        "      .+. .::::::::    +::::::::++::   ",
        "    . ::.:+:.          :::       ::+:  ",
        "   .: :::+.            +:+       .+++  ",
        "   .+ .+::             +:+.    .:+++.  ",
        "    +: :+.             ++++++++++++:   ",
        "     +:.:+             +++:......:+++: ",
        "   :. :++++.           +++         ++%:",
        "    ::  .::+++:::::    +++        .++%:",
        "     .:::....::++++   .+++:.....::+++: ",
        "    ... ..:+::+::+++:. ::++++++++++:.  ",
        "      :+:. :+.:+:.:++::......  ...     ",
        "        :+: :+..++...::::.......        ",
        "          .. :+:..:+:.........          ",
    ]

    # Split por mitad para colorear cyan/naranja
    print()
    for line in logo:
        mid = len(line) // 2
        print(f"       {CYAN}{BOLD}{line[:mid]}{ORAN}{line[mid:]}{RST}")

    # Crédito debajo del ASCII
    print(f"                          {DIM}by: Fgunther{RST}")
    print()
    print(f"  {CYAN}{BOLD}Ciber{ORAN}brigada{RST} {CYAN}OSINT Suite{RST}  {DIM}─────────────────────{RST}")
    print(f"  {BOLD}╔══════════════════════════════════════════╗{RST}")
    print(f"  {BOLD}║  📧  CB-EMAILHUNTER  v1.0               ║{RST}")
    print(f"  {BOLD}║  Email OSINT & Breach Intelligence      ║{RST}")
    print(f"  {BOLD}╚══════════════════════════════════════════╝{RST}")
    print(f"  {DIM}[ ciberbrigada.com ]  [ OSINT Suite ]{RST}")
    print(f"  {YEL}⚠  Solo para uso legal, ético y educativo  ⚠{RST}")
    print()

def separador(titulo=""):
    if titulo:
        pad = (58 - len(titulo)) // 2
        print(f"\n{C}{'─' * pad} {B}{titulo}{RS}{C} {'─' * pad}{RS}")
    else:
        print(f"{D}{'─' * 60}{RS}")

def ok(msg):    print(f"  {G}{B}[✓]{RS} {W}{msg}{RS}")
def info(msg):  print(f"  {C}[i]{RS} {W}{msg}{RS}")
def warn(msg):  print(f"  {Y}[!]{RS} {Y}{msg}{RS}")
def fail(msg):  print(f"  {R}[✗]{RS} {D}{msg}{RS}")
def dato(k, v): print(f"  {C}  ▸ {D}{k}:{RS} {W}{B}{v}{RS}")

def validar_email(email):
    return bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email.strip()))

def get_md5(email):
    return hashlib.md5(email.lower().strip().encode()).hexdigest()

def get_sha1(email):
    return hashlib.sha1(email.lower().strip().encode()).hexdigest()

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — SMTP VERIFY (¿Existe el email en el servidor?)
# ══════════════════════════════════════════════════════════════════════════════
def smtp_verify(email):
    separador("VERIFICACIÓN SMTP")
    domain = email.split("@")[1]
    try:
        mx_records = socket.getaddrinfo(f"mail.{domain}", 25)
        mx_ip = mx_records[0][4][0]
    except:
        mx_ip = None

    smtp_servers = {
        "gmail.com":    "aspmx.l.google.com",
        "googlemail.com": "aspmx.l.google.com",
        "yahoo.com":    "mta5.am0.yahoodns.net",
        "outlook.com":  "outlook-com.olc.protection.outlook.com",
        "hotmail.com":  "outlook-com.olc.protection.outlook.com",
        "live.com":     "outlook-com.olc.protection.outlook.com",
        "protonmail.com": "mail.protonmail.ch",
        "icloud.com":   "mx1.mail.icloud.com",
    }

    server = smtp_servers.get(domain, f"mail.{domain}")
    dato("Dominio", domain)
    dato("Servidor MX", server)

    try:
        with smtplib.SMTP(timeout=8) as s:
            s.connect(server, 25)
            s.helo("verify.osint.com")
            s.mail("osint@ciberbrigada.com")
            code, msg = s.rcpt(email)
            if code == 250:
                ok(f"Email VÁLIDO — El servidor aceptó la dirección")
            elif code == 550:
                fail(f"Email INVÁLIDO — El servidor lo rechazó (550)")
            else:
                warn(f"Respuesta ambigua del servidor: {code}")
    except smtplib.SMTPConnectError:
        warn("No se pudo conectar al servidor SMTP (firewall/timeout)")
    except Exception as e:
        warn(f"SMTP no disponible: {type(e).__name__}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — EMAILREP.IO (Reputación y score)
# ══════════════════════════════════════════════════════════════════════════════
def emailrep(email):
    separador("EMAILREP.IO — Reputación")
    try:
        r = requests.get(
            f"https://emailrep.io/{urllib.parse.quote(email)}",
            headers={
                "User-Agent": "cb-emailhunter/1.0",
                "Accept": "application/json",
            },
            timeout=10
        )
        if r.status_code == 200:
            d = r.json()
            dato("Reputación",        d.get("reputation", "—").upper())
            dato("Suspicious",        "SÍ ⚠" if d.get("suspicious") else "NO")
            dato("Referencias",       str(d.get("references", 0)))

            details = d.get("details", {})
            dato("Blacklisted",       "SÍ ⚠" if details.get("blacklisted") else "NO")
            dato("Malicious activity","SÍ ⚠" if details.get("malicious_activity") else "NO")
            dato("Credenciales exp.", "SÍ ⚠" if details.get("credentials_leaked") else "NO")
            dato("Data breach",       "SÍ ⚠" if details.get("data_breach") else "NO")
            dato("Primer visto",      details.get("first_seen", "—"))
            dato("Último visto",      details.get("last_seen", "—"))
            dato("SPF",               "SÍ" if details.get("spf_strict") else "NO")
            dato("DMARC",             "SÍ" if details.get("dmarc_enforced") else "NO")
            dato("Deliverable",       "SÍ" if details.get("deliverable") else "NO")
            dato("Free provider",     "SÍ" if details.get("free_provider") else "NO")
            dato("Disposable",        "SÍ ⚠" if details.get("disposable") else "NO")
            profiles = details.get("profiles", [])
            if profiles:
                dato("Perfiles encontrados", ", ".join(profiles))
            if details.get("data_breach"):
                ok("⚠  Email encontrado en filtraciones de datos")
        elif r.status_code == 429:
            warn("Rate limit en EmailRep.io — esperá unos minutos y reintentá")
            info("Verificación manual: https://emailrep.io/" + email)
        elif r.status_code == 400:
            warn("EmailRep no pudo procesar este email")
        else:
            warn(f"EmailRep respondió con código {r.status_code}")
    except requests.exceptions.Timeout:
        warn("EmailRep.io no respondió (timeout)")
    except Exception as e:
        fail(f"Error en EmailRep: {type(e).__name__}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — HUDSONROCK (Infostealers / Credenciales robadas)
# ══════════════════════════════════════════════════════════════════════════════
def hudsonrock(email):
    separador("HUDSONROCK — Infostealers")
    # Endpoint actualizado 2025
    endpoints = [
        f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-login?login={urllib.parse.quote(email)}",
        f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/check-email?email={urllib.parse.quote(email)}",
    ]
    success = False
    for url in endpoints:
        try:
            r = requests.get(url, headers={
                **HEADERS,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0.0.0 Safari/537.36",
            }, timeout=12)
            if r.status_code == 200:
                d = r.json()
                stealers = d.get("stealers", []) or d.get("data", [])
                if stealers:
                    ok(f"¡ALERTA! Email en {len(stealers)} registros de infostealers")
                    for i, s in enumerate(stealers[:5], 1):
                        print(f"\n  {R}{B}  [Registro #{i}]{RS}")
                        dato("  Fecha",        s.get("date_uploaded", s.get("date", "—")))
                        dato("  Stealer",      s.get("stealer_family", s.get("malware", "—")))
                        dato("  OS",           s.get("operating_system", s.get("os", "—")))
                        dato("  Contraseña",   s.get("password", "—"))
                        dato("  URL",          s.get("url", "—"))
                    if len(stealers) > 5:
                        warn(f"  ... y {len(stealers) - 5} registros más")
                else:
                    ok("No encontrado en bases de infostealers de HudsonRock")
                success = True
                break
            elif r.status_code == 429:
                warn("Rate limit en HudsonRock — intentá en unos minutos")
                success = True
                break
        except Exception:
            continue

    if not success:
        # Fallback: búsqueda manual via web
        warn("HudsonRock API no disponible — verificá manualmente:")
        url_manual = f"https://cavalier.hudsonrock.com/search?query={urllib.parse.quote(email)}"
        dato("  URL manual", url_manual)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4 — BREACH CHECK (Leaks públicos — múltiples fuentes)
# ══════════════════════════════════════════════════════════════════════════════
def breach_directory(email):
    separador("BREACH CHECK — Leaks públicos")
    domain = email.split("@")[1]
    found_any = False

    # Fuente 1: ProxyNova COMB (Collection Of Many Breaches)
    try:
        r = requests.get(
            f"https://api.proxynova.com/comb?query={urllib.parse.quote(email)}&start=0&limit=10",
            headers=HEADERS, timeout=12
        )
        if r.status_code == 200:
            d = r.json()
            lines = d.get("lines", [])
            count = d.get("count", 0)
            if lines:
                ok(f"ProxyNova COMB: {count} registros encontrados")
                for line in lines[:6]:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        passwd = ":".join(parts[1:])
                        print(f"  {Y}  ▸{RS} {W}{parts[0]}{RS}  pass: {R}{passwd[:3]}***{RS}")
                found_any = True
            else:
                ok("ProxyNova COMB: sin resultados")
        else:
            warn(f"ProxyNova respondió {r.status_code}")
    except Exception as e:
        warn(f"ProxyNova no disponible: {type(e).__name__}")

    # Fuente 2: HIBP — lista de breaches del dominio (pública, sin key)
    try:
        r = requests.get(
            "https://haveibeenpwned.com/api/v3/breaches",
            headers={**HEADERS, "User-Agent": "cb-emailhunter/1.0"},
            timeout=10
        )
        if r.status_code == 200:
            breaches = r.json()
            # Filtrar breaches que incluyen el dominio del email
            domain_breaches = [b for b in breaches if domain in b.get("Domain", "").lower()
                              or domain.split(".")[0] in b.get("Name", "").lower()]
            if domain_breaches:
                ok(f"HIBP: dominio '{domain}' aparece en {len(domain_breaches)} breach(es) conocidos")
                for b in domain_breaches[:3]:
                    dato(f"  Breach", b.get("Name", "—"))
                    dato(f"  Fecha",  b.get("BreachDate", "—"))
                    dato(f"  Cuentas comprometidas", f"{b.get('PwnCount', 0):,}")
                    tipos = ", ".join(b.get("DataClasses", [])[:4])
                    dato(f"  Datos expuestos", tipos)
            else:
                info(f"Dominio '{domain}' no aparece directamente en breaches de HIBP")
            # Siempre informar que para verificar el email específico se necesita key
            dato("  Verificar email en HIBP", f"https://haveibeenpwned.com/account/{urllib.parse.quote(email)}")
        else:
            warn(f"HIBP respondió {r.status_code}")
    except Exception as e:
        warn(f"HIBP no disponible: {type(e).__name__}")

    # Fuente 3: Link directo para verificación manual
    print()
    info("Links para verificación manual adicional:")
    dato("  HIBP",          f"https://haveibeenpwned.com/account/{urllib.parse.quote(email)}")
    dato("  LeakCheck",     f"https://leakcheck.io/?query={urllib.parse.quote(email)}")
    dato("  DeHashed",      f"https://dehashed.com/search?query={urllib.parse.quote(email)}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5 — GRAVATAR (Perfil e imagen asociada)
# ══════════════════════════════════════════════════════════════════════════════
def gravatar_check(email):
    separador("GRAVATAR — Perfil asociado")
    md5 = get_md5(email)
    try:
        r = requests.get(
            f"https://www.gravatar.com/{md5}.json",
            headers=HEADERS, timeout=8
        )
        if r.status_code == 200:
            d = r.json()
            entry = d.get("entry", [{}])[0]
            ok("Perfil Gravatar encontrado")
            dato("Display name", entry.get("displayName", "—"))
            dato("Username",     entry.get("preferredUsername", "—"))
            dato("Perfil URL",   f"https://gravatar.com/{entry.get('preferredUsername','')}")
            dato("Avatar URL",   f"https://www.gravatar.com/avatar/{md5}?s=200")

            for acc in entry.get("accounts", []):
                dato(f"  Red [{acc.get('shortname','?')}]",
                     acc.get("url", "—"))

            for url in entry.get("urls", []):
                dato(f"  URL", url.get("value", "—"))

            about = entry.get("aboutMe", "")
            if about:
                dato("Bio", about[:120])
        elif r.status_code == 404:
            warn("No hay perfil Gravatar asociado a este email")
        else:
            warn(f"Gravatar respondió con código {r.status_code}")
    except Exception as e:
        fail(f"Error en Gravatar: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 6 — GOOGLE DORKS (Búsquedas automáticas)
# ══════════════════════════════════════════════════════════════════════════════
def google_dorks(email):
    separador("GOOGLE DORKS — Links de búsqueda")
    domain = email.split("@")[1]
    user   = email.split("@")[0]
    dorks = [
        (f'"{email}"',                                    "Email exacto"),
        (f'"{email}" filetype:pdf',                       "En documentos PDF"),
        (f'"{email}" site:linkedin.com',                  "LinkedIn"),
        (f'"{email}" site:facebook.com',                  "Facebook"),
        (f'"{email}" site:instagram.com',                 "Instagram"),
        (f'"{email}" password OR leak OR breach',         "Leaks públicos"),
        (f'"{email}" CV OR curriculum OR resume',         "Curriculums"),
        (f'"{user}" site:{domain}',                       "En su propio dominio"),
        (f'intext:"{email}" site:pastebin.com',           "Pastebin"),
        (f'intext:"{email}" site:github.com',             "GitHub"),
    ]
    for dork, desc in dorks:
        encoded = urllib.parse.quote(dork)
        url = f"https://www.google.com/search?q={encoded}"
        print(f"  {C}▸ {W}{desc:<28}{RS} {D}{url[:72]}{RS}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 7 — DOMINIO (Info del dominio del email)
# ══════════════════════════════════════════════════════════════════════════════
def domain_info(email):
    separador("DOMINIO — Info del proveedor")
    domain = email.split("@")[1]
    dato("Dominio", domain)

    # DNS lookup básico
    try:
        ip = socket.gethostbyname(domain)
        dato("IP del servidor", ip)
    except:
        warn("No se pudo resolver el dominio")

    # Clasificación del proveedor
    free_providers = {
        "gmail.com": "Google Gmail",
        "googlemail.com": "Google Gmail",
        "yahoo.com": "Yahoo Mail",
        "yahoo.com.ar": "Yahoo Mail AR",
        "outlook.com": "Microsoft Outlook",
        "hotmail.com": "Microsoft Hotmail",
        "live.com": "Microsoft Live",
        "protonmail.com": "ProtonMail (cifrado)",
        "proton.me": "ProtonMail (cifrado)",
        "tutanota.com": "Tutanota (cifrado)",
        "icloud.com": "Apple iCloud",
        "me.com": "Apple Me",
        "aol.com": "AOL Mail",
        "yandex.com": "Yandex Mail (Rusia)",
        "yandex.ru": "Yandex Mail (Rusia)",
        "mail.ru": "Mail.ru (Rusia)",
        "gmx.com": "GMX Mail",
        "zoho.com": "Zoho Mail",
        "temp-mail.org": "⚠ TEMPORAL/DESECHABLE",
        "guerrillamail.com": "⚠ TEMPORAL/DESECHABLE",
        "mailinator.com": "⚠ TEMPORAL/DESECHABLE",
        "10minutemail.com": "⚠ TEMPORAL/DESECHABLE",
        "sharklasers.com": "⚠ TEMPORAL/DESECHABLE",
    }

    if domain in free_providers:
        dato("Proveedor", free_providers[domain])
        if domain in ["protonmail.com", "proton.me", "tutanota.com"]:
            warn("Email cifrado — difícil de rastrear")
        elif "TEMPORAL" in free_providers.get(domain, ""):
            warn("Email desechable — probablemente no real")
        else:
            ok("Proveedor gratuito reconocido")
    else:
        ok(f"Dominio corporativo/privado: {domain}")
        # Intentar WHOIS básico
        try:
            r = requests.get(
                f"https://api.whois.vu/?q={domain}",
                headers=HEADERS, timeout=8
            )
            if r.status_code == 200:
                d = r.json()
                dato("Registrador", d.get("registrar", "—"))
                dato("Creación",    d.get("creation_date", "—"))
                dato("Expiración",  d.get("expiration_date", "—"))
                dato("País",        d.get("country", "—"))
        except:
            pass

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 8 — RESUMEN FINAL
# ══════════════════════════════════════════════════════════════════════════════
def resumen(email, resultados):
    separador("RESUMEN DE INTELIGENCIA")
    print(f"\n  {C}{B}Target:{RS} {W}{B}{email}{RS}\n")
    for item in resultados:
        estado = item.get("estado", "—")
        modulo = item.get("modulo", "—")
        halgo  = item.get("hallazgo", "")
        if estado == "ok":
            print(f"  {G}[✓]{RS} {W}{modulo:<30}{RS} {G}{halgo}{RS}")
        elif estado == "warn":
            print(f"  {Y}[!]{RS} {W}{modulo:<30}{RS} {Y}{halgo}{RS}")
        elif estado == "fail":
            print(f"  {R}[✗]{RS} {W}{modulo:<30}{RS} {D}{halgo}{RS}")
    print(f"\n  {D}Análisis completado — Ciberbrigada OSINT Suite v1.0{RS}\n")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    banner()

    print(f"  {W}Ingresá el email a analizar (o 'salir' para terminar):{RS}\n")

    while True:
        try:
            email = input(f"  {C}▸ Email:{RS} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {Y}Saliendo... Hasta pronto.{RS}\n")
            sys.exit(0)

        if email in ("salir", "exit", "quit", "q"):
            print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n")
            sys.exit(0)

        if not validar_email(email):
            warn("Email inválido. Ingresá uno con formato correcto (ej: user@domain.com)")
            continue

        print(f"\n  {C}Iniciando análisis de:{RS} {W}{B}{email}{RS}")
        print(f"  {D}{'─' * 50}{RS}\n")
        time.sleep(0.3)

        # Menú de módulos
        separador("SELECCIONÁ LOS MÓDULOS")
        modulos = [
            ("1", "SMTP Verify        — ¿Existe el email?"),
            ("2", "EmailRep.io        — Reputación y score"),
            ("3", "HudsonRock         — Infostealers"),
            ("4", "BreachDirectory    — Leaks públicos"),
            ("5", "Gravatar           — Perfil asociado"),
            ("6", "Google Dorks       — Links de búsqueda"),
            ("7", "Domain Info        — Info del dominio"),
            ("0", "TODOS LOS MÓDULOS"),
        ]
        for num, desc in modulos:
            color = C if num != "0" else Y
            print(f"  {color}[{num}]{RS} {W}{desc}{RS}")

        print()
        try:
            sel = input(f"  {C}▸ Opción (ej: 0 o 1,3,5):{RS} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {Y}Saliendo...{RS}\n")
            sys.exit(0)

        if sel == "0":
            selected = ["1","2","3","4","5","6","7"]
        else:
            selected = [s.strip() for s in sel.split(",")]

        print()

        if "1" in selected: smtp_verify(email)
        if "2" in selected: emailrep(email)
        if "3" in selected: hudsonrock(email)
        if "4" in selected: breach_directory(email)
        if "5" in selected: gravatar_check(email)
        if "6" in selected: google_dorks(email)
        if "7" in selected: domain_info(email)

        separador()
        print(f"\n  {D}¿Analizar otro email? (Enter para continuar / 'salir' para terminar){RS}")
        try:
            again = input(f"  {C}▸{RS} ").strip().lower()
            if again in ("salir", "exit", "quit", "q"):
                print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {Y}Saliendo...{RS}\n")
            sys.exit(0)

        banner()

if __name__ == "__main__":
    main()
