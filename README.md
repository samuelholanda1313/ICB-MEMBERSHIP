1 OBJETIVOS DESTE DOCUMENTO

	Visa documentar o projeto de desenvolvimento do sistema Web criado para uma instituição religiosa do Estado do Ceará, com criação e revisão feitos pela equipe de Desenvolvimento de cinco Alunos do 4° Semestre do Curso de Análise e Desenvolvimento de Sistemas da Unifor através da disciplina de Projeto Aplicado de Desenvolvimento de Software - Etapa 1 sob supervisão pedagógica do Professor Orientador Ronnison Reges Vidal.


2 SITUAÇÃO ATUAL E JUSTIFICATIVA DO PROJETO

A maioria das igrejas hoje desconhece a quantidade de membros que frequentam assiduamente seus templos, tampouco consegue identificá-los se preciso, seja pra uma simples visita ao membro, seja para realização de uma campanha qualquer que requeira uma mobilização do quadro de membros ativos (assíduos). Entendendo todo o potencial desta instituição como agente de mudanças espiritual/social da comunidade em que está inserida, se faz necessário virtualizar o processo de Cadastro e Identificação de sua membresia como ferramenta propulsora para realização de projetos, eventos, e também dos próprios cultos com mais qualidade, uma vez que ao compreender mais e melhor o público com a qual a mesma está lidando, a mesma conseguirá ter mais eficácia em suas atividades e projetos.


3 OBJETIVOS 

Visa desenvolver um sistema Web para auxiliar a liderança gestora da Igreja Casa da Benção Ceará (com sede em Cascavel), com ênfase no cadastramento e controle de membros das igrejas que compõem seu campo de atuação estadual. No intuito de gerar mais organização, levantamento de dados necessários para planejamento estratégico de eventos e gastos, elaboração de planos de crescimento/melhoria, métricas.  O ICB MEMBERSHIP deve gerar link de cadastro de membro para que o mesmo o faça no conforto de sua casa.

4 PRINCIPAIS REQUISITOS FUNCIONAIS E NÃO FUNCIONAIS DAS PRINCIPAIS ENTREGAS/PRODUTOS

O Sistema deve ter:

REQUISITOS FUNCIONAIS
    • TELA 1 (Tela inicial) - Tela Inicial deve conter os botões “CADASTRO MEMBRO” e “LOGIN LÍDER”, uma vez concluído o cadastro do membro, aparecerá na tela a mensagem “Membro Cadastrado com Sucesso”. No botão “LOGIN LÍDER” ao acessar o mesmo terá acesso as ABAS (FICHAS DE CADASTRO, PROGRAMAÇÃO ICB (seria uma agenda interna ou uma integração com agenda do google) para organização de eventos do usuário de cada Igreja. OBS¹: Caso o membro logue com senha  de ADMINISTRADOR o mesmo terá acesso às FICHAS/PROGRAMAÇÃO de todas as igrejas instituições, caso seja suplente/secretário terá acesso apenas a igreja a que pertence.
        ◦ BOTÃO I (Cadastro Membro) – Esse botão servirá apenas para os membros que forem autorizados a se cadastrarem na plataforma através do link com ele compartilhado. 
*Obs¹: Não é qualquer pessoa que poderá se cadastrar no sistema, por conta que as vezes a pessoa frequenta aquela Igreja porem ainda não se identifica como membro mas sim como visitante, uma vez manifestado o desejo da pessoa de ser membro, então será compartilhado com ela o link de cadastro da plataforma.
            ▪ TELA 1.2 (Tela Cadastro Membro) -  A Tela Cadastro Membro será divida em duas seções de Campos de Preenchimento, a saber:
                • DADOS PESSOAIS - Com os campos:
                    ◦ Foto (upload/Camera);
                    ◦ Nome (obrigatório/digitado); 
                    ◦ Endereço (obrigatório/digitado); 
                    ◦ Estado Civil (obrigatório/cx opções); 
                    ◦ Contato (no formato xx 9 xxxx – xxxx, com cx de marcação lateral, caso seja Wattsapp);
                    ◦ Data Nascimento (Formato Dia/Mês/Ano); 
                    ◦ Escolaridade (cx de opções); 
                    ◦ Profissão (digitado); 
                    ◦ RG/CPF opcional; 
                    ◦ Redes Sociais (instagram/facebook) precedido do “@”.
                • DADOS ECLESIÁSTICOS - Com os campos: 
                    ◦ Data Conversão;
                    ◦ Data Batismo nas Águas (a cx com SIM/NÃO precede o campo DATA, o habilitando apenas se for marcada com SIM);
                    ◦ Igreja Anterior (as) em que Congregou Anteriormente, 
                    ◦ Igreja (congregação) Atual (cx já contendo todos os nomes de igrejas pré cadastradas);
                    ◦ Cargo/Função atual(a cx com SIM/NÃO precede o campo QUAL;

        ◦ BOTÃO II (Login Líder) - Deve conter pelo menos duas telas (Cadastro Membro / Tela de Navegação Usuário Nível I (secretário), Nível II (Admin). 
OBS¹ Caso algum dado do cadastro necessite de correção/edição, o mesmo só poderá ser feito pelo ADM local/geral do Sistema;
            ▪ TELA 2 (Área do Pastor/Líder) – Essa tela será dinâmica, ou seja, após a validação do login, a tela se apresentará diferente dependendo do usuário que logar (ver Requisitos Não-Funcionais), para o usuário ADM GERAL conterá várias abas/seções, a saber: MEMBROS/ IGREJAS/LÍDER/ CONSULTAS, dentro destas haverá:
            ▪ TELA 2.1
                • MEMBROS – Esta tela será apenas o espelho do cadastro feito pelo membro. Ainda nesta tela será possível EDITAR/EXCLUIR ou ARQUIVAR/ADICIONAR MEMBRO (TELA 1.2);
            ▪ IGREJAS - 
            ▪ TELA 2.3
                • IGREJAS-LÍDER – Esta tela só aparecerá para o usuário ADM GERAL, porque apenas ele poderá cadastrar os usuários ADM LOCAL, então para um ADM LOCAL acessar o sistema é necessário que o mesmo já tenha sido pré cadastro pelo ADM GERAL. Esta tela herdará a TELA 1.2 com a adição da seção “Perfil Líder” com os campos: 
                • Habilidades Técnicas (com campos em branco para preenchimento Livre
                • Habilidades Espirituais; 
                • Habilidades Emocionais; 
                • Hobby; 
                • Temperamento; 
                • Vivências/EXPERIÊNCIAS (espirituais) Passadas;
                • Fale mais sobre você (histórico); 
                • Livros Preferidos; 
                • Cursos (secular ou não);
            ▪ TELA 2.4 
                • CONSULTAS – Nesta área do sistema haverá uma DASHBOARD de métricas obtidas a partir dos dados levantados pelo Sistema, tais como Qnt de Membros por gênero, por faixa etária, por igreja.
OBS²: Implementar gráfico de levantamento de dados
OBS³: Propor cadastro independente de ser ou não membro.


REQUISITOS NÃO-FUNCIONAIS

    • USUÁRIOS e suas ATRIBUIÇÕES/RESTRIÇÕES - Os usuários do sistema serão:
        ◦ ADM GERAL: 
                • Acesso total à todas telas de todas as igrejas/templos;
                • Cadastra, Exclui, Edita membro;
                • Atribui direitos de ADM LOCAL para membros;
                • Cadastra templos;
        ◦ ADM LOCAL – Edita cadastros com permissão do ADM GERAL;
        ◦ MEMBRO – Apenas se auto cadastra através do link;
    • Pelo menos 2 níveis de acesso por instituição e um geral que prevaleça sobre todos, sendo para o líder principal (Pastor) e outro para usuário suplente (secretário) com suas respectivas restrições de segurança;
    • 
