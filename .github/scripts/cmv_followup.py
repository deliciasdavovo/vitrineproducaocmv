from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_name = '<input class="sheet-input" id="quick-insumo-nome" autocomplete="off" placeholder="Insumo existente ou novo" onkeydown="handleQuickInsumoKey(event)" style="min-width:130px;">'
new_name = '<input class="sheet-input" id="quick-insumo-nome" list="quick-insumo-list" autocomplete="off" placeholder="Insumo existente ou novo" oninput="applyQuickInsumoExistingMeta(this.value)" onkeydown="handleQuickInsumoKey(event)" style="min-width:130px;">'
if old_name not in s:
    raise SystemExit('Campo quick-insumo-nome nao encontrado no formato esperado')
s = s.replace(old_name, new_name, 1)

old_fornecedor = '<input class="sheet-input" id="quick-insumo-fornecedor" autocomplete="off" placeholder="Fornecedor" onkeydown="handleQuickInsumoKey(event)" style="min-width:110px;">'
new_fornecedor = '<input class="sheet-input" id="quick-insumo-fornecedor" list="fornecedores-list" autocomplete="off" placeholder="Fornecedor" onkeydown="handleQuickInsumoKey(event)" style="min-width:110px;">'
if old_fornecedor in s:
    s = s.replace(old_fornecedor, new_fornecedor, 1)

p.write_text(s, encoding='utf-8')

scripts = [x for x in re.findall(r'<script(?:[^>]*)>(.*?)</script>', s, re.S) if x.strip()]
if not scripts:
    raise SystemExit('Nenhum script inline encontrado')
js = Path('/tmp/ddv-app.js')
js.write_text(max(scripts, key=len), encoding='utf-8')
subprocess.run(['node', '--check', str(js)], check=True)
print('Autocomplete dos insumos e fornecedores conectado e JS validado.')
