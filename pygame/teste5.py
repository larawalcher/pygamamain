import pygame as pg
import random

# Configurações do jogo
CORES = {
    'branco': (255, 255, 255), 'preto': (0, 0, 0), 'vermelho': (255, 0, 0), 'verde': (0, 255, 0), 
    'azul': (0, 0, 255), 'amarelo': (255, 255, 0), 'cinza': (169, 169, 169)
}

class Janela:
    def __init__(self, resolucao=(1180, 720), titulo='CodeSnake', fps=30):
        pg.init()
        self.janela = pg.display.set_mode(resolucao)
        pg.display.set_caption(titulo)
        self.clock = pg.time.Clock()
        self.limite_fps = fps
        self.fonte = pg.font.SysFont("Courier New", 50, bold=True)
        self.fonte_pequena = pg.font.SysFont("Courier New", 30, bold=True)
        self.executando, self.pausado, self.menu_inicial = True, False, True
        try:
            self.fundo_menu = pg.transform.scale(pg.image.load("imgtelamenu.jpg"), resolucao)
            self.fundo_fim = pg.transform.scale(pg.image.load("imgtelafim.jpg"), resolucao)
            self.imagem_maca = pg.transform.scale(pg.image.load("macapygame.webp"), (30, 30))
        except pg.error:
            print("Erro ao carregar imagens. Verifique os arquivos de imagem.")
            self.executando = False

    def atualizar(self):
        pg.display.update()
        self.clock.tick(self.limite_fps)

    def limpar(self, cor='preto'):
        self.janela.fill(CORES[cor])
    
    def desenhar_texto(self, texto, pos, cor='branco', fonte=None):
        fonte = fonte or self.fonte
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
        movimentos = {pg.K_w: (0, -1), pg.K_s: (0, 1), pg.K_a: (-1, 0), pg.K_d: (1, 0)}
        if tecla in movimentos and (movimentos[tecla][0] != -self.direcao[0] or movimentos[tecla][1] != -self.direcao[1]):
            self.direcao = movimentos[tecla]
    
    def reiniciar(self):
        self.__init__()

# Inicialização
janela = Janela()
if not janela.executando:
    pg.quit()
else:
    jogo = CodeSnake()

def loop_principal():
    while janela.executando:
        janela.limpar()
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                janela.executando = False
        janela.atualizar()
    pg.quit()

loop_principal()
