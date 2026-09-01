from pathlib import Path

p = Path('.github/scripts/cmv_fix.py')
s = p.read_text(encoding='utf-8')
old1 = "    end = s.find('\\n\\n' + next_sig, start)"
new1 = "    end = s.find(next_sig, start + len(start_sig))"
old2 = "    s = s[:start] + new_block.rstrip() + s[end:]"
new2 = "    s = s[:start] + new_block.rstrip() + '\\n\\n' + s[end:]"
if old1 not in s:
    raise SystemExit('helper: localizador antigo nao encontrado')
if old2 not in s:
    raise SystemExit('helper: montagem antiga nao encontrada')
s = s.replace(old1, new1, 1).replace(old2, new2, 1)
p.write_text(s, encoding='utf-8')
print('Localizador de blocos ajustado para ignorar espacamento.')
