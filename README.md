# 📧 CB-EmailHunter

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-cyan?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OSINT-Email-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/free-sin%20API%20key-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <b>Herramienta de reconocimiento OSINT para análisis de emails en fuentes abiertas</b><br/>
  Parte de la <a href="https://ciberbrigada.com">Ciberbrigada OSINT Suite</a>
</p>

---

## ¿Qué hace?

CB-EmailHunter analiza un email en múltiples fuentes abiertas y gratuitas para obtener inteligencia sobre:

- ✅ Si el email existe realmente (verificación SMTP)
- ✅ Reputación y score del email
- ✅ Si aparece en bases de infostealers (credenciales robadas)
- ✅ Si fue comprometido en filtraciones públicas
- ✅ Perfil e identidad asociada (Gravatar)
- ✅ Google Dorks automáticos
- ✅ Información del dominio del proveedor

**100% gratuito · Sin API keys · Sin registro · Sin login**

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ciberbrigada/cb-emailhunter
cd cb-emailhunter

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python3 cb_email_hunter.py
```

### Kali Linux / Parrot OS / Ubuntu

```bash
git clone https://github.com/ciberbrigada/cb-emailhunter
cd cb-emailhunter
pip install -r requirements.txt
python3 cb_email_hunter.py
```

### Windows

```cmd
git clone https://github.com/ciberbrigada/cb-emailhunter
cd cb-emailhunter
pip install -r requirements.txt
python cb_email_hunter.py
```

---

## 🔄 Mantener actualizado

Para tener siempre la última versión con las mejoras y correcciones:

```bash
cd cb-emailhunter
git pull
```

Ejecutá `git pull` cada vez que quieras actualizar. Siempre vas a tener la versión más reciente del repositorio.

---

## Uso

```bash
python3 cb_email_hunter.py
```

1. Ingresás el email a analizar
2. Seleccionás los módulos (0 = todos)
3. Analizás los resultados

```
▸ Email: ejemplo@gmail.com

[0] TODOS LOS MÓDULOS
[1] SMTP Verify        — ¿Existe el email?
[2] EmailRep.io        — Reputación y score
[3] HudsonRock         — Infostealers
[4] Breach Check       — Leaks públicos
[5] Gravatar           — Perfil asociado
[6] Google Dorks       — Links de búsqueda
[7] Domain Info        — Info del dominio

▸ Opción: 0
```

---

## Módulos

| # | Módulo | Fuente | Descripción |
|---|--------|--------|-------------|
| 1 | SMTP Verify | Directo al servidor | Verifica si el email existe en el servidor de correo |
| 2 | EmailRep.io | emailrep.io | Reputación, blacklists, historial de actividad |
| 3 | HudsonRock | cavalier.hudsonrock.com | Credenciales robadas por infostealers |
| 4 | Breach Check | ProxyNova + HIBP | Filtraciones y leaks públicos |
| 5 | Gravatar | gravatar.com | Foto de perfil, nombre, redes sociales asociadas |
| 6 | Google Dorks | Google | Links de búsqueda automáticos para OSINT manual |
| 7 | Domain Info | DNS + WHOIS | Información del dominio del proveedor de email |

---

## Requisitos

- Python 3.8+
- requests
- colorama
- Conexión a internet

---

## ⚠️ Aviso Legal

Esta herramienta es para uso **exclusivamente legal, ético y educativo**.  
El uso de esta herramienta para actividades ilegales queda bajo la responsabilidad del usuario.  
Ciberbrigada no se hace responsable del mal uso de esta herramienta.

---

## 🛡️ Ciberbrigada OSINT Suite

Esta herramienta forma parte de la suite OSINT de Ciberbrigada.  
Más herramientas en desarrollo:

- 📧 **CB-EmailHunter** — Email OSINT *(este repositorio)*
- 👤 **CB-UserHunter** — Username en todas las redes *(próximamente)*
- 📱 **CB-PhoneHunter** — OSINT de números telefónicos *(próximamente)*
- 🌐 **CB-DomainHunter** — OSINT de dominios e IPs *(próximamente)*
- 📸 **CB-InstaHunter** — Instagram OSINT *(próximamente)*

---

<p align="center">
  <a href="https://ciberbrigada.com">ciberbrigada.com</a> ·
  <a href="https://github.com/ciberbrigada">GitHub</a> ·
  <a href="https://www.linkedin.com/company/ciberbrigada/">LinkedIn</a>
  <br/><br/>
  <sub>by: Fgunther</sub>
</p>
