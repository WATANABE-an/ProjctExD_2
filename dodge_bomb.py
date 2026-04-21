import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrect、ばくだんrect
    戻り値：横方向、縦方向判定（true：画面内 false：画面外）
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right: #横判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦判定
        tate = False
    return yoko, tate

def get_kk_imgs(base_img: pg.Surface) -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルと対応するこうかとん画像の辞書を返す関数
    """
    kk_dict = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 1.0),
        (0, -5): pg.transform.rotozoom(base_img, 90, 1.0),
        (0, +5): pg.transform.rotozoom(base_img, 270, 1.0),
        (-5, 0): pg.transform.rotozoom(base_img, 180, 1.0),
        (+5, 0): pg.transform.rotozoom(base_img, 0, 1.0),
        (-5, -5): pg.transform.rotozoom(base_img, 135, 1.0),
        (+5, -5): pg.transform.rotozoom(base_img, 45, 1.0),
        (-5, +5): pg.transform.rotozoom(base_img, 225, 1.0),
        (+5, +5): pg.transform.rotozoom(base_img, 315, 1.0),
    }
    return kk_dict

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバーを表示する関数
    引数：surface
    戻り値：なし
    """
    bk_img = pg.Surface((WIDTH, HEIGHT))
    bk_img.set_colorkey((20, 20, 20))
    bk_img.set_alpha(200)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER", True, (255, 255, 255))
    gm_img = pg.image.load("fig/8.png")
    bk_img.blit(txt, [350, 250])
    bk_img.blit(gm_img, [300, 250])
    bk_img.blit(gm_img, [700, 250])
    screen.blit(bk_img, [0, 0])
    pg.display.update()
    time.sleep(5)
    return bk_img


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    bb_img = pg.Surface((20, 20))#爆弾の生成
    pg.draw.circle(bb_img, (255, 0, 0),(10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img. get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx , vy = +5, +5

    kk_imgs = get_kk_imgs(kk_img)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        kk_img = kk_imgs.get(tuple(sum_mv), kk_img)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
