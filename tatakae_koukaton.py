import os
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800   #ディスプレイの大きさ
battle = 1 #バトルモードの時、攻撃があった場合
mode_a = ""
mode_aa = 0

def load_sound(file):
    """
    音源を読み込む関数
    引数1 file：音源ファイル
    """
    if not pg.mixer:
        return None
    
    try:
        sound = pg.mixer.Sound(file) #Soundオブジェクト作成
        return sound
    except pg.error:
        print(f"Warning, unable to load,{file}")
    
    return None


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    Rectの画面内外判定用の関数
    引数：プレイヤーRect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:   # 横方向のはみ出し判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def check_bound2(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    Rectの画面内外判定用の関数
    引数：プレイヤーRect
    戻り値：左方向判定結果，右方向判定結果，上方向判定結果，下方向判定結果（True：画面内／False：画面外）
    """
    ue, hidari, sita, migi = True, True, True, True
    if obj_rct.left < 0:        # 左方向のはみ出し判定
        hidari = False
    if WIDTH < obj_rct.right:   # 右方向のはみ出し判定
        migi = False
    if obj_rct.top < 0:         # 上方向のはみ出し判定
        ue = False
    if HEIGHT < obj_rct.bottom: # 下方向のはみ出し判定
        sita = False
    return ue, hidari, sita, migi

class Synopsis:
    """
    あらすじ画面に関するクラス
    """

    #あらすじリスト
    syp_lst = [
        "20××年、東京工科大学のマスコットキャラの,こうかとんが何らかの力によって邪悪な存在へと,変貌してしまった。", 
        "邪悪な存在となったこうかとんは学生の単位と学部長賞を奪っていった。", 
        "そこで立ち上がったのは、プロジェクト演習Dチーム3であった。", 
        "こうかとんの手下とこうかとんを倒すため、いざ出陣！"
    ]

    def __init__(self):
        """
        あらすじに必要な、背景写真・メッセージボックス・あらすじ文を生成する
        """
        self.image = pg.image.load("fig/kouka.jpg")  #タイトルと同じ画像
        self.rect = self.image.get_rect()

        self.image2 = pg.Surface((WIDTH, HEIGHT)) #透明な四角
        pg.draw.rect(self.image2, (0,0,0), (0,0,WIDTH, HEIGHT))
        self.rect2 = self.image2.get_rect()
        self.image2.set_alpha(128)

        self.image3 = pg.Surface((WIDTH-200, HEIGHT-600)) #メッセージボックス
        pg.draw.rect(self.image3, (0,0,0), (0,0,WIDTH, HEIGHT))
        self.rect3 = self.image3.get_rect()
        self.rect3.center = WIDTH/2, HEIGHT-(HEIGHT/6)

        self.font = pg.font.SysFont("hg正楷書体pro",40)
        self.index = 0  #表示文字のインデックス
        # self.num = 1  #フェードアウト確認用

    
    def key_event(self, event):
        """
        エンターキーが押されたかを判定
        モードの切り替え
        """
        global mode_a
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.index += 1
            self.image3.fill((0,0,0)) #リセット
            if self.index >= len(__class__.syp_lst):
                self.index = 0
                self.num = 0
                mode_a = "マップ"   #変更
                mode_aa = 1
                print("a")
        return True
    

    def update(self, screen:pg.Surface):
        """
        あらすじ文字の表示
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.image2, self.rect2)
        screen.blit(self.image3, self.rect3)

        y_off = 10
        high = 40

        if self.index < len(__class__.syp_lst):
            text = __class__.syp_lst[self.index]
            for i in range(0, len(text), 25):
                line = text[i:i+25]
                self.txt = self.font.render(line, True, (255,255,255,))
                self.image3.blit(self.txt, [10, y_off])
                y_off += high


class Map:
    """
    Mapの描画に関するクラス。
    """
    map_scene_xy = [(-240, -280), (-240, -200), (-240, -120), (-240, -50), (-150, -50), (-180, -20), (-40, -20), (-50, -140), (-160, -180), (-160, -250), (-320, -60), (-380, -70)]
    map_scnen_name = ["片桐研究所", "坂道", "坂の上", "研究所A&B", "講義棟A&講義実験棟", "マック", "体育館", "運動場", "FOOS FOO", "FOOS FOO 2", "講義棟C", "メディアホール"]
    img_zoom = 10.0
    def __init__(self) -> None:
        self.image = pg.image.load(f"fig/tut_map.jpg")
        self.img = pg.transform.rotozoom(self.image, 0, __class__.img_zoom)
        self.scene_num = 0
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)

    def update(self, screen, score):
        screen.blit(self.img, [__class__.map_scene_xy[self.scene_num][0]*__class__.img_zoom, 
                               __class__.map_scene_xy[self.scene_num][1]*__class__.img_zoom])
        
        # 今いる場所の表示(左上)
        self.txt = self.font.render(__class__.map_scnen_name[self.scene_num], True, (0, 0, 0))
        self.txt_rect = self.txt.get_rect()
        self.txt_rect.center = 250, 80
        screen.blit(self.txt, self.txt_rect)

        # スコアの表示(左上)
        self.txt3 = self.font.render(f"単位数：{score}", 0, (255, 0, 0))
        self.txt_rect = self.txt3.get_rect()
        self.txt_rect.center = 1100, 80
        screen.blit(self.txt3, self.txt_rect)
        

class Novel:
    """
    map下部に語り文を表示させるクラス。
    """
    nl = ["せいな：", "こうた：", "さゆか：", "まの：", "ほのか："] # プレイヤーの名前の表示
    # 表示させる語り文
    novel_lst = [[[f"{nl[0]}着いた！！片桐研究所だ！", f"{nl[4]}うえーーーーん", ""], 
                  [f"{nl[2]}今回の私達の目的は単位を拾って", "こうかとんを倒すことよ！！", ""], 
                  [f"{nl[3]}じゃあここらへんで単位をさがすか～！", "", ""]],
                 [[f"{nl[2]}ここは庭だね、、、", "", ""], 
                  [f"{nl[0]}特になにもなさそうだね、、、", "", ""], 
                  [f"{nl[1]}でも、横にはFOOS FOOがあるよ！！", "", ""]],
                 [[f"{nl[0]}坂の上は人が多いね、、、", "", ""], 
                  [f"{nl[2]}あそこみて！！！何かいるよ！！！", "いってみようよ！", ""], 
                  [f"{nl[1]}行きたくないんだけどな、、、", "", ""]],
                 [[f"{nl[2]}ここはCSで有名な研究所だね？", "ちょっとこわい、、", ""], 
                  [f"{nl[0]}なかにはいってみようか！！！", "、、、いや入り口になんかいない？？？", ""], 
                  [f"{nl[3]}多分気のせい！！！はなしかけて", "みよう！！", ""]],
                 [[f"{nl[0]}英語のにおいがするな", "", ""], 
                  [f"{nl[3]}うわ、講義室の場所に来ただけでにおう", "とか、、、英語狂人じゃん", ""], 
                  [f"{nl[0]}黙れ", "", ""], [f"{nl[2]}ところで、ここには何もなくない？？？", "", ""]],
                 [[f"{nl[3]}うわあああ不健康だぁぁぁぁぁ", "", ""], 
                  [f"{nl[4]}うええええええん", "", ""], 
                  [f"{nl[2]}そんなことより単位を探さないと！！！", "", ""]],
                 [[f"{nl[3]}健康だね！！！運動ができるよみんな", "私はしないけど、、、", ""], 
                  [f"{nl[2]}ほら、あそこに運動しがいがあるもの", "がいるよ！！", ""], 
                  [f"{nl[1]}どうせまた単位と戦わなきゃいけな", "いんでしょ", ""]],
                 [[f"{nl[2]}運動場だ！！広いね！！！", "", ""], 
                  [f"{nl[1]}ほんとに！！！！砂漠の中からアリを", "さがすくらい難しいね", ""], 
                  [f"{nl[0]}何言ってんの？", "", ""], [f"{nl[2]}喧嘩しないで", "", ""]],
                 [[f"{nl[0]}ふーず・ふーだ！！！", "", ""], 
                  ["工科大の広告をしておこう。東京工科大学で", "は校内に吉野家、\
                   マック、セブンなど沢山のご", "はん屋さんがある。大学行くなら工科大！！"], 
                  [f"{nl[1]}これで工科大の宣伝に効果大だね！！", "", ""], 
                  [f"{nl[3]}hhh", "", ""]],
                 [[f"{nl[0]}画面が少しも動いてないじゃん！！", "", ""], 
                  [f"{nl[2]}こうゆうときこそなにか大事なものが", "", ""], 
                  [f"{nl[4]}うええええええん", "", ""]],
                 [[f"{nl[3]}講義棟Cにきたよ！！！陰キャCSには", "無縁の場所だね！", ""], 
                  [f"{nl[0]}何言ってんの！！しーー！", "", ""], 
                  [f"{nl[1]}Cだけに？", "", ""], 
                  [f"{nl[4]}うわーーーーん", "", ""]],
                 [[f"{nl[0]}メディアホールだ！！！", "", "※コード書いてる中の人はここらへんで疲れた"], 
                  [f"{nl[1]}なにいいいいいい！！", "", ""], 
                  [f"{nl[3]}なにかいるんじゃないのおおおお", "", ""]]]
    def __init__(self) -> None:
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
        self.novel_num = 0

        # 表示させる文章のサーフェイスとレクトの初期状態の定義
        self.image = pg.Surface((WIDTH-200, HEIGHT-600))
        pg.draw.rect(self.image, (0,0,0), (0,0,WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT-(HEIGHT/6)
        self.alpha_num = 255
        
    def update(self, screen, map: Map): 
        self.image.set_alpha(self.alpha_num)
        screen.blit(self.image, self.rect)
        
        # 表示させる文章のサーフェイスと文章の定義
        self.image = pg.Surface((WIDTH-200, HEIGHT-600))
        pg.draw.rect(self.image, (0,0,0), (0,0,WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT-(HEIGHT/6)
        # 文章は三段に分けて表示させる
        self.txt0 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][0], 0, (255, 255, 255))
        self.txt1 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][1], 0, (255, 255, 255))
        self.txt2 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][2], 0, (255, 255, 255))
        self.image.blit(self.txt0, [10, 10])
        self.image.blit(self.txt1, [10, 60])
        self.image.blit(self.txt2, [10, 110])
    
    def alpha(self):
        self.alpha_num -= 5 # alpha値を減らす(徐々に透明にさせる)
        

class Map_player:
    """
    プレイヤー表示に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }
    def __init__(self, i) -> None:
        self.image2 = pg.transform.rotozoom(pg.image.load(f"fig/pl{i}_0.png"), 0, 0.4)
        self.rect2 = self.image2.get_rect()
        self.i = i  # iをのちのupdateで使うために定義
        
        # 表示位置の設定
        if i == 0 or i == 1:
            self.rect2.center = WIDTH/2+(100*i), HEIGHT/2  
        else:
            self.rect2.center = WIDTH/2+(100*(i-2))-50, HEIGHT/2+100
        self.speed = 10 #動かすスピードの設定
        
    def update(self, screen, key_lst, all_mode, scene_num, map_mode):
        screen.blit(self.image2, self.rect2)
        sum_mv = [0, 0] # プレイヤーの移動量のリスト
        
        # マップモードが入れない判定の時(2)はプレイヤーを中央に移動
        for h in range(4):
            if map_mode[scene_num][h] == 1:
                if self.i == 0 or self.i == 1:
                    self.rect2.center = WIDTH/2+(100*self.i), HEIGHT/2  
                else:
                    self.rect2.center = WIDTH/2+(100*(self.i-2))-50, HEIGHT/2+100
        
        # 押されたキーによって移動
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                
        # all_mode(まだ敵が倒されていない)時はプレイヤーを中央に移動
        self.rect2.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1]) 
        if all_mode == 1:
            if self.i == 0 or self.i == 1:
                self.rect2.center = WIDTH/2+(100*self.i), HEIGHT/2  
            else:
                self.rect2.center = WIDTH/2+(100*(self.i-2))-50, HEIGHT/2+100
                
class Map_enemy:
    map_enemy = ["fig/tanni.png", "fig/En1.png","fig/En2.png", "fig/En3.png", "fig/En4.png", "fig/En5.png", "fig/En6.png", "fig/En2.png", "fig/En8.png", "fig/tanni.png", "fig/En2.png", "fig/En11.png"]
    me_xy = [(300, 500), (WIDTH*3/4, HEIGHT/2), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500)]
    def __init__(self) -> None:
        pass
        
    def update(self, screen, i):
        if i == 100:
            pass
        else:
            # enemyを描写
            self.image = pg.image.load(__class__.map_enemy[i])
            self.rect = self.image.get_rect()
            self.rect.center = __class__.me_xy[i]
            screen.blit(self.image, self.rect)
def main():
    global mode_a, mode_aa
    mode = "オープニング"    
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    synopsis = Synopsis() #初期値
    map = Map()
    novel = Novel()
    novel_mode = 0
    mpl_lst = []
    for i in range(5):  # プレイヤーごとにクラスの生成
        mpl = Map_player(i)
        mpl_lst.append(mpl)
    all_mode = 0
    Map_Mode = "normal "    # mapモードがonであるかどうか(マージ後の初期値はnormal)
    map_enemy = Map_enemy()
    enemy_mode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    map_mode = [[0, 0, 2, 2], [0, 2, 0, 2], [0, 0, 0, 2], 
                [2, 0, 0, 0], [0, 0, 0, 0], [2, 2, 0, 2], 
                [2, 2, 0, 0], [0, 2, 2, 2], [0, 2, 0, 0], 
                [0, 2, 2, 0], [2, 0, 2, 0], [2, 0, 2, 2]]
    map_saki = [[1, 9, 0, 0], [2, 0, 0, 0], [3, 8, 1, 0], 
                [0, 4, 2, 10], [5, 6, 8, 3], [0, 0, 4, 0], 
                [0, 0, 7, 4], [6, 0, 0, 0], [4, 0, 9, 2], 
                [8, 0, 0, 0], [0, 3, 0, 11], [0, 10, 0, 0]]
    score = 0   # 単位数
    map_pl_mode = 100
    music_t = 0
    
    bg = pg.image.load(f"fig/kena-xga.jpg").convert_alpha()
    bg = pg.transform.scale(bg, (WIDTH,HEIGHT)) 
    shikaku = pg.Surface((WIDTH,HEIGHT))
    shikaku_rect = pg.draw.rect(shikaku,(255,255,255),pg.Rect(0,0,WIDTH,HEIGHT))
    shikaku.set_alpha(128)
    gamemode = "0" #ゲームモードを０に設定する
    op_bgm = load_sound("sound/op_bgm.mp3")
    syp_bgm = load_sound("sound/syp_bgm.mp3")
    map_bgm = load_sound("sound/map_bgm.mp3")
    battle_bgm = load_sound("sound/battle_bgm.mp3")
    panch = load_sound("sound/panch.mp3")
    ed_bgm = load_sound("sound/ed_bgm.mp3")
    gameover = load_sound("sound/gameover.mp3")
    
    while True:
        if mode_a == "マップ":
            mode = "マップ"
        if mode_aa == 1:
            music_t = 0
            mode_aa = 0
        if mode == "オープニング" and music_t == 0:
             op_bgm.play()
             music_t = 1
        elif mode == "あらすじ" and music_t == 0:
            syp_bgm.play()
            music_t = 1
            # if synopsis.num == 0:
                # syp_bgm.fadeout(10)  #フェードアウト
        elif mode == "マップ" and music_t == 0:
            map_bgm.play()
        elif mode == "バトル" and music_t == 0:
            battle_bgm.play()
            if battle == 1: #攻撃が行われたとき#ループなし
                panch.play()
        elif mode == "エンディング" and music_t == 0:
            ed_bgm.play()
        elif mode == "ゲームオーバー" and music_t == 0: #ループなし
            gameover.play()
        
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                gamemode = "2"
            if event.type == pg.KEYDOWN and event.key == pg.K_t:
                mode = "あらすじ"  #ゲームモードを1にする
                op_bgm.stop()
                music_t = 0
                gamemode = "100"
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                syp_bgm.stop()
                Map_Mode = "map"
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if novel_mode == 2:
                    novel_mode = 0
                    novel.alpha_num = 255
                elif novel.novel_num == len(Novel.novel_lst[novel.novel_num])-1:
                    novel_mode = 1
                else:
                    novel.novel_num += 1
            if mode == "あらすじ":
                if not synopsis.key_event(event):
                    pg.quit()
                    sys.exit()

        if mode == "あらすじ":
            synopsis.update(screen)

        if gamemode == "0": #もしゲームモードが0ならば
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            img1 = fonto1.render("倒せこうかとん", 0, (0, 0, 0)) #タイトル
            screen.blit(bg,[0,0]) #背景画像
            screen.blit(shikaku, shikaku_rect)
            screen.blit(img1, [400, 150])
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
            img2 = fonto2.render("Press t to Start", 0, (0, 255, 255))
            screen.blit(img2, [450, 400])
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (400, 400)) 
            screen.blit(cha1,[-50,400]) #キャラクター1
            cha2 = pg.image.load(f"fig/PL6.png").convert_alpha()
            cha2 = pg.transform.scale(cha2, (400, 400)) 
            screen.blit(cha2,[190,400]) #キャラクター2
            cha3 = pg.image.load(f"fig/pl5.png").convert_alpha()
            cha3 = pg.transform.scale(cha3, (400, 400)) 
            screen.blit(cha3,[430,400]) #キャラクター3
            cha4 = pg.image.load(f"fig/chibi_20240527_185904.png").convert_alpha()
            cha4 = pg.transform.scale(cha4, (400, 400)) 
            screen.blit(cha4,[670,400]) #キャラクター4
            cha5 = pg.image.load(f"fig/chibi_20240527_181131.png").convert_alpha()
            cha5 = pg.transform.scale(cha5, (400, 400)) 
            screen.blit(cha5,[910,400]) #キャラクター5
            fonto3 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
            img3 = fonto3.render("キャラクタープロフィール:shift", 0, (255, 0, 255))
            screen.blit(img3, [350, 700])
            pg.display.update()

        elif gamemode == "1": #もしゲームモードが1ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            img = fonto.render("あらすじ", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(img, [400, 250]) #あらすじ表示
            pg.display.update()
        
        elif gamemode == "2": #もしゲームモードが2ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara1name = fonto.render("さゆか", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara1name, [400, 250]) #chara1name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara1pro = fonto1.render("しっかり者のお姉さん系、ベーシスト。", 0, (0, 0, 0))
            screen.blit(chara1pro, [400, 400]) #chara1pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (500, 500))
            screen.blit(cha1,[0,200]) #キャラクター1 
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return 
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "3"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "6"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "3": #もしゲームモードが3ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara2name = fonto.render("せいな", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara2name, [400, 250]) #chara2name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara2pro = fonto1.render("冷静そうで熱い何かを持っている。", 0, (0, 0, 0))
            screen.blit(chara2pro, [400, 400]) #chara2pro表示
            chara2pro = fonto1.render("チームのまとめ役。", 0, (0, 0, 0))
            screen.blit(chara2pro, [400, 470]) #chara2pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha2 = pg.image.load(f"fig/PL6.png").convert_alpha()
            cha2 = pg.transform.scale(cha2, (500, 500)) 
            screen.blit(cha2,[0,200]) #キャラクター2
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return 
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "4"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "2"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "4": #もしゲームモードが4ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara3name = fonto.render("こうた", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara3name, [400, 250]) #chara3name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara3pro = fonto1.render("頭がおかしい。ギャグを言う。", 0, (0, 0, 0))
            screen.blit(chara3pro, [400, 400]) #chara3pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha3 = pg.image.load(f"fig/pl5.png").convert_alpha()
            cha3 = pg.transform.scale(cha3, (500, 500)) 
            screen.blit(cha3,[0,200]) #キャラクター3
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "5"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "3"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "5": #もしゲームモードが5ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara4name = fonto.render("ほのか", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara4name, [400, 250]) #chara4name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara4pro = fonto1.render("ずっと泣いている。心優しい女の子", 0, (0, 0, 0))
            screen.blit(chara4pro, [400, 400]) #chara4pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha4 = pg.image.load(f"fig/chibi_20240527_185904.png").convert_alpha()
            cha4 = pg.transform.scale(cha4, (500, 500)) 
            screen.blit(cha4,[0,200]) #キャラクター4
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "6"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "4"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "6": #もしゲームモードが6ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara5name = fonto.render("まの", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara5name, [400, 250]) #chara5name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara5pro = fonto1.render("落ち着きない人。", 0, (0, 0, 0))
            screen.blit(chara5pro, [400, 400]) #chara5pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha5 = pg.image.load(f"fig/chibi_20240527_181131.png").convert_alpha()
            cha5 = pg.transform.scale(cha5, (500, 500)) 
            screen.blit(cha5,[0,200]) #キャラクター5
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "2"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "5"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "100"
                    Map_Mode = "map"
        
        if Map_Mode == "map":
            map.update(screen, score)
            map_pl_mode = 100
            if novel_mode == 1:
                novel.alpha()
                if novel.alpha_num == 0:
                    novel.alpha_num = 0
                    novel.novel_num = 0
                    novel_mode = 2
            novel.update(screen, map)
            
            # mapの画面遷移についてのfor文
            for mpl_k in mpl_lst:
                if check_bound(mpl_k.rect2) != (True, True):
                    if enemy_mode[map.scene_num] == 1:
                        all_mode = 1
                        if map_mode[map.scene_num][0] == 0 and check_bound2(mpl_k.rect2) == (False, True, True, True):
                            map_pl_mode = 0
                        elif map_mode[map.scene_num][1] == 0 and check_bound2(mpl_k.rect2) == (True, False, True, True):
                            map_pl_mode = 1
                        elif map_mode[map.scene_num][2] == 0 and check_bound2(mpl_k.rect2) == (True, True, False, True):
                            map_pl_mode = 2
                        elif map_mode[map.scene_num][3] == 0 and check_bound2(mpl_k.rect2) == (True, True, True, False):
                            map_pl_mode = 3
                    else:
                        all_mode = 1
            
            # 実際の画面変位動作の実行
            if map_pl_mode == 0:
                map.scene_num = map_saki[map.scene_num][0]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 1:
                map.scene_num = map_saki[map.scene_num][1]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 2:
                map.scene_num = map_saki[map.scene_num][2]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 3:
                map.scene_num = map_saki[map.scene_num][3]
                novel.novel_num = 0
                novel.alpha_num = 255
                
            # プレイヤーをupdate
            for mpl_k in mpl_lst:
                mpl_k.update(screen, key_lst, all_mode, map.scene_num, map_mode)
            all_mode = 0    # all_modeをリセット
            map_enemy.update(screen, map.scene_num)
            
            # 敵とプレイヤーが遭遇した時の処理
            for mpl in mpl_lst:
                if map_enemy.rect.colliderect(mpl.rect2):
                    enemy_mode[map.scene_num] = 1
            novel.update(screen, map)
        pg.display.update()   


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()