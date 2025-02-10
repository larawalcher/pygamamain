import pygame as pg
import random
import time

# Configurações de cores
CORES = {
    'branco': (255, 255, 255), 'preto': (0, 0, 0), 'vermelho': (255, 0, 0), 'verde': (0, 255, 0), 
    'azul': (0, 0, 255), 'amarelo': (255, 255, 0), 'cinza': (169, 169, 169), 'cinza_escuro': (40, 40, 40),
    'azul_claro': (60, 100, 255), 'laranja': (255, 165, 0)
}

# Classe que gerencia a janela do jogo e a interface gráfica
class Janela:
    def __init__(self, resolucao=(1180, 620), titulo='CodeSnake', fps=25):
        pg.init()  # Inicializa o Pygame
        self.janela = pg.display.set_mode(resolucao)  # Define o tamanho da janela
        pg.display.set_caption(titulo)  
        self.clock = pg.time.Clock()  
        self.limite_fps = fps  # Define o limite de FPS do jogo
        try:
            # fonte
            self.fonte = pg.font.Font("MightySouly-lxggD.ttf", 60)
            self.fonte_pequena = pg.font.Font("MightySouly-lxggD.ttf", 35)
        except:
            # Se falhar, utiliza uma fonte padrão do sistema
            self.fonte = pg.font.SysFont("Arial", 60, bold=True)
            self.fonte_pequena = pg.font.SysFont("Arial", 35, bold=True)
        
        self.executando, self.pausado, self.menu_inicial = True, False, True  # Inicializa variáveis do jogo
        # Carrega as imagens de fundo do jogo
        self.fundo_menu = pg.image.load("imgtelamenu.jpg")  
        self.fundo_menu = pg.transform.scale(self.fundo_menu, resolucao)
        self.imagem_fundo_jogo = pg.image.load("imgtelaprincipal.jpg")
        self.imagem_fundo_jogo = pg.transform.scale(self.imagem_fundo_jogo, resolucao)
        self.imagem_maca = pg.image.load("macapygame.webp")  # Imagem da maçã
        self.imagem_maca = pg.transform.scale(self.imagem_maca, (30, 30))  # Ajusta o tamanho da maçã

    # Método para limpar a tela
    def limpar(self, cor='preto', fundo=None):
        if fundo:
            self.janela.blit(fundo, (0, 0))
        else:
            self.janela.fill(CORES[cor])

    # Método para atualizar a tela e controlar os FPS
    def atualizar(self):
        pg.display.update()  # Atualiza a tela
        self.clock.tick(self.limite_fps)  # Controla os FPS

    
    def desenhar_texto(self, texto, pos, cor='branco', fonte=None, sombra=False):
        if fonte is None:
            fonte = self.fonte  # Usa a fonte padrão se não for especificada
        renderizado = fonte.render(texto, True, CORES[cor])  # Renderiza o texto com a cor especificada
        if sombra:
            # efeito de sombra
            self.janela.blit(renderizado, (pos[0] + 2, pos[1] + 2))
        self.janela.blit(renderizado, pos)

    # botão na tela
    def botao(self, texto, pos, tamanho, cor='branco', cor_texto='preto', arredondado=10):
        retangulo = pg.Rect(*pos, *tamanho)  # Cria um retângulo para o botão
        pg.draw.rect(self.janela, CORES[cor], retangulo, border_radius=arredondado)  # Desenha o botão
        pg.draw.rect(self.janela, CORES['cinza_escuro'], retangulo, width=5, border_radius=arredondado)  # Borda mais destacada
        # Centraliza o texto dentro do botão e desenha
        self.desenhar_texto(texto, (pos[0] + (tamanho[0] - self.fonte_pequena.size(texto)[0]) // 2, 
                                   pos[1] + (tamanho[1] - self.fonte_pequena.size(texto)[1]) // 2), 
                            cor=cor_texto, fonte=self.fonte_pequena)
        return retangulo  # Retorna o retângulo do botão

    # Método para desenhar a cobrinha na tela
    def desenhar(self, janela):
        for i, segmento in enumerate(self.cobrinha):
            cor = CORES['verde'] if i == 0 else CORES['azul_claro']  # A cabeça da cobrinha é verde, o resto é azul claro
            pg.draw.circle(janela, cor, (segmento[0] * 24 + 12, segmento[1] * 24 + 12), 12)  # Desenha o segmento
            pg.draw.circle(janela, CORES['preto'], (segmento[0] * 24 + 12, segmento[1] * 24 + 12), 12, 2)  # Desenha contorno

# Classe principal que controla a lógica do jogo (Cobrinha, movimento, colisões)
class CodeSnake:
    def __init__(self):
        self.tamanho_grelha = (53, 30)  # Tamanho da grade do jogo
        self.cobrinha = [(10, 10), (9, 10), (8, 10)]  # Posição inicial da cobrinha
        self.direcao = (1, 0)  # Direção inicial da cobrinha (direita)
        self.maçã = self.gerar_posicao_maca()  # Gera a primeira maçã
        self.pontuacao, self.fim_de_jogo = 0, False  # Inicializa a pontuação e o status do jogo
    
    # Método para gerar uma posição aleatória para a maçã
    def gerar_posicao_maca(self):
        return (random.randint(0, 45), random.randint(0, 25))
    
    # Método para mover a cobrinha
    def mover(self):
        if self.fim_de_jogo:
            return  # Se o jogo terminou, não move a cobrinha
        nova_cabeca = (self.cobrinha[0][0] + self.direcao[0], self.cobrinha[0][1] + self.direcao[1])  # Calcula a nova posição da cabeça
        self.cobrinha.insert(0, nova_cabeca)  # Adiciona a nova cabeça na frente da cobrinha
        if nova_cabeca == self.maçã:  # Se a cobrinha comer a maçã
            self.maçã = self.gerar_posicao_maca()  # Gera uma nova maçã
            self.pontuacao += 1  # Incrementa a pontuação
        else:
            self.cobrinha.pop()  # Remove o último segmento (cobrinha não cresceu)
        self.verificar_colisao()  # Verifica colisões

    # Método para verificar colisões (com a parede ou com a própria cobrinha)
    def verificar_colisao(self):
        cabeca = self.cobrinha[0]
        if cabeca in self.cobrinha[1:] or not (0 <= cabeca[0] < 53 and 0 <= cabeca[1] < 30):
            self.fim_de_jogo = True  # Se colidir, o jogo termina
    
    # Método para mudar a direção da cobrinha
    def mudar_direcao(self, tecla):
        movimentos = {
            pg.K_w: (0, -1), pg.K_s: (0, 1), 
            pg.K_a: (-1, 0), pg.K_d: (1, 0)
        }
        # Impede a reversão instantânea da direção
        if tecla in movimentos and (movimentos[tecla][0] != -self.direcao[0] or movimentos[tecla][1] != -self.direcao[1]):
            self.direcao = movimentos[tecla]
    
    # Método para reiniciar o jogo
    def reiniciar(self):
        self.__init__()  # Recria a instância da classe, resetando o jogo

# Inicialização do jogo
janela = Janela()  # Cria a janela do jogo
jogo = CodeSnake()  # Cria o objeto do jogo

# Função principal do loop do jogo
def loop_principal():
    while janela.executando:
        janela.limpar()  # Limpa a tela a cada iteração
        for evento in pg.event.get():  # Verifica eventos (teclado, fechar a janela, etc)
            if evento.type == pg.QUIT:
                janela.executando = False  # Fecha o jogo
            if evento.type == pg.KEYDOWN:
                if janela.menu_inicial and evento.key == pg.K_RETURN:
                    janela.menu_inicial = False  # Inicia o jogo ao pressionar Enter
                elif not janela.menu_inicial:
                    if evento.key == pg.K_ESCAPE:
                        janela.pausado = not janela.pausado  # Pausa e retoma o jogo ao pressionar ESC
                    elif not janela.pausado:
                        jogo.mudar_direcao(evento.key)  # Muda a direção da cobrinha

        # Menu Inicial
        if janela.menu_inicial:
            janela.janela.blit(janela.fundo_menu, (0, 0))  # Desenha o fundo do menu
            janela.desenhar_texto("CodeSnake", (janela.janela.get_width() // 2 - janela.fonte.size("CodeSnake")[0] // 2, 100), cor='branco', fonte=janela.fonte)
            botao_iniciar = janela.botao("Iniciar", (500, 300), (200, 80), cor='amarelo', cor_texto='preto')
            if pg.mouse.get_pressed()[0] and botao_iniciar.collidepoint(pg.mouse.get_pos()):
                janela.menu_inicial = False  # Inicia o jogo quando o botão for pressionado
        
        # Jogo Pausado
        elif janela.pausado:
            janela.desenhar_texto("Pausado - ESC para Continuar", (250, 250))

        # Durante o Jogo
        else:
            janela.janela.blit(janela.imagem_fundo_jogo, (0, 0))  # Desenha o fundo do jogo
            jogo.mover()  # Atualiza a posição da cobrinha
            for segmento in jogo.cobrinha:
                pg.draw.rect(janela.janela, CORES['preto'], (segmento[0] * 24, segmento[1] * 24, 24, 24))  # Desenha cada segmento da cobrinha
            janela.janela.blit(janela.imagem_maca, (jogo.maçã[0] * 24, jogo.maçã[1] * 24))  # Desenha a maçã
            janela.desenhar_texto(f"Pontuação: {jogo.pontuacao}", (10, 10))  # Exibe a pontuação

        # Fim de Jogo
        if jogo.fim_de_jogo:
            janela.limpar('cinza')  # Limpa a tela e coloca um fundo cinza
            janela.janela.blit(janela.fundo_menu, (0, 0))  # Exibe o fundo do menu
            janela.desenhar_texto("Fim de Jogo", (janela.janela.get_width() // 2 - 150, 250), cor='vermelho', fonte=janela.fonte)
            janela.desenhar_texto("Pressione ENTER para Reiniciar", (janela.janela.get_width() // 2 - 250, 350), cor='preto', fonte=janela.fonte_pequena)
            teclas = pg.key.get_pressed()
            if teclas[pg.K_RETURN]:
                jogo.reiniciar()  # Reinicia o jogo quando pressionado Enter
        
        janela.atualizar()  # Atualiza a tela
    pg.quit()  # Fecha o Pygame quando o jogo for encerrado

loop_principal()  # Inicia o loop principal do jogo
