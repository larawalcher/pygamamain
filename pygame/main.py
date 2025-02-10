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
    def __init__(self, resolucao=(1180, 620), titulo='CodeSnake', fps=20):
        pg.init()
        self.janela = pg.display.set_mode(resolucao)
        pg.display.set_caption(titulo)
        self.clock = pg.time.Clock()
        self.limite_fps = fps
        self.fonte = pg.font.Font("pygamamain-main/pygame/PressStart2P-Regular.ttf", 50)
        self.fonte_pequena = pg.font.Font("pygamamain-main/pygame/PressStart2P-Regular.ttf", 30)
        self.executando, self.pausado, self.menu_inicial = True, False, True
        self.fundo_menu = pg.image.load("pygamamain-main/pygame/imgtelamenu.jpg")  # Carregar imagem de fundo
        self.fundo_menu = pg.transform.scale(self.fundo_menu, resolucao)  # Ajustar tamanho
        self.imagem_fundo_jogo = pg.image.load("pygamamain-main/pygame/imgtelaprincipal.jpg")  # Carregar imagem de fundo para o jogo
        self.imagem_fundo_jogo = pg.transform.scale(self.imagem_fundo_jogo, resolucao)  # Ajustar tamanho
        self.imagem_maca = pg.image.load("pygamamain-main/pygame/macapygame.webp")  # Carregar imagem da maçã
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

    def botao(self, texto, pos, tamanho, cor='branco', cor_texto='preto', arredondado=10):
        retangulo = pg.Rect(*pos, *tamanho)
        pg.draw.rect(self.janela, CORES[cor], retangulo, border_radius=arredondado)
        pg.draw.rect(self.janela, CORES['cinza_escuro'], retangulo, width=5, border_radius=arredondado)  # Borda mais destacada
        self.desenhar_texto(texto, (pos[0] + (tamanho[0] - self.fonte_pequena.size(texto)[0]) // 2, 
                                   pos[1] + (tamanho[1] - self.fonte_pequena.size(texto)[1]) // 2), 
                            cor=cor_texto, fonte=self.fonte_pequena)
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
            self.maçã = self.gerar_posicao_maca()  # Gerar nova posição para a maçã
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
            janela.desenhar_texto("CodeSnake", (janela.janela.get_width() // 2 - 200, 100), cor='branco', fonte=janela.fonte)
            botao_iniciar = janela.botao("Iniciar", (500, 300), (200, 80), cor='amarelo', cor_texto='preto')
            if pg.mouse.get_pressed()[0] and botao_iniciar.collidepoint(pg.mouse.get_pos()):
        
        elif janela.pausado:
            janela.desenhar_texto("Pausado - Pressione ESC para Continuar", (350, 300))
        else:
            janela.janela.blit(janela.imagem_fundo_jogo, (0, 0))  # Adicionando o fundo do jogo
            jogo.mover()
            for segmento in jogo.cobrinha:
                pg.draw.rect(janela.janela, CORES['verde'], (segmento[0] * 24, segmento[1] * 24, 24, 24))
            janela.janela.blit(janela.imagem_maca, (jogo.maçã[0] * 24, jogo.maçã[1] * 24))
            janela.desenhar_texto(f"Pontuação: {jogo.pontuacao}", (10, 10))
        
        if jogo.fim_de_jogo:
            janela.limpar('cinza')
            janela.janela.blit(janela.fundo_menu, (0, 0))  # Usando o fundo do menu para o fim de jogo
            janela.desenhar_texto("Fim de Jogo", (janela.janela.get_width() // 2 - 150, 250), cor='vermelho', fonte=janela.fonte)
            janela.desenhar_texto("Pressione ENTER para Reiniciar", (janela.janela.get_width() // 2 - 250, 350), cor='branco', fonte=janela.fonte_pequena)
            teclas = pg.key.get_pressed()
            if teclas[pg.K_RETURN]:
                jogo.reiniciar()
        
        janela.atualizar()
    pg.quit()

loop_principal()
