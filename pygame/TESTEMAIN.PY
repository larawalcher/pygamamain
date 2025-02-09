import pygame as pg
import random
import time

# Configurações do jogo
CORES = {
    'branco': (255, 255, 255), 'preto': (0, 0, 0), 'vermelho': (255, 0, 0), 'verde': (0, 255, 0), 
    'azul': (0, 0, 255), 'amarelo': (255, 255, 0), 'cinza': (169, 169, 169)
}

class Janela:
    def __init__(self, resolucao=(1180, 620), titulo='CodeSnake', fps=25):
        pg.init()
        self.janela = pg.display.set_mode(resolucao)
        pg.display.set_caption(titulo)
        self.clock = pg.time.Clock()
        self.limite_fps = fps
        self.fonte = pg.font.SysFont("Courier New", 50, bold=True)
        self.fonte_pequena = pg.font.SysFont("Courier New", 30, bold=True)
        self.executando, self.pausado, self.menu_inicial = True, False, True

        # Tratamento de erro ao carregar imagens
        try:
            self.fundo_menu = pg.image.load("imgtelamenu.jpg")  # Carregar imagem de fundo para o menu
            self.fundo_menu = pg.transform.scale(self.fundo_menu, resolucao)  # Ajustar tamanho
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo do menu: {e}")
            self.fundo_menu = None  # Defina um fundo de fallback

        try:
            self.fundo_jogo = pg.image.load("imgtelaprincipal.jpg")  # Carregar imagem de fundo para o jogo
            self.fundo_jogo = pg.transform.scale(self.fundo_jogo, resolucao)  # Ajustar tamanho
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo do jogo: {e}")
            self.fundo_jogo = None  # Defina um fundo de fallback

        try:
            self.imagem_maca = pg.image.load("macapygame.webp")  # Carregar imagem da maçã
            self.imagem_maca = pg.transform.scale(self.imagem_maca, (30, 30))  # Ajustar tamanho da maçã
        except Exception as e:
            print(f"Erro ao carregar imagem da maçã: {e}")
            self.imagem_maca = None  # Defina um fundo de fallback
        
    
    def atualizar(self):
        pg.display.update()
        self.clock.tick(self.limite_fps)

    def limpar(self, fundo=None):
        if fundo:
            self.janela.blit(fundo, (0, 0))  # Desenhar o fundo
        else:
            self.janela.fill(CORES['preto'])  # Caso não tenha fundo, preencher com a cor preta
    
    def desenhar_texto(self, texto, pos, cor='branco', fonte=None):
        if fonte is None:
            fonte = self.fonte
        renderizado = fonte.render(texto, True, CORES[cor])
        self.janela.blit(renderizado, pos)

    def botao(self, texto, pos, tamanho, cor='branco', cor_texto='preto', arredondado=10):
        retangulo = pg.Rect(*pos, *tamanho)
        pg.draw.rect(self.janela, CORES[cor], retangulo, border_radius=arredondado)
        self.desenhar_texto(texto, (pos[0] + (tamanho[0] - self.fonte_pequena.size(texto)[0]) // 2, 
                                   pos[1] + (tamanho[1] - self.fonte_pequena.size(texto)[1]) // 2), 
                            cor=cor_texto, fonte=self.fonte_pequena)
        return retangulo

class CodeSnake:
    def __init__(self):
        self.tamanho_grelha = (53, 30)
        self.cobrinha = [(10, 10), (9, 10), (8, 10)]
        self.direcao = (1, 0)
        self.maçã = (random.randint(0, 52), random.randint(0, 29))
        self.pontuacao, self.fim_de_jogo = 0, False
    
    def mover(self):
        if self.fim_de_jogo:
            return
        nova_cabeca = (self.cobrinha[0][0] + self.direcao[0], self.cobrinha[0][1] + self.direcao[1])
        self.cobrinha.insert(0, nova_cabeca)
        if nova_cabeca == self.maçã:
            self.maçã = (random.randint(0, 52), random.randint(0, 29))
            self.pontuacao += 1
        else:
            self.cobrinha.pop()
        self.verificar_colisao()
    
    def verificar_colisao(self):
        cabeca = self.cobrinha[0]
        if cabeca in self.cobrinha[1:] or not (0 <= cabeca[0] < 53 and 0 <= cabeca[1] < 30):
            self.fim_de_jogo = True
    
    def mudar_direcao(self, tecla):
        movimentos = {
            pg.K_w: (0, -1), pg.K_s: (0, 1), 
            pg.K_a: (-1, 0), pg.K_d: (1, 0)
        }
        if tecla in movimentos and (movimentos[tecla][0] != -self.direcao[0] or movimentos[tecla][1] != -self.direcao[1]):
            self.direcao = movimentos[tecla]
    
    def reiniciar(self):
        self.__init__()

# Inicialização
janela = Janela()
jogo = CodeSnake()

def loop_principal():
    while janela.executando:
        if janela.menu_inicial:
            janela.limpar(fundo=janela.fundo_menu)  # Usar o fundo do menu
        else:
            janela.limpar(fundo=janela.fundo_jogo)  # Usar o fundo do jogo

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                janela.executando = False
            if evento.type == pg.KEYDOWN:
                if janela.menu_inicial and evento.key == pg.K_RETURN:
                    janela.menu_inicial = False
                elif not janela.menu_inicial:
                    if evento.key == pg.K_ESCAPE:
                        janela.pausado = not janela.pausado
                    elif not janela.pausado:
                        jogo.mudar_direcao(evento.key)
        
        if janela.menu_inicial:
            janela.desenhar_texto("CodeSnake", (janela.janela.get_width() // 2 - 200, 100), cor='branco', fonte=janela.fonte)
            botao_iniciar = janela.botao("Iniciar", (500, 300), (200, 80), cor='amarelo', cor_texto='preto')
            if pg.mouse.get_pressed()[0] and botao_iniciar.collidepoint(pg.mouse.get_pos()):
                janela.menu_inicial = False
        
        elif janela.pausado:
            janela.desenhar_texto("Pausado - Pressione ESC para Continuar", (350, 300))
        else:
            jogo.mover()
            for segmento in jogo.cobrinha:
                pg.draw.rect(janela.janela, CORES['verde'], (segmento[0] * 24, segmento[1] * 24, 24, 24))
            janela.janela.blit(janela.imagem_maca, (jogo.maçã[0] * 24, jogo.maçã[1] * 24))
            janela.desenhar_texto(f"Pontuação: {jogo.pontuacao}", (10, 10))
        
        if jogo.fim_de_jogo:
            janela.limpar('cinza')
            janela.desenhar_texto("Fim de Jogo", (janela.janela.get_width() // 2 - 150, 250), cor='vermelho', fonte=janela.fonte)
            janela.desenhar_texto("Pressione ENTER para Reiniciar", (janela.janela.get_width() // 2 - 250, 350), cor='branco', fonte=janela.fonte_pequena)
            teclas = pg.key.get_pressed()
            if teclas[pg.K_RETURN]:
                jogo.reiniciar()
        
        janela.atualizar()
    pg.quit()

loop_principal()
