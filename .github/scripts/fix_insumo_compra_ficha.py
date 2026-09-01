from pathlib import Path
import re
import subprocess

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_toolbar = '''    <datalist id="quick-insumo-list"></datalist>
    <div style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap; align-items:center;">
      <button class="btn btn-ghost btn-sm" onclick="addIngredienteRow()">+ Criar linha vazia</button>
    </div>'''

new_toolbar = '''    <datalist id="quick-insumo-list"></datalist>

    <div class="card" style="margin-bottom:12px;padding:14px 16px;">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px;flex-wrap:wrap;">
        <div>
          <div style="font-size:13px;font-weight:800;color:var(--text);">1. Cadastrar insumo</div>
          <div style="font-size:11px;color:var(--text-light);margin-top:2px;">Aqui você cadastra o item. A compra é registrada separadamente logo abaixo.</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:minmax(190px,2fr) 110px minmax(140px,1fr) auto;gap:8px;align-items:end;">
        <div class="form-group"><label>Nome do insumo</label><input class="sheet-input" id="novo-insumo-nome" autocomplete="off" placeholder="ex: Farinha de trigo"></div>
        <div class="form-group"><label>Unidade base</label><select class="sheet-select" id="novo-insumo-unidade"><option value="g">g</option><option value="ml">ml</option><option value="un">un</option></select></div>
        <div class="form-group"><label>Classe</label><select class="sheet-select" id="novo-insumo-classe"><option value="insumo">Ingrediente</option><option value="embalagem">Embalagem</option><option value="limpeza">Limpeza</option></select></div>
        <button class="btn btn-primary" onclick="submitNovoInsumoSeparado()" style="white-space:nowrap;">Cadastrar insumo</button>
      </div>
    </div>

    <div class="card" style="margin-bottom:14px;padding:14px 16px;border-left:3px solid var(--blue);">
      <div style="margin-bottom:10px;">
        <div style="font-size:13px;font-weight:800;color:var(--text);">2. Registrar nova compra</div>
        <div style="font-size:11px;color:var(--text-light);margin-top:2px;">Selecione um insumo já cadastrado e informe os dados desta compra. Fornecedor e data ficam gravados no histórico.</div>
      </div>
      <div style="display:grid;grid-template-columns:minmax(170px,1.5fr) minmax(150px,1.2fr) 135px 110px 120px auto;gap:8px;align-items:end;">
        <div class="form-group"><label>Insumo</label><input class="sheet-input" id="compra-insumo-nome" list="quick-insumo-list" autocomplete="off" placeholder="Selecione o insumo"></div>
        <div class="form-group"><label>Fornecedor</label><input class="sheet-input" id="compra-insumo-fornecedor" list="fornecedores-list" autocomplete="off" placeholder="Fornecedor"></div>
        <div class="form-group"><label>Data da compra</label><input class="sheet-input" id="compra-insumo-data" type="date"></div>
        <div class="form-group"><label>Quantidade</label><input class="sheet-input" id="compra-insumo-qtd" type="number" min="0.001" step="0.001" placeholder="Qtd."></div>
        <div class="form-group"><label>Valor total R$</label><input class="sheet-input" id="compra-insumo-custo" type="text" inputmode="decimal" oninput="maskMoney(this)" placeholder="0,00" onkeydown="if(event.key==='Enter'){event.preventDefault();submitCompraInsumoSeparada();}"></div>
        <button class="btn btn-primary" onclick="submitCompraInsumoSeparada()" style="white-space:nowrap;">Registrar compra</button>
      </div>
    </div>'''

if old_toolbar not in s:
    raise SystemExit('Nao encontrei toolbar original de insumos')
s = s.replace(old_toolbar, new_toolbar, 1)

quick_row = '<tr class="quick-entry-row" aria-label="Entrada rapida de insumo">'
if quick_row not in s:
    raise SystemExit('Nao encontrei linha rapida antiga')
s = s.replace(quick_row, '<tr class="quick-entry-row" aria-label="Entrada rapida de insumo" style="display:none;">', 1)

marker = 'function handleQuickInsumoKey(e) {'
if marker not in s:
    raise SystemExit('Nao encontrei ponto de insercao das funcoes de insumo')

new_funcs = r'''function ensureCompraInsumoDate() {
  const el = document.getElementById('compra-insumo-data');
  if (el && !el.value) el.value = todayISO();
}

function submitNovoInsumoSeparado() {
  const nomeEl = document.getElementById('novo-insumo-nome');
  const unidadeEl = document.getElementById('novo-insumo-unidade');
  const classeEl = document.getElementById('novo-insumo-classe');
  const nome = (nomeEl?.value || '').trim();
  if (!nome) return showToast('Informe o nome do insumo', 'error');

  const existente = ingredientes.find(i => normalizeLookupName(i.nome) === normalizeLookupName(nome));
  if (existente) {
    const compraNome = document.getElementById('compra-insumo-nome');
    if (compraNome) compraNome.value = existente.nome;
    ensureCompraInsumoDate();
    showToast('Este insumo já existe. Você pode registrar a compra abaixo.', 'error');
    document.getElementById('compra-insumo-fornecedor')?.focus();
    return;
  }

  ingredientes.unshift({
    id: ++nextId,
    nome,
    unidade: unidadeEl?.value || 'g',
    classe: classeEl?.value || 'insumo',
    qtdCompra: 0,
    custoCompra: 0,
    fatia: null,
    variacaoUnidade: null,
    historico: []
  });
  saveAll();
  renderCMV();
  renderProdutos();
  renderQuickInsumoList();

  const compraNome = document.getElementById('compra-insumo-nome');
  if (compraNome) compraNome.value = nome;
  if (nomeEl) nomeEl.value = '';
  if (unidadeEl) unidadeEl.value = 'g';
  if (classeEl) classeEl.value = 'insumo';
  ensureCompraInsumoDate();
  showToast('Insumo cadastrado. Agora registre a compra abaixo.', 'success');
  document.getElementById('compra-insumo-fornecedor')?.focus();
}

function submitCompraInsumoSeparada() {
  const nomeEl = document.getElementById('compra-insumo-nome');
  const fornecedorEl = document.getElementById('compra-insumo-fornecedor');
  const dataEl = document.getElementById('compra-insumo-data');
  const qtdEl = document.getElementById('compra-insumo-qtd');
  const custoEl = document.getElementById('compra-insumo-custo');

  const nome = (nomeEl?.value || '').trim();
  const fornecedor = (fornecedorEl?.value || '').trim();
  const data = dataEl?.value || '';
  const qtdCompra = parseFloat(qtdEl?.value) || 0;
  const custoCompra = parseMoney(custoEl?.value);

  if (!nome) return showToast('Selecione o insumo da compra', 'error');
  const ing = ingredientes.find(i => normalizeLookupName(i.nome) === normalizeLookupName(nome));
  if (!ing) return showToast('Este insumo ainda não está cadastrado. Cadastre-o primeiro.', 'error');
  if (!fornecedor) return showToast('Informe o fornecedor', 'error');
  if (!data) return showToast('Informe a data da compra', 'error');
  if (!(qtdCompra > 0)) return showToast('Informe a quantidade comprada', 'error');
  if (!(custoCompra > 0)) return showToast('Informe o valor total da compra', 'error');

  if (!Array.isArray(ing.historico)) ing.historico = [];
  ing.historico.push({ id: ++nextId, fornecedor, data, qtdCompra, custoCompra });
  syncIngredienteFromHistorico(ing);
  saveAll();
  refreshProductCostsFromRecipes();
  renderCMV();
  renderProdutos();

  if (nomeEl) nomeEl.value = '';
  if (fornecedorEl) fornecedorEl.value = '';
  if (qtdEl) qtdEl.value = '';
  if (custoEl) custoEl.value = '';
  if (dataEl) dataEl.value = todayISO();
  showToast(`Compra de ${ing.nome} registrada`, 'success');
  nomeEl?.focus();
}

'''
s = s.replace(marker, new_funcs + marker, 1)

start = s.find('function openFichaParaProduto(prodId, addIfEmpty = false) {')
end_marker = '\nfunction renderReceitaFlat() {'
if start == -1:
    raise SystemExit('Nao encontrei openFichaParaProduto atual')
end = s.find(end_marker, start)
if end == -1:
    raise SystemExit('Nao encontrei fim de openFichaParaProduto')

new_ficha = r'''function openFichaParaProduto(prodId, addIfEmpty = true) {
  const id = parseInt(prodId);
  if (!id) return;

  // Se o clique veio do CMV/Fabricação, primeiro abre a página que contém o editor.
  showPage('insumos');
  setInsumosTab('receitas');

  // Remove busca antiga para garantir que o produto clicado não fique escondido.
  fichaBusca = '';
  const busca = document.querySelector('#cmv-panel-receitas input[placeholder="Buscar produto..."]');
  if (busca) busca.value = '';
  setReceitaView('grouped');

  const temFicha = getReceitasByProduto(id).length > 0;
  if (!temFicha) {
    addReceitaRow(id);
  } else {
    renderReceitaSheet();
  }

  setTimeout(() => {
    const el = document.querySelector(`[data-prod-ficha="${id}"]`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      const campo = el.querySelector('select, input');
      if (campo) campo.focus();
    }
  }, 140);
}
'''
s = s[:start] + new_ficha + s[end:]

# Ao abrir a aba de ingredientes, já deixa a data da nova compra preenchida com hoje.
set_tab_marker = "function setInsumosTab(tab) {\n  currentInsumosTab = tab;"
if set_tab_marker not in s:
    raise SystemExit('Nao encontrei setInsumosTab')
s = s.replace(set_tab_marker, set_tab_marker + "\n  if (tab === 'ingredientes') setTimeout(ensureCompraInsumoDate, 0);", 1)

required = [
    '1. Cadastrar insumo',
    '2. Registrar nova compra',
    'function submitCompraInsumoSeparada()',
    "showPage('insumos');",
    "if (!temFicha) {\n    addReceitaRow(id);"
]
for x in required:
    if x not in s:
        raise SystemExit('Marcador ausente: ' + x)

path.write_text(s, encoding='utf-8')

scripts = [x for x in re.findall(r'<script(?:[^>]*)>(.*?)</script>', s, re.S) if x.strip()]
if not scripts:
    raise SystemExit('Nenhum script inline para validar')
js = max(scripts, key=len)
Path('/tmp/ddv_app.js').write_text(js, encoding='utf-8')
subprocess.run(['node', '--check', '/tmp/ddv_app.js'], check=True)
print('UI fix aplicada e JavaScript validado.')
