import pygame as pg
import random
import time

# Configurações do jogo
CORES = {
    'branco': (255, 255, 255), 'preto': (0, 0, 0), 'vermelho': (255, 0, 0), 'verde': (0, 255, 0), 
    'azul': (0, 0, 255), 'amarelo': (255, 255, 0), 'cinza': (169, 169, 169), 'cinza_escuro': (40, 40, 40),
    'azul_claro': (60, 100, 255), 'laranja': (255, 165, 0)
}

class Janela:
    def __init__(self, resolucao=(1180, 620), titulo='CodeSnake', fps=25):
        pg.init()
        self.janela = pg.display.set_mode(resolucao)
        pg.display.set_caption(titulo)
        self.clock = pg.time.Clock()
        self.limite_fps = fps
        try:
            self.fonte = pg.font.Font("MightySouly-lxggD.ttf", 60)
            self.fonte_pequena = pg.font.Font("MightySouly-lxggD.ttf", 35)
        except:
            self.fonte = pg.font.SysFont("Arial", 60, bold=True)
            self.fonte_pequena = pg.font.SysFont("Arial", 35, bold=True)
        self.executando, self.pausado, self.menu_inicial = True, False, True
        self.fundo_menu = pg.image.load("imgtelamenu.jpg")  # Carregar imagem de fundo
        self.fundo_menu = pg.transform.scale(self.fundo_menu, resolucao)  # Ajustar tamanho
        self.imagem_fundo_jogo = pg.image.load("imgtelaprincipal.jpg")  # Carregar imagem de fundo para o jogo
        self.imagem_fundo_jogo = pg.transform.scale(self.imagem_fundo_jogo, resolucao)  # Ajustar tamanho
        self.imagem_maca = pg.image.load("macapygame.webp")  # Carregar imagem da maçã
        self.imagem_maca = pg.transform.scale(self.imagem_maca, (30, 30))  # Ajustar tamanho da maçã

    def limpar(self, cor='preto', fundo=None):
        if fundo:
            self.janela.blit(fundo, (0, 0))  # Desenhar o fundo
        else:
            self.janela.fill(CORES[cor])

    def atualizar(self):
        pg.display.update()
        self.clock.tick(self.limite_fps)

    def desenhar_texto(self, texto, pos, cor='branco', fonte=None, sombra=False):
        if fonte is None:
            fonte = self.fonte
        renderizado = fonte.render(texto, True, CORES[cor])
        if sombra:
            self.janela.blit(renderizado, (pos[0] + 2, pos[1] + 2))  # Sombra do texto
        self.janela.blit(renderizado, pos)

class CodeSnake:
    def __init__(self):
        self.tamanho_grelha = (53, 30)
        self.cobrinha = [(10, 10), (9, 10), (8, 10)]
        self.direcao = (1, 0)
        self.maçã = self.gerar_posicao_maca()
        self.pontuacao, self.fim_de_jogo = 0, False
    
    def gerar_posicao_maca(self):
        return (random.randint(0, 45), random.randint(0, 25))
    
    def mover(self):
        if self.fim_de_jogo:
            return
        nova_cabeca = (self.cobrinha[0][0] + self.direcao[0], self.cobrinha[0][1] + self.direcao[1])
        self.cobrinha.insert(0, nova_cabeca)
        if nova_cabeca == self.maçã:
            self.maçã = self.gerar_posicao_maca()
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
    
    def desenhar(self, janela):
        for i, segmento in enumerate(self.cobrinha):
            cor = CORES['vermelho'] if i == 0 else CORES['azul_claro']
            pg.draw.circle(janela, cor, (segmento[0] * 24 + 12, segmento[1] * 24 + 12), 12)
            pg.draw.circle(janela, CORES['preto'], (segmento[0] * 24 + 12, segmento[1] * 24 + 12), 12, 2)

janela = Janela()
jogo = CodeSnake()

def loop_principal():
    while janela.executando:
        janela.limpar(fundo=janela.imagem_fundo_jogo)
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                janela.executando = False
            if evento.type == pg.KEYDOWN:
                jogo.mudar_direcao(evento.key)
        
        jogo.mover()
        jogo.desenhar(janela.janela)
        janela.janela.blit(janela.imagem_maca, (jogo.maçã[0] * 24, jogo.maçã[1] * 24))
        janela.desenhar_texto(f"Pontuação: {jogo.pontuacao}", (10, 10))
        janela.atualizar()
    pg.quit()

loop_principal()
