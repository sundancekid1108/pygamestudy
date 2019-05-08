#모듈import
import pygame
import math
import random
#초기화
pygame.init()

#help 명령어로 메서드 설명 보기가 가능하다 help(pygame.init)

width, height = 1280, 960

#스크린 만들기
screen = pygame.display.set_mode((width, height))

#이미지를 불러와 오브젝트 생성
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")


keys = [False, False, False, False] #처음 키값.. 입력받을것들 WASD
playpos = [ 500, 480] # 플레이어 위치 값이 바뀌면서 움직일수 있다..
# 경로 입력하는 부분을 모르겠다..


#화살 추가
acc = [0, 0]
arrows = [] # 화살 정보

#적
badtimer=100
badtimer1=0
badguys=[[1280, 960],] #적이 출현하는 위치


#HP
healthvalue = 194

#계속 보이게 반복
running = 1
exitcode = 0
while running:
    badtimer-=1 # 왜 넣는지모름..

    #화면 계속 띄우기
    screen.fill((0,0,0))

    #배경그리기 , # //는 소수점 버림..
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
          screen.blit(grass, (x*100, y*100))

    screen.blit(castle, (0, 50))
    screen.blit(castle, (0, 200))
    screen.blit(castle, (0, 350))
    screen.blit(castle, (0, 500))
    screen.blit(castle, (0, 650))

    #플레이어 포지션 회전, https://opentutorials.org/course/3045/18395 두번째 강
    position = pygame.mouse.get_pos() #현재 마우스의 위치값 가져옴..
    angle = math.atan2(position[1]- (playpos[1]+32), position[0]- (playpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29) # 로테이션. 객체를 각도만큼 회전시켜주는 함수
    playerpos1 = (playpos[0] - playerrot.get_rect().width//2, playpos[1] - playerrot.get_rect().height//2)
    screen.blit(playerrot, playerpos1)


    #화살 그리기
    #bullet은 [각도, 플레이어의 x좌표, y좌표]
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 20  #코사인 곱하면 x 속도 성분
        vely = math.sin(bullet[0]) * 20  #sin 곱하면 y 속도 성분
        bullet[1] = bullet[1] + velx
        bullet[2] = bullet[2] + vely
        if bullet[1] < -64 or bullet[1] > 1280 or bullet[2] < -64 or bullet[2] > 960:
            arrows.pop(index) #화면 밖으로 나가거나 아래로 나거가나 할때 . arrow.pop으로 index 없앰
        index = index + 1

    for projectile in arrows: #방향에 따라 arrow 회전...
        arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29) #porjectile[0] 는 각도값, rad이라 57.29곱해줌
        screen.blit(arrow1, (projectile[1], projectile[2])) #회전된 객체를 보여줌



    #적 추가
    if badtimer == 0:
        badguys.append([1200, random.randint(50,900)]) #적 리스폰 위치 x 1200, y 50~900사이에서 나옴
        badtimer = 100-(badtimer1*2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 = badtimer1+5
    index=0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] = badguy[0]-7

        # 성 공격
        badrect = pygame.Rect(badguyimg.get_rect()) #사각형이미지의 정보 오브젝트로 가져옴
        badrect.top = badguy[1]  #badguy의 y좌표값
        badrect.left = badguy[0] #badguy x좌표값

        # 맵을 가로질러가서  데미지를 주는 로직..  
        if badrect.left < 64:
            healthvalue = healthvalue-random.randint(5,20)
            badguys.pop(index)

        # 케릭터의 공격 로직.. 화살에 맞은 적 사라짐
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1] #x좌표
            bullrect.top = bullet[2] #좌표

            #colliderect => 객체끼리 충돌했는지 (여기선 badrect와 bullrect가 충돌했는지), True면 실행
            if badrect.colliderect(bullrect):
                acc[0] = acc[0]+1 #화살 맞은 개수 카운트..(점수로)
                badguys.pop(index)  # 악당 없에기
                arrows.pop(index1)  # 화살 없에기 
            index1 = index1+1

        # 6.3.3 - 다음 오소리
        index = index+1
    for badguy in badguys:
        screen.blit(badguyimg, badguy) #화면에 badguy 그려줌


    #시간 카운트 (약속으로 이렇게 쓴대..)
    font = pygame.font.Font(None, 24) #폰트 종류, 사이즈,  None은 기본..
    survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+\
        ":"+str(((90000-pygame.time.get_ticks())//1000)%60).zfill(2), True, (0,0,0))
    # survivedtext = font.render("{0:.2f}".format(9000-pygame.time.get_ticks()/1000)+" : "+"{0:.2f}".format(((90000-pygame.time.get_ticks())/1000)%60).zfill(2), True, (0,0,0))
    # 밀리세컨드라 90000쓴다..
    # 몇초가 남았는지를 카운트해서 보여줌...
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]  #여기 좌표에 표시함..
    screen.blit(survivedtext, textRect)

    #HP 표시
    screen.blit(healthbar, (5,5)) #healthbar를 5,5 위치에 표신
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8)) #health그림 위에 여러개를 덮음.. healthvalue가 줄어들수록 표시가 적어짐..

    

    


    # 화면 다시 그리기 flip은 화면 전체 업데이트
    pygame.display.flip()





    #게임 종료
    for event in pygame.event.get():  #이벤트 발생하면
        # 화면에 X 눌렀을때 꺼지게
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            
        #마우스 컨트롤
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()  # 현재 마우스의 위치값을 찾아 position에 대입  각cf. /하면 밑으로 내려쓸수있다.
            acc[1] = acc[1] + 1
            arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), \
                                      position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32, \
                           playerpos1[1] + 32])


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        
    #player 움직이기
    if keys[0] == True:
        playpos[1] = playpos[1] - 10
    elif keys[2] == True:
        playpos[1] = playpos[1] + 10 #아래로 내려감
    elif keys[1] == True:
        playpos[0] = playpos[0] - 10 # 왼쪽이동
    elif keys[3] == True:
        playpos[0] += 10 #오른

        

        # 승리 / 패배 로직
        #10 - Win/Lose 검사
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    #90초 버티면 끝(승리)    
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    # HP 다  떨어지면 끝(패배 )    
    if acc[1] != 0:
        accuracy = acc[0]*1.0/acc[1]*100 #명중률..
    else:  
        accuracy = 0        
    

# 승리 /패배 결과창
if exitcode == 0:    # 패배 (LOSE)
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+"{0:.2f}".format(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)

else:    # 게임승리 (WIN)
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+"{0:.2f}".format(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

    


