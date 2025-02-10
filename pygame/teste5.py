import pygame as pg
import random

# Configuração de cores
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
        
        # Configuração de fontes
        try:
            self.fonte = pg.font.Font("MightySouly-lxggD.ttf", 60)
            self.fonte_pequena = pg.font.Font("MightySouly-lxggD.ttf", 35)
        except:
            self.fonte = pg.font.SysFont("Arial", 60, bold=True)
            self.fonte_pequena = pg.font.SysFont("Arial", 35, bold=True)
        
        self.executando, self.pausado, self.menu_inicial = True, False, True
        
        # Carregar imagens
        self.fundo_menu = pg.transform.scale(pg.image.load("imgtelamenu.jpg"), resolucao)
        self.imagem_fundo_jogo = pg.transform.scale(pg.image.load("imgtelaprincipal.jpg"), resolucao)
        self.imagem_maca = pg.transform.scale(pg.image.load("macapygame.webp"), (30, 30))

    def limpar(self, cor='preto', fundo=None):
        self.janela.blit(fundo, (0, 0)) if fundo else self.janela.fill(CORES[cor])
    
    def atualizar(self):
        pg.display.update()
        self.clock.tick(self.limite_fps)
    
    def desenhar_texto(self, texto, pos, cor='branco', fonte=None, sombra=False):
        fonte = fonte or self.fonte
        renderizado = fonte.render(texto, True, CORES[cor])
        if sombra:
            self.janela.blit(renderizado, (pos[0] + 2, pos[1] + 2))
        self.janela.blit(renderizado, pos)
    
    def botao(self, texto, pos, tamanho, cor='branco', cor_texto='preto', arredondado=10):
        retangulo = pg.Rect(*pos, *tamanho)
        pg.draw.rect(self.janela, CORES[cor], retangulo, border_radius=arredondado)
        pg.draw.rect(self.janela, CORES['cinza_escuro'], retangulo, width=5, border_radius=arredondado)
        self.desenhar_texto(texto, (pos[0] + (tamanho[0] - self.fonte_pequena.size(texto)[0]) // 2,
                                    pos[1] + (tamanho[1] - self.fonte_pequena.size(texto)[1]) // 2), cor=cor_texto, fonte=self.fonte_pequena)
        return retangulo

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
        movimentos = {pg.K_w: (0, -1), pg.K_s: (0, 1), pg.K_a: (-1, 0), pg.K_d: (1, 0)}
        if tecla in movimentos and (movimentos[tecla][0] != -self.direcao[0] or movimentos[tecla][1] != -self.direcao[1]):
            self.direcao = movimentos[tecla]
    
    def reiniciar(self):
        self.__init__()

# Inicialização
janela = Janela()
jogo = CodeSnake()

def loop_principal():
    while janela.executando:
        janela.limpar()
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
            janela.janela.blit(janela.fundo_menu, (0, 0))
            janela.desenhar_texto("CodeSnake", (500, 100), cor='branco', fonte=janela.fonte)
            botao_iniciar = janela.botao("Iniciar", (500, 300), (200, 80), cor='amarelo', cor_texto='preto')
            if pg.mouse.get_pressed()[0] and botao_iniciar.collidepoint(pg.mouse.get_pos()):
                janela.menu_inicial = False
        
        elif janela.pausado:
            janela.desenhar_texto("Pausado - ESC para Continuar", (250, 250))
        else:
            janela.janela.blit(janela.imagem_fundo_jogo, (0, 0))
            jogo.mover()
            for segmento in jogo.cobrinha:
                pg.draw.rect(janela.janela, CORES['preto'], (segmento[0] * 24, segmento[1] * 24, 24, 24))
            janela.janela.blit(janela.imagem_maca, (jogo.maçã[0] * 24, jogo.maçã[1] * 24))
            janela.desenhar_texto(f"Pontuação: {jogo.pontuacao}", (10, 10))
        
        if jogo.fim_de_jogo:
            janela.desenhar_texto("Fim de Jogo - Pressione ENTER", (350, 250))
            if pg.key.get_pressed()[pg.K_RETURN]:
                jogo.reiniciar()
        
        janela.atualizar()
    pg.quit()

loop_principal()
