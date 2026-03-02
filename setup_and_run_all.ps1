# ============================================================
# Setup + Run: Playwright + Pytest + HTML report + Evidencias
# ============================================================

$ErrorActionPreference = "Stop"

$projectPath = "C:\opencart-tests"
$testsPath   = Join-Path $projectPath "tests"
$resultsPath = Join-Path $projectPath "test-results"
$videosPath  = Join-Path $resultsPath "videos"

Write-Host "=== Creando entorno en $projectPath ==="
New-Item -ItemType Directory -Force -Path $projectPath | Out-Null
Set-Location $projectPath

# Evita bloqueo de Activate.ps1 en esta sesión
Set-ExecutionPolicy -Scope Process Bypass -Force

# 1) Crear venv (solo si no existe)
if (!(Test-Path "$projectPath\venv\Scripts\python.exe")) {
  Write-Host "=== Creando entorno virtual ==="
  python -m venv "$projectPath\venv"
}

# 2) Activar venv (IMPORTANTE: dot-source)
Write-Host "=== Activando entorno virtual ==="
. "$projectPath\venv\Scripts\Activate.ps1"

# 3) Instalar deps de forma consistente
Write-Host "=== Instalando dependencias ==="
python -m pip install --upgrade pip
python -m pip install pytest pytest-html playwright
python -m playwright install chromium

# 4) Crear estructura
Write-Host "=== Creando carpeta tests ==="
New-Item -ItemType Directory -Force -Path $testsPath | Out-Null

# 5) Preparar test-results (limpia y recrea + videos)
Write-Host "=== Preparando test-results ==="
if (Test-Path $resultsPath) { Remove-Item -Recurse -Force $resultsPath }
New-Item -ItemType Directory -Force -Path $resultsPath | Out-Null
New-Item -ItemType Directory -Force -Path $videosPath  | Out-Null

# 6) Generar tests (con waits + selectores estables)
Write-Host "=== Generando archivos de prueba ==="

@"
from playwright.sync_api import sync_playwright

BASE_URL = "https://demo.opencart.com"

def test_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # para diagnosticar
        context = browser.new_context(record_video_dir="test-results/videos")
        page = context.new_page()

        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="test-results/search_step1.png")

        page.wait_for_selector("input[name='search']", timeout=30000)
        page.fill("input[name='search']", "iPhone")
        page.screenshot(path="test-results/search_step2.png")

        page.click("#search button")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="test-results/search_step3.png")

        assert page.is_visible("text=iPhone")

        context.close()
        browser.close()
"@ | Out-File -Encoding utf8 (Join-Path $testsPath "test_search.py")

# (Opcional) si quieres mantener tus otros tests, te los ajusto igual.

# 7) Ejecutar pytest con reporte
Write-Host "=== Ejecutando pruebas ==="
python -m pytest tests -v --html=report.html --self-contained-html

# 8) Abrir reporte
Write-Host "=== Abriendo reporte HTML ==="
Start-Process (Join-Path $projectPath "report.html")

Write-Host "=== Finalizado ==="