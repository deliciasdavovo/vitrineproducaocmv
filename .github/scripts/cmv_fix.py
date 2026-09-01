from pathlib import Path
import re
import subprocess

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_between(start_sig, next_sig, new_block, label):
    global s
    start = s.find(start_sig)
    if start < 0:
        raise SystemExit(f'Nao encontrei inicio de {label}: {start_sig}')
    end = s.find('\n\n' + next_sig, start)
    if end < 0:
        raise SystemExit(f'Nao encontrei fim de {label}: {next_sig}')
    s = s[:start] + new_block.rstrip() + s[end:]


replace_between(
    'function handleQuickInsumoKey(e) {',
    'function submitQuickInsumo() {',
    r'''function handleQuickInsumoKey(e) {
  if (e.key !== 'Enter' || e.ctrlKey || e.metaKey || e.altKey) return;
  e.preventDefault();

  const t = e.target;
  const fields = ['quick-insumo-nome','quick-insumo-unidade','quick-insumo-fornecedor','quick-insumo-data','quick-insumo-qtd','quick-insumo-custo']
    .map(id => document.getElementById(id))
    .filter(el => el && !el.disabled);
  const index = fields.indexOf(t);

  if (e.shiftKey) {
    if (index > 0) fields[index - 1].focus();
    return;
  }

  // Se houver sugestao da ultima compra, Enter aceita antes de avancar.
  if (t && t.dataset && t.dataset.ghost != null && t.dataset.ghost !== '' && !t.value) {
    t.value = t.dataset.ghost;
    delete t.dataset.ghost;
    if (t.id === 'quick-insumo-custo') maskMoney(t);
  }

  if (index >= 0 && index < fields.length - 1) {
    fields[index + 1].focus();
    return;
  }

  // Ultima coluna: salva e abre a proxima linha (submit limpa e volta ao nome).
  if (index === fields.length - 1) submitQuickInsumo();
}''',
    'navegacao da compra rapida'
)

replace_between(
    'function setQuickInsumoGhosts(nome) {',
    'function applyQuickInsumoExistingMeta(nome) {',
    r'''function setQuickInsumoGhosts(nome) {
  const uc = ultimaCompraPorNome(nome);
  if (!uc) { clearQuickInsumoGhosts(); return; }

  applyQuickGhost('quick-insumo-fornecedor', uc.fornecedor || '', uc.fornecedor || '');
  const qtd = Number(uc.qtdCompra) > 0 ? String(uc.qtdCompra) : '';
  applyQuickGhost('quick-insumo-qtd', qtd, qtd);
  const custo = Number(uc.custoCompra) > 0 ? moneyInputVal(uc.custoCompra) : '';
  applyQuickGhost('quick-insumo-custo', custo, custo ? 'R$ ' + custo : '');

  // Alem do placeholder, mostra a ultima compra de forma explicita na linha.
  const hint = document.getElementById('quick-insumo-lock-hint');
  if (hint) {
    const key = normalizeLookupName(nome);
    const ing = ingredientes.find(i => normalizeLookupName(i.nome) === key);
    const rev = produtos.find(p => (p.tipo || 'fabricacao') === 'revenda' && normalizeLookupName(p.nome) === key);
    const unidade = ing?.unidade || rev?.compraUnidade || rev?.precoUnidade || '';
    const dataTxt = uc.data ? new Date(uc.data + 'T12:00:00').toLocaleDateString('pt-BR') : '';
    const custoTxt = Number(uc.custoCompra) > 0
      ? Number(uc.custoCompra).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
      : '';
    const partes = [
      Number(uc.qtdCompra) > 0 ? `${uc.qtdCompra}${unidade ? ' ' + unidade : ''}` : '',
      custoTxt,
      uc.fornecedor || '',
      dataTxt
    ].filter(Boolean);
    if (partes.length) {
      hint.innerHTML += `<div style="margin-top:5px;color:var(--text);"><strong>Ultima compra:</strong> ${partes.map(escHtml).join(' · ')}</div>`;
    }
  }
}''',
    'resumo da ultima compra'
)

replace_between(
    'async function salvarReceitaItens(receita, syncErrors) {',
    'function syncToSupabase() {',
    r'''async function salvarReceitaItens(receita, syncErrors) {
  // Nunca apaga primeiro. Le as linhas antigas, grava as novas e so depois
  // remove as antigas. Se a rede falhar, a ficha anterior continua intacta.
  const atuais = await db.from('receita_itens').select('id').eq('receita_id', receita.id);
  if (atuais?.error) {
    syncErrors.push({ label: 'ler itens atuais da ficha', error: atuais.error });
    console.error('Supabase: ler itens atuais da ficha', atuais.error);
    return false;
  }
  const idsAntigos = (atuais?.data || []).map(x => x.id).filter(Boolean);

  if (!receita.itens?.length) {
    if (idsAntigos.length) {
      await runSupabase('limpar itens da ficha', db.from('receita_itens').delete().in('id', idsAntigos), syncErrors);
    }
    return true;
  }

  const itensComUnidadeUso = receita.itens.map(item => ({
    receita_id: receita.id,
    ing_id: item.ingId,
    qtd: item.qtd,
    uso_unidade: item.usoUnidade || null
  }));

  let insert = await db.from('receita_itens').insert(itensComUnidadeUso).select('id');
  if (insert?.error) {
    const detalhe = `${insert.error.message || ''} ${insert.error.details || ''} ${insert.error.hint || ''}`;
    if (/uso_unidade/i.test(detalhe)) {
      console.warn('Supabase: coluna uso_unidade ausente; salvando ficha no formato antigo.', insert.error);
      const itensSemUnidadeUso = receita.itens.map(item => ({
        receita_id: receita.id,
        ing_id: item.ingId,
        qtd: item.qtd
      }));
      insert = await db.from('receita_itens').insert(itensSemUnidadeUso).select('id');
    }
  }

  if (insert?.error) {
    syncErrors.push({ label: 'salvar itens da ficha', error: insert.error });
    console.error('Supabase: salvar itens da ficha', insert.error);
    return false;
  }

  const idsNovos = (insert?.data || []).map(x => x.id).filter(Boolean);
  if (idsAntigos.length) {
    await runSupabase('substituir itens antigos da ficha', db.from('receita_itens').delete().in('id', idsAntigos), syncErrors);
  }
  if (!idsNovos.length) console.warn('Ficha salva sem IDs retornados; mantendo dados locais como backup.');
  return true;
}''',
    'gravacao segura das fichas'
)

# Recuperacao passa a ser por ficha, e nao apenas quando a tabela inteira vem vazia.
start = s.find('    const itensLocaisPorReceita = {};')
end_marker = '    dedupeIngredientesByName();'
end = s.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit('Nao encontrei o bloco de recuperacao das fichas')
load_new = r'''    const itensLocaisPorReceita = {};
    receitasLocalAntesLoad.forEach(r => {
      if (r.itens?.length) itensLocaisPorReceita[r.id] = r.itens;
    });
    const itensBackupPorReceita = {};
    (getStorage('ddv_receitas_backup', []) || []).forEach(r => {
      if (r.itens?.length) itensBackupPorReceita[r.id] = r.itens;
    });
    receitas = (recData || []).map(r => {
      const nuvem = itensPorReceita[r.id] || [];
      const local = itensLocaisPorReceita[r.id] || [];
      const backup = itensBackupPorReceita[r.id] || [];
      const itens = nuvem.length ? nuvem : (local.length ? local : backup);
      if (!nuvem.length && itens.length) {
        console.warn(`Ficha ${r.id} veio sem itens da nuvem; recuperando copia local.`);
      }
      return {
        id: r.id, prodId: r.prod_id, rendimento: Number(r.rendimento), unidade: r.unidade,
        pesoPorUnidade: r.peso_por_unidade ? Number(r.peso_por_unidade) : null,
        itens
      };
    });
'''
s = s[:start] + load_new + s[end:]

replace_between(
    'function addReceitaRow(prodId = null) {',
    'function insertReceitaRowAfter(id) {',
    r'''function addReceitaRow(prodId = null) {
  if (!produtos.length) return showToast('Cadastre um produto antes da receita', 'error');
  if (!ingredientes.length) return showToast('Cadastre um ingrediente antes da receita', 'error');
  const produtoId = parseInt(prodId) || produtos[0].id;
  const newId = ++nextId;
  lastAddedReceitaId = newId;
  receitas.push({
    id: newId,
    prodId: produtoId,
    rendimento: 1,
    unidade: 'un.',
    itens: [{ ingId: ingredientes[0].id, qtd: 0 }]
  });
  saveAll();
  renderCMV();
  focusReceitaRow(newId, 0);
  setTimeout(() => {
    const el = document.querySelector(`tr[data-receita-id="${newId}"]`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    lastAddedReceitaId = null;
  }, 80);
}''',
    'criacao de linha de ficha'
)

replace_between(
    'function insertReceitaRowAfter(id) {',
    'function duplicateReceita(id) {',
    r'''function focusReceitaRow(id, fieldIndex = 0) {
  setTimeout(() => {
    const row = document.querySelector(`tr[data-receita-id="${id}"]`);
    if (!row) return;
    const fields = [...row.querySelectorAll('input:not([disabled]), select:not([disabled]), textarea:not([disabled])')];
    const field = fields[Math.max(0, Math.min(fieldIndex, fields.length - 1))];
    if (field) {
      field.focus();
      if (field.select && field.tagName === 'INPUT') field.select();
    }
  }, 30);
}

function insertReceitaRowAfter(id) {
  if (!produtos.length) return showToast('Cadastre um produto antes da receita', 'error');
  if (!ingredientes.length) return showToast('Cadastre um ingrediente antes da receita', 'error');
  const idx = receitas.findIndex(r => r.id === id);
  if (idx === -1) return addReceitaRow();
  const ref = receitas[idx];
  const newId = ++nextId;
  receitas.splice(idx + 1, 0, {
    id: newId,
    prodId: ref.prodId,
    rendimento: getProdutoReceitaRendimento(ref.prodId),
    unidade: getProdutoReceitaUnidade(ref.prodId),
    pesoPorUnidade: getProdutoPesoPorUnidade(ref.prodId) || null,
    itens: [{ ingId: ingredientes[0].id, qtd: 0 }]
  });
  saveAll();
  renderCMV();
  focusReceitaRow(newId, 0);
}

function handleReceitaSheetKey(e) {
  if (e.key !== 'Enter' || e.ctrlKey || e.metaKey || e.altKey) return;
  const row = e.target.closest?.('#receitas-container tr[data-receita-id]');
  if (!row) return;
  const fields = [...row.querySelectorAll('input:not([disabled]), select:not([disabled]), textarea:not([disabled])')];
  const index = fields.indexOf(e.target);
  if (index < 0) return;
  e.preventDefault();
  e.stopPropagation();
  const receitaId = Number(row.dataset.receitaId);

  if (e.shiftKey) {
    if (index <= 0) return;
    e.target.blur();
    setTimeout(() => focusReceitaRow(receitaId, index - 1), 0);
    return;
  }

  if (index < fields.length - 1) {
    e.target.blur();
    setTimeout(() => focusReceitaRow(receitaId, index + 1), 0);
    return;
  }

  // Ultima celula: cria imediatamente outra linha do MESMO produto.
  e.target.blur();
  setTimeout(() => insertReceitaRowAfter(receitaId), 0);
}
document.addEventListener('keydown', handleReceitaSheetKey, true);''',
    'navegacao das fichas'
)

required = [
    'function handleReceitaSheetKey(e)',
    "select('id').eq('receita_id', receita.id)",
    'recuperando copia local',
    '<strong>Ultima compra:</strong>'
]
for marker in required:
    if marker not in s:
        raise SystemExit('Marcador final ausente: ' + marker)

path.write_text(s, encoding='utf-8')

# Extrai o maior script inline e usa o parser do Node para impedir commit com JS quebrado.
scripts = [x for x in re.findall(r'<script(?:[^>]*)>(.*?)</script>', s, re.S) if x.strip()]
if not scripts:
    raise SystemExit('Nenhum script inline encontrado')
js_path = Path('/tmp/ddv-app.js')
js_path.write_text(max(scripts, key=len), encoding='utf-8')
subprocess.run(['node', '--check', str(js_path)], check=True)
print('CMV/fichas patch aplicado e JavaScript validado.')
