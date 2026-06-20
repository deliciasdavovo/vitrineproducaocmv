-- ============================================================
-- Inserir FICHAS TÉCNICAS (receitas + ingredientes) que ainda NÃO existem
-- ------------------------------------------------------------
-- Como usar:
--   1. Abra https://supabase.com e entre no seu projeto
--   2. Menu lateral: "SQL Editor" -> "New query"
--   3. Cole TODO este conteúdo e clique em "Run"
--
-- É SEGURO e idempotente:
--   * Só cria ficha para produtos que AINDA NÃO têm ficha.
--   * Não altera nem apaga fichas já existentes.
--   * O cruzamento de nomes ignora espaços e maiúsculas/minúsculas.
--   * No final mostra os nomes que NÃO foram encontrados no cadastro.
--   * Pode rodar quantas vezes quiser.
-- ============================================================

create temp table _stage (produto text, ingrediente text, qtd numeric, unidade text);

insert into _stage (produto, ingrediente, qtd, unidade) values
('Café casa G - COADO NA HR','Café coador Jaguari',16,'g'),
('Café casa PQ - COADO NA HR','Café coador Jaguari',9,'g'),
('Café com leite G Expresso','Café em grãos Toledo',10,'g'),
('Café com leite G Expresso','Leite',100,'ml'),
('Café com leite PQ Expresso','Café em grãos Toledo',10,'g'),
('Café com leite PQ Expresso','Leite',50,'ml'),
('Capuccino G','Capuccino em pó Bevaccino',24,'g'),
('Capuccino G','Leite',100,'ml'),
('Capuccino gelado','Calda de chocolate',20,'g'),
('Capuccino gelado','Capuccino em pó Bevaccino',35,'g'),
('Capuccino gelado','Leite',250,'ml'),
('Capuccino italiano','Café em grãos Toledo',10,'g'),
('Capuccino italiano','Chocolate em pó 50 % Mavalerio',15,'g'),
('Capuccino italiano','Leite',100,'ml'),
('Capuccino PQ','Capuccino em pó Bevaccino',12,'g'),
('Capuccino PQ','Leite',50,'ml'),
('Chocolate quente grande - meio amargo','Chocolate em pó 50 % Mavalerio',12,'g'),
('Chocolate quente grande - meio amargo','Leite',120,'ml'),
('Chocolate quente pequeno - meio amargo','Chocolate em pó 50 % Mavalerio',6,'g'),
('Chocolate quente pequeno - meio amargo','Leite',70,'ml'),
('Expresso Duplo','Café em grãos Toledo',15,'g'),
('Expresso PQ','Café em grãos Toledo',10,'g'),
('Gelado de chocolate Meio amargo','Calda de chocolate',20,'g'),
('Gelado de chocolate Meio amargo','Chocolate em pó 50 % Mavalerio',20,'g'),
('Gelado de chocolate Meio amargo','Leite',250,'ml'),
('Gelado de chocolate Toddy','Calda de chocolate',20,'g'),
('Gelado de chocolate Toddy','Leite',250,'ml'),
('Gelado de chocolate Toddy','Toddy',20,'g'),
('Leite puro','Leite',200,'ml'),
('Ovolmaltine gelado','Calda de chocolate',20,'g'),
('Ovolmaltine gelado','Leite',250,'ml'),
('Ovolmaltine gelado','Ovomaltine',35,'g'),
('Brigadeiro unitário','Chocolate em pó 50 % Mavalerio',50,'g'),
('Brigadeiro unitário','Leite condesado Moça',2,'un'),
('Brigadeiro unitário','Manteiga Alto Alegre',60,'g'),
('Camafeu','Nozes sem casca',175,'g'),
('Camafeu','Leite condesado Moça',2,'un'),
('Camafeu','Margarina Coamo',30,'g'),
('Camafeu','Fondant 1KG MIX',700,'g'),
('Pão de Mel','Leite condesado Moça',480,'g'),
('Pão de Mel','Chocolate ao leite barra CargilL',850,'g'),
('Pão de Mel','Pré Mistura Bolo Chocomousse Fleishman',500,'g'),
('Pão de Mel','Oléo Liza 900ml',100,'ml'),
('Pão de Mel','Ovos',200,'g'),
('Pão de Mel','Ganache Toffee Vabene 4kg',30,'g'),
('Bauru','Pão francês',1,'un'),
('Bauru','Presunto Magro Sadia',2,'un'),
('Bauru','Queijo Muçarela Lacmon',2,'un'),
('Bauru','Tomate',2,'un'),
('Chapa','Manteiga Alto Alegre',50,'g'),
('Chapa','Pão francês',1,'un'),
('Integral com requeijão chapa','Manteiga Alto Alegre',30,'g'),
('Integral com requeijão chapa','Pão integral 70%',1,'un'),
('Integral com requeijão chapa','Requeijão Catupiry',50,'g'),
('Integral na chapa','Pão integral 70%',1,'un'),
('Integral na chapa','Manteiga Alto Alegre',50,'g'),
('Lanche de salame','Salame Italiano Sadia',6,'un'),
('Lanche de salame','Pão francês',1,'un'),
('Lanche de salame','Queijo Muçarela Lacmon',2,'un'),
('Lanche natural FR','Frango desfiado',60,'g'),
('Lanche natural FR','Maionese',100,'g'),
('Lanche natural FR','Pão pullman integral',3,'un'),
('Lanche natural FR','Tomate',4,'un'),
('Lanche natural FR','Pão pullman integral',3,'un'),
('Lanche natural FR','Frango desfiado',70,'g'),
('Lanche natural FR','Tomate',4,'un'),
('Lanche natural FR','Alface',70,'g'),
('Lanche natural FR','Maionese',100,'g'),
('Lanche natural PP','Pão pullman integral',3,'un'),
('Lanche natural PP','Peito de peru Sadia',4,'un'),
('Lanche natural PP','Queijo branco',1,'un'),
('Lanche natural PP','Tomate',4,'un'),
('Lanche natural PP','Alface',70,'g'),
('Lanche natural PP','Maionese',80,'g'),
('Lanche natural PQ','Pão pullman integral',3,'un'),
('Lanche natural PQ','Presunto Magro Seara',4,'un'),
('Lanche natural PQ','Queijo Muçarela Lacmon',4,'un'),
('Lanche natural PQ','Tomate',4,'un'),
('Lanche natural PQ','Alface',70,'g'),
('Lanche natural PQ','Maionese',80,'g'),
('Manteiga frio','Pão francês',1,'un'),
('Manteiga frio','Manteiga Alto Alegre',50,'g'),
('Misto frio','Pão francês',1,'un'),
('Misto frio','Presunto Magro Sadia',1.5,'un'),
('Misto frio','Queijo Muçarela Lacmon',1.5,'un'),
('Misto quente','Manteiga Alto Alegre',20,'g'),
('Misto quente','Pão francês',1,'un'),
('Misto quente','Presunto Magro Sadia',2,'un'),
('Misto quente','Queijo Muçarela Lacmon',2,'un'),
('Ovos mexidos','Ovos',2,'un'),
('Ovos mexidos','Manteiga Alto Alegre',50,'g'),
('Pão com ovo','Manteiga Alto Alegre',30,'g'),
('Pão com ovo','Ovos',2,'un'),
('Pão com ovo','Pão francês',1,'un'),
('Pão com requeijão chapa','Manteiga Alto Alegre',30,'g'),
('Pão com requeijão chapa','Pão francês',1,'un'),
('Pão com requeijão chapa','Requeijão Catupiry',50,'g'),
('Peito de peru light','Tomate',2,'un'),
('Peito de peru light','Pão integral 70%',1,'un'),
('Peito de peru light','Peito de peru Sadia',2,'un'),
('Peito de peru light','Queijo branco',1,'un'),
('Peito de peru quente','Pão francês',1,'un'),
('Peito de peru quente','Peito de peru Sadia',2,'un'),
('Peito de peru quente','Queijo Muçarela Lacmon',2,'un'),
('Queijo quente branco','Pão francês',1,'un'),
('Queijo quente branco','Queijo branco',1,'un'),
('Queijo quente light','Tomate',2,'un'),
('Queijo quente light','Pão integral 70%',1,'un'),
('Queijo quente light','Queijo branco',1,'un'),
('Queijo quente mussarela','Pão francês',1,'un'),
('Queijo quente mussarela','Queijo Muçarela Lacmon',4,'un'),
('Queijo quente prato','Pão francês',1,'un'),
('Queijo quente prato','Queijo prato',3,'un'),
('Requeijão frio','Requeijão Catupiry',50,'g'),
('Requeijão frio','Pão francês',1,'un'),
('Crepioca FR c/ catupiry','Frango desfiado',70,'g'),
('Crepioca FR c/ catupiry','Ovos',1,'un'),
('Crepioca FR c/ catupiry','Requeijão cremoso Coronata',60,'g'),
('Crepioca FR c/ catupiry','Tapioca terrinha',50,'g'),
('Crepioca FR c/ muçarela','Frango desfiado',70,'g'),
('Crepioca FR c/ muçarela','Ovos',1,'un'),
('Crepioca FR c/ muçarela','Queijo Muçarela Lacmon',2,'un'),
('Crepioca FR c/ muçarela','Tapioca terrinha',50,'g'),
('Crepioca FR c/ Q. Branco','Frango desfiado',70,'g'),
('Crepioca FR c/ Q. Branco','Ovos',1,'un'),
('Crepioca FR c/ Q. Branco','Queijo branco',1,'un'),
('Crepioca FR c/ Q. Branco','Tapioca terrinha',50,'g'),
('Crepioca FR c/ Q. prato','Frango desfiado',70,'g'),
('Crepioca FR c/ Q. prato','Ovos',1,'un'),
('Crepioca FR c/ Q. prato','Queijo prato',2,'un'),
('Crepioca FR c/ Q. prato','Tapioca terrinha',50,'g'),
('Crepioca PP/ Q. branco','Ovos',1,'un'),
('Crepioca PP/ Q. branco','Peito de peru Sadia',2,'un'),
('Crepioca PP/ Q. branco','Queijo branco',1,'un'),
('Crepioca PP/ Q. branco','Tapioca terrinha',50,'g'),
('Crepioca PQ','Ovos',1,'un'),
('Crepioca PQ','Presunto Magro Sadia',2,'un'),
('Crepioca PQ','Queijo Muçarela Lacmon',2,'un'),
('Crepioca PQ','Tapioca terrinha',50,'g'),
('Crepioca Rucula / tom. seco/ Q. Branco','Ovos',1,'un'),
('Crepioca Rucula / tom. seco/ Q. Branco','Queijo branco',1,'un'),
('Crepioca Rucula / tom. seco/ Q. Branco','Rucúla',40,'g'),
('Crepioca Rucula / tom. seco/ Q. Branco','Tapioca terrinha',50,'g'),
('Crepioca Rucula / tom. seco/ Q. Branco','Tomate Seco',30,'g'),
('Hamburguer - Cheeseburguer','Hamburguer artesanal',1,'un'),
('Hamburguer - Cheeseburguer','Pão pullman hamburguer',1,'un'),
('Hamburguer - Cheeseburguer','Queijo prato',2,'un'),
('Omelete 1 CAM - FR c/ catupiry','Frango desfiado',70,'g'),
('Omelete 1 CAM - FR c/ catupiry','Ovos',2,'un'),
('Omelete 1 CAM - FR c/ catupiry','Queijo Muçarela Lacmon',1,'un'),
('Omelete 1 CAM - FR c/ catupiry','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - FR c/ catupiry','Requeijão cremoso Coronata',60,'g'),
('Omelete 1 CAM - FR c/ muçarela','Frango desfiado',70,'g'),
('Omelete 1 CAM - FR c/ muçarela','Ovos',2,'un'),
('Omelete 1 CAM - FR c/ muçarela','Queijo Muçarela Lacmon',3,'un'),
('Omelete 1 CAM - FR c/ muçarela','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - FR c/ Queijo Branco','Frango desfiado',70,'g'),
('Omelete 1 CAM - FR c/ Queijo Branco','Ovos',2,'un'),
('Omelete 1 CAM - FR c/ Queijo Branco','Queijo branco',1,'un'),
('Omelete 1 CAM - FR c/ Queijo Branco','Queijo Muçarela Lacmon',1,'un'),
('Omelete 1 CAM - FR c/ Queijo Branco','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - FR c/ Queijo Prato','Frango desfiado',70,'g'),
('Omelete 1 CAM - FR c/ Queijo Prato','Ovos',2,'un'),
('Omelete 1 CAM - FR c/ Queijo Prato','Queijo Muçarela Lacmon',1,'un'),
('Omelete 1 CAM - FR c/ Queijo Prato','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - FR c/ Queijo Prato','Queijo prato',2,'un'),
('Omelete 1 CAM - PQ','Ovos',2,'un'),
('Omelete 1 CAM - PQ','Presunto Magro Sadia',2,'un'),
('Omelete 1 CAM - PQ','Queijo Muçarela Lacmon',3,'un'),
('Omelete 1 CAM - PQ','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Ovos',2,'un'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Queijo branco',1,'un'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Queijo Muçarela Lacmon',1,'un'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Queijo Parmesão Scala',10,'g'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Rucúla',40,'g'),
('Omelete 1 CAM - Rúcula/ tom. seco/ Q branco','Tomate Seco',30,'g'),
('Omelete 2 CAM - FR c/ catupiry','Frango desfiado',120,'g'),
('Omelete 2 CAM - FR c/ catupiry','Ovos',2,'un'),
('Omelete 2 CAM - FR c/ catupiry','Queijo Muçarela Lacmon',1,'un'),
('Omelete 2 CAM - FR c/ catupiry','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - FR c/ catupiry','Requeijão cremoso Coronata',100,'g'),
('Omelete 2 CAM - FR c/ muçarela','Frango desfiado',120,'g'),
('Omelete 2 CAM - FR c/ muçarela','Ovos',2,'un'),
('Omelete 2 CAM - FR c/ muçarela','Queijo Muçarela Lacmon',5,'un'),
('Omelete 2 CAM - FR c/ muçarela','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - FR c/ Queijo Branco','Frango desfiado',120,'g'),
('Omelete 2 CAM - FR c/ Queijo Branco','Ovos',2,'un'),
('Omelete 2 CAM - FR c/ Queijo Branco','Queijo branco',2,'un'),
('Omelete 2 CAM - FR c/ Queijo Branco','Queijo Muçarela Lacmon',1,'un'),
('Omelete 2 CAM - FR c/ Queijo Branco','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - FR c/ Queijo Prato','Frango desfiado',120,'g'),
('Omelete 2 CAM - FR c/ Queijo Prato','Ovos',2,'un'),
('Omelete 2 CAM - FR c/ Queijo Prato','Queijo Muçarela Lacmon',1,'un'),
('Omelete 2 CAM - FR c/ Queijo Prato','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - FR c/ Queijo Prato','Queijo prato',4,'un'),
('Omelete 2 CAM - PQ','Ovos',2,'un'),
('Omelete 2 CAM - PQ','Presunto Magro Sadia',4,'un'),
('Omelete 2 CAM - PQ','Queijo Muçarela Lacmon',5,'un'),
('Omelete 2 CAM - PQ','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Ovos',2,'un'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Queijo branco',1.5,'un'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Queijo Muçarela Lacmon',1,'un'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Queijo Parmesão Scala',10,'g'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Rucúla',50,'g'),
('Omelete 2 CAM - Rúcula/ tom. seco/ Q branco','Tomate Seco',50,'g'),
('Omelete sem recheio','Manteiga Alto Alegre',30,'g'),
('Omelete sem recheio','Ovos',2,'un'),
('Omelete sem recheio','Queijo Muçarela Lacmon',1,'un'),
('Tapioca FR c/ catupiry','Frango desfiado',70,'g'),
('Tapioca FR c/ catupiry','Requeijão cremoso Coronata',60,'g'),
('Tapioca FR c/ catupiry','Tapioca terrinha',100,'g'),
('Tapioca FR c/ muçarela','Frango desfiado',70,'g'),
('Tapioca FR c/ muçarela','Queijo Muçarela Lacmon',2,'un'),
('Tapioca FR c/ muçarela','Tapioca terrinha',100,'g'),
('Tapioca FR c/ Q. Branco','Frango desfiado',70,'g'),
('Tapioca FR c/ Q. Branco','Queijo branco',1,'un'),
('Tapioca FR c/ Q. Branco','Tapioca terrinha',100,'g'),
('Tapioca FR c/ Q. prato','Frango desfiado',70,'g'),
('Tapioca FR c/ Q. prato','Queijo prato',2,'un'),
('Tapioca FR c/ Q. prato','Tapioca terrinha',100,'g'),
('Tapioca PP/ Q. branco','Peito de peru Sadia',2,'un'),
('Tapioca PP/ Q. branco','Queijo branco',1,'un'),
('Tapioca PP/ Q. branco','Tapioca terrinha',100,'g'),
('Tapioca PQ','Tapioca terrinha',100,'g'),
('Tapioca PQ','Presunto Magro Sadia',2,'un'),
('Tapioca PQ','Queijo Muçarela Lacmon',2,'un'),
('Tapioca Rucula / tom. seco/ Q. Branco','Queijo branco',1,'un'),
('Tapioca Rucula / tom. seco/ Q. Branco','Rucúla',40,'g'),
('Tapioca Rucula / tom. seco/ Q. Branco','Tapioca terrinha',100,'g'),
('Tapioca Rucula / tom. seco/ Q. Branco','Tomate Seco',30,'g'),
('Shake proteico','Whey Black Skull',30,'g'),
('Shake proteico com café','Café expresso',1,'un'),
('Shake proteico com café','Whey Black Skull',30,'g'),
('Suco Caju','Caju poupa',1,'un'),
('Suco Frutas Vermelhas','Frutas vermelhas poupa',1,'un'),
('Suco Maracujá','Maracuja poupa',1,'un'),
('Palha Italiana','Bolacha Maizena 200g',350,'g'),
('Palha Italiana','Leite condesado Moça',3,'un'),
('Palha Italiana','Creme de leite',1,'un'),
('Palha Italiana','Chocolate em pó 50% Melken',70,'g'),
('Palha Italiana','Margarina Coamo',50,'g'),
('Palha Italiana','Açucar refinado',200,'g');

-- ------------------------------------------------------------
-- 1) Cria a ficha (receita) só para produtos que existem e ainda NÃO têm ficha
-- ------------------------------------------------------------
create temp table _newrec (id bigint, prod_id bigint);

with prod_match as (
  select distinct p.id as prod_id
  from _stage s
  join produtos p on lower(trim(p.nome)) = lower(trim(s.produto))
),
to_add as (
  select pm.prod_id
  from prod_match pm
  where not exists (select 1 from receitas r where r.prod_id = pm.prod_id)
),
numbered as (
  select prod_id,
         (select coalesce(max(id),0) from receitas) + row_number() over (order by prod_id) as new_id
  from to_add
),
ins as (
  insert into receitas (id, prod_id, rendimento, unidade)
  select new_id, prod_id, 1, 'un.' from numbered
  returning id, prod_id
)
insert into _newrec (id, prod_id) select id, prod_id from ins;

-- ------------------------------------------------------------
-- 2) Insere os ingredientes apenas das fichas recém-criadas
-- ------------------------------------------------------------
insert into receita_itens (receita_id, ing_id, qtd, uso_unidade)
select nr.id, i.id, s.qtd, s.unidade
from _stage s
join produtos p     on lower(trim(p.nome)) = lower(trim(s.produto))
join _newrec nr     on nr.prod_id = p.id
join ingredientes i on lower(trim(i.nome)) = lower(trim(s.ingrediente));

-- ------------------------------------------------------------
-- 3) RELATÓRIO: nomes da sua lista que NÃO foram encontrados no cadastro.
--    (Esses itens NÃO entraram. Cadastre o produto/ingrediente e rode de novo.)
-- ------------------------------------------------------------
select 'PRODUTO não cadastrado' as aviso, x.nome
from (select distinct produto as nome from _stage) x
where not exists (select 1 from produtos p where lower(trim(p.nome)) = lower(trim(x.nome)))
union all
select 'INGREDIENTE não cadastrado' as aviso, x.nome
from (select distinct ingrediente as nome from _stage) x
where not exists (select 1 from ingredientes i where lower(trim(i.nome)) = lower(trim(x.nome)))
order by 1, 2;
